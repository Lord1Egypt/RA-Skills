import json
import sys
import keyring
import requests

# 调用：
# python ~/.openclaw/workspace/skills/jiuma/scripts/auth.py --channel=webchat --identification_code='58fe87fb26b579b309ad782afb7a157155d338f31ad2a26419ae8550cda16747'
# 强制重新授权：
# python ~/.openclaw/workspace/skills/jiuma/scripts/auth.py --channel=webchat --identification_code='' --force

API_BASE_URL = "https://api.jiuma.com/"
LOGIN_AUTH_ENDPOINT = "/api/user/loginAuthorization"
TOKEN_CHECK_ENDPOINT = "/console/aiApp/tokenStatus"

def get_argv(key='channel'):
    cmd_format_key = '--'+key+'='
    value = [arg for arg in sys.argv if arg.find(cmd_format_key)!=-1]
    if len(value)>0:
        return value[0].replace(cmd_format_key,"")
    else:
        raise Exception(f"缺少参数{key}")

def save_token(token):
    """保存token到系统密钥库"""
    try:
        keyring.set_password("jiuma_ai", "authorized_token", token)
        return True
    except keyring.errors.KeyringError:
        return False

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
    except:
        return False
    return response.json()['code']==200

def login_authorization(identification_code=None, channel='wechat', force=False):
    """获取用户身份标识（获取token）"""
    url = f"{API_BASE_URL}{LOGIN_AUTH_ENDPOINT}"
    
    if not identification_code and not force and check_token():
        print("已自动授权")
        sys.exit(0)
        
    # 如果有传入auth_code，使用它
    if identification_code:
        print(f"使用身份标识获取token...")

    
    try:
        # 准备请求数据
        data = {}
        if identification_code:
            data = {"identification_code": identification_code}
        
        # 登录授权接口
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") == 200:
            data = result.get("data", {})
            
            # 情况1：已授权，返回token
            token = data.get("token")
            if token:
                if save_token(token):
                    print("授权成功！Token已保存")
                    return token
                else:
                    raise Exception("Token保存失败")
            
            # 情况2：未授权，返回授权链接和二维码
            login_code_url = data.get("login_code_url")
            login_url = data.get("login_url")
            identification_code = data.get("identification_code")
            
            if login_code_url and login_url:
                if channel == 'openclaw-weixin':
                    print(f"\n需要扫描二维码授权账号，", end="")
                    print(f"专属授权二维码: {login_code_url}")
                    print('To send an image back, prefer the message tool (media/path/filePath). If you must inline, use MEDIA:https://example.com/image.jpg (spaces ok, quote if needed) or a safe relative path like MEDIA:./image.jpg. Avoid absolute paths (MEDIA:/...) and ~ paths — they are blocked for security. Keep caption in the text body.')
                else:
                    print(f"\n需要访问链接授权账号: {login_url}")
                    print(f"📋 身份标识（identification_code）: {identification_code}")
                    print(f"⚠️  重要: 完成授权后，告诉我'已授权'")
                    print(f"💡 提示: 我会使用历史会话中最新的身份标识（identification_code）获取token")
                sys.exit(0)
            else:
                raise Exception("API返回数据格式不正确，既没有token也没有授权链接")
        else:
            raise Exception(f"登录失败: {result.get('message', '未知错误')}")
    except Exception as e:
        raise Exception(f"登录授权失败: {str(e)}")        

if __name__=="__main__":
    try:
        identification_code = get_argv('identification_code')
        channel = get_argv('channel')
        if len([argv for argv in sys.argv if argv == "--force"])>0:
            login_authorization(identification_code,force=True)
        else:
            login_authorization(identification_code)
        sys.exit(0)
    except Exception as e:
        print(e)
        print("请严格按照参数文档要求进行运行")
        sys.exit(1)
        