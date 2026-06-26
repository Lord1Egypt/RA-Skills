import requests
import json
import os
import base64


# 默认 Logo URL（用户可自定义）
DEFAULT_LOGOS = {
    "logo_main": "",
    "logo_secondary": "",
    "logo_third": ""
}

# 简单的XOR加密（用于密码混淆，非安全加密）
def encode_password(password):
    if not password:
        return ""
    key = "pinza2026"
    encoded = []
    for i, char in enumerate(password):
        encoded.append(chr(ord(char) ^ ord(key[i % len(key)])))
    return base64.b64encode("".join(encoded).encode()).decode()

def decode_password(encoded):
    if not encoded:
        return ""
    key = "pinza2026"
    try:
        decoded = base64.b64decode(encoded.encode()).decode()
        return "".join(chr(ord(char) ^ ord(key[i % len(key)])) for i, char in enumerate(decoded))
    except:
        return ""


# 从环境变量或配置文件读取账号密码
def get_credentials():
    # 优先从环境变量读取
    username = os.environ.get('LINGQUE_USERNAME')
    password = os.environ.get('LINGQUE_PASSWORD')
    
    if username and password:
        return username, password
    
    # 其次从配置文件读取
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            username = config.get('lingque_username')
            # 解密密码
            encoded_password = config.get('lingque_password_encoded')
            if encoded_password:
                password = decode_password(encoded_password)
            else:
                password = config.get('lingque_password')
            return username, password
    
    return None, None


# 保存账号密码到配置文件（加密存储）
def save_credentials(username, password):
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    config = {}
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    
    config['lingque_username'] = username
    # 加密存储密码
    config['lingque_password_encoded'] = encode_password(password)
    # 移除明文密码（如果存在）
    if 'lingque_password' in config:
        del config['lingque_password']
    
    with open(config_path, 'w') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


# 读取自定义 Logo 配置
def get_logos():
    logos = {}
    
    # 从环境变量读取
    for key in DEFAULT_LOGOS:
        env_key = key.upper()
        logos[key] = os.environ.get(env_key)
    
    # 从配置文件读取（覆盖环境变量）
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            for key in DEFAULT_LOGOS:
                if config.get(key):
                    logos[key] = config[key]
    
    # 过滤空值
    return {k: v for k, v in logos.items() if v}


# 第一步：获取 access_token
def get_access_token(username, password):
    url = f"https://server.pinza.com.cn/pincloud-auth/chat/login"
    headers = {'Content-Type': 'application/json'}
    params = {
        "username": username,
        "password": password
    }
    response = requests.post(url, data=params)
    response_data = response.json()
    if response_data['code'] == "0":
        return response_data['data']
    else:
        return None
    

if __name__ == "__main__":
    import sys
    
    # 支持输出 Logo 配置
    if len(sys.argv) > 1 and sys.argv[1] == '--logos':
        logos = get_logos()
        print(json.dumps(logos, ensure_ascii=False))
        exit(0)
    
    # 优先从命令行参数读取（兼容旧调用方式）
    if len(sys.argv) > 2:
        username = sys.argv[1]
        password = sys.argv[2]
    else:
        username, password = get_credentials()
        
    if not username or not password:
        print("请配置灵雀AI账号密码")
        print("方法1：设置环境变量 LINGQUE_USERNAME 和 LINGQUE_PASSWORD")
        exit(1)
    
    access_token = get_access_token(username, password)
    if access_token:
        # 自动保存到配置文件（加密存储）
        save_credentials(username, password)
        print(access_token)
    else:
        print("获取token失败，请检查账号密码")
        exit(1)
