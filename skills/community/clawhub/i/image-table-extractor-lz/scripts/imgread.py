import requests
import json
import argparse
import os


def KpImgReadRun(file_path, ketop_key):
    # 解析图片
    print("解析文件")
    url = "https://kpp.ketop.cn/Api/KpAiImgTbApi?act=imgtb"

    header = {
        "X-API-Key": f"{ketop_key}"
    }

    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url,headers=header,files=files)
        if response.status_code == 200:
            result = response.json()
            #print(json.dumps(result))
            if result["code"] == 0:
                #print("上传成功")
                wk_data = result["data"]
                print(wk_data)
                return wk_data
            else:
                print("失败")
                return None


def main():

    parser = argparse.ArgumentParser(description='图片解析')
    parser.add_argument('-f', '--file', help='图片路径')
    # parser.add_argument('-k', '--key', help='ketop_key')
    
    args = parser.parse_args()

    if args.file:
        file_path = args.file
        ketop_key = os.getenv('KETOP_KEY_TOKEN')
        #ketop_key = args.key
        KpImgReadRun(file_path = file_path, ketop_key=ketop_key);
        
    else:
        print("参数错误")
    
if __name__ == "__main__":
    main()
    