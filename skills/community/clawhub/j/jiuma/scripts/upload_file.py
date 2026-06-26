import requests
import json
import sys
import keyring
import os

# 调用：
# python ~/.openclaw/workspace/skills/jiuma/scripts/upload_file.py --file_path=~/.openclaw/workspace/douyin-downloads/audio.wav

API_BASE_URL = "https://api.jiuma.com/"

# 接口端点
UPLOAD_ENDPOINT = "/console/aiApp/uploadOneFile"

def get_token():
    """获取已保存的token"""
    try:
        token = keyring.get_password("jiuma_ai", "authorized_token")
        if token and len(token) > 20:  # 基本验证token长度
            return token
    except (keyring.errors.KeyringError, FileNotFoundError):
        pass
    return None

def upload_file_with_token(file_path):
    """使用token上传文件"""
    url = f"{API_BASE_URL}{UPLOAD_ENDPOINT}"
    
    # 获取token
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    with open(os.path.expanduser(file_path), 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()
    return result
        
        

def get_argv(key='channel'):
    cmd_format_key = '--'+key+'='
    value = [arg for arg in sys.argv if arg.find(cmd_format_key)!=-1]
    if len(value)>0:
        return value[0].replace(cmd_format_key,"")
    else:
        raise Exception(f"缺少参数{key}")

if __name__ == "__main__":
    try:
        file_path = get_argv('file_path')
        # 执行上传
        file_url = upload_file_with_token(file_path)
        
        # 输出结果
        result = {
            "code": 200,
            "data": {
                "file_url": file_url
            }
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)
    except Exception as e:
        print(f"错误: {e}")
        print('请严格按照参数文档要求进行运行')
        sys.exit(1)
