import requests
import json
import uuid

# 生成海报url
def generate_poster_url(token, record_data):
    url = f"https://server.pinza.com.cn/gpt/design/gemini"
    headers = {'token': token}
    files=[]
   
    response = requests.post(url, headers=headers, data=record_data, files=files)
    response_data = response.json()
    
    if response_data['code'] == "0" :
        return response_data['data']['images'][0]['url']
    else:
        return None
    

if __name__ == "__main__":
    import sys
    token = sys.argv[1]
    record_data = json.loads(sys.argv[2])
    record_data['groupId'] = str(uuid.uuid4())  # 添加唯一请求ID
    poster_url = generate_poster_url(token, record_data)
    if poster_url:
        print(poster_url)
