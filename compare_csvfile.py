'''
Python homework 
Created on 2015/3/24
@已解決問題:
-0324-
a.自行輸入檔案名稱(0324) (與0330(b).衝突，已拔除)
b.除了考慮到client少記錄的資料 也多檢查了 client 多產出的資料 (0324)
-0330-
a.檢查本身資料是否有重複(0330)
b.加入argv 方便程式直接帶參數 (0330) 
c. function or parameter 重新命名 (0330)
-0331-
a.將輸出結果建立一log檔 (0331)
b.告知user 目前處理進度到哪裡(0331)

@未處理問題:
-0324-
a.處理速度加強，Memory控制  EX: 2GB以上的資料(0324)
0330 Idea:
用csv module 將匯入的csv檔，轉換成dict , 並用第一列的名稱當key
server與client的key值相同，若client csv file 中key值對應的  value 為0 ,即代表client csv file中無此資料，反之亦然
這樣的好處為，資料會越比越少，速度可能會提升，占用的記憶體大小不確定。

@類似寫法:
a. temp= set(adata) - set(bdata) 可以改成  temp =   set(adata).difference(set(bdata))   
#keyword : python , difference 
@author: James
'''
# coding = UTF-8
import collections ,sys
def remove_ID(csvfile):
    try:     
        noID_data = []     
        for line in csvfile :                # 把首欄的id 去掉，id只代表資料的排列順序，無任何意義
            data =line.split(",",1)
            noID_data.append(data[1])
        return noID_data
    except:
        print("Remove ID error")
    finally:
        print("Remove ID process finish")                   
def find_duplicate(noID_data):
    try:
        duplicate_data=[]
        for item, count in collections.Counter(noID_data).items():
            if count > 1:
                    duplicate_data.append(item)
        else:
            pass
        return len(duplicate_data)
    except:
        print("Find duplicate error")
    finally:
        print("Find duplicate process finish")               
def find_difference(server_noID_data,client_noID_data):
    try:
        log = open("%s" %sys.argv[3],"w")
        server_result= set(server_noID_data) - set(client_noID_data)
        server_amount= len(server_result)
        if server_amount == 0:
            log.write("與Server端產生的資料比對,沒有資料不符合，pass")
        else:
            log.write( "與Server端產生的資料比對,有 %d 筆資料不符合!!\n" %server_amount)
            for non_match in server_result:
                log.write(non_match)
                            
        client_result = set(client_noID_data) -set(server_noID_data)
        client_amount=len(client_result)
        if client_amount > 0:
            log.write("但Client端產生的檔案多了%d筆資料!!\n"%client_amount)
            for non_match in client_result:
                log.write(non_match)
        else:
            pass    
    except:
        print(" Find difference error")
    finally:
        print("Find difference process finish")
        log.close()           
def main():
    try:
        server_csv_file=  open ("%s" %sys.argv[1],"r",encoding="UTF8") 
        client_csv_file =  open ("%s" %sys.argv[2],"r",encoding="UTF8")
        log = open("%s" %sys.argv[3],"w")
        server_noID_data = remove_ID(server_csv_file)
        client_noID_data = remove_ID(client_csv_file)          
        if find_duplicate(server_noID_data) > 0:
            log.write("Server資料本身有%d筆重複，請先確認資料正確性再進行比對"%find_duplicate(server_noID_data))          
        elif find_duplicate(client_noID_data)> 0:
            log.write("Client資料本身有%d筆重複，請先確認資料正確性再進行比對"%find_duplicate(client_noID_data))
        else:
            find_difference(server_noID_data, client_noID_data)
        
    except:
        print("格式錯誤，範例為difference.py (server csv檔案位置) (client csv檔案位置) (輸入的log檔(請自行輸入檔名)存放位置")
    finally:
        print("All process finish")
        log.close()
main()