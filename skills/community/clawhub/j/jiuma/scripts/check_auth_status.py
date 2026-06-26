import sys
import keyring
import requests

API_BASE_URL = "https://api.jiuma.com/"
TOKEN_CHECK_ENDPOINT = "/console/aiApp/tokenStatus"

def get_token():
    """获取已保存的token"""
    try:
        token = keyring.get_password("jiuma_ai", "authorized_token")
        if token and len(token) > 20:  # 基本验证token长度
            return token
    except (keyring.errors.KeyringError, FileNotFoundError):
        pass
    return None

def check_token():
    url = f"{API_BASE_URL}{TOKEN_CHECK_ENDPOINT}"
    
    # 获取token
    token = get_token()
    if not token:
        return False
    try:
        response = requests.post(url, headers={"Content-Type": "application/json","Authorization": f"Bearer {token}"}, timeout=30)
    except Exception as e:
        return False
    return response.json()['code']==200



if __name__=="__main__":
    try:
        if check_token():
            print("已授权")
        else:
            print("未授权，或者授权过期请重新授权")
        sys.exit(0)
    except Exception as e:
        print(e)
        print("请严格按照参数文档要求进行运行")
        sys.exit(1)