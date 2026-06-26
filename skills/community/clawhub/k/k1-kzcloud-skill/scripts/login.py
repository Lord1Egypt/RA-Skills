# login.py
import requests
import base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()
import json
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64
import argparse
from pathlib import Path

class LoginClient:
    def __init__(self, base_url="http://your-backend-url"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.verify = False

    def get_public_key(self, account):
        """获取RSA公钥"""
        url = f"{self.base_url}/api/v1/SysUser/GenerateEncryptKey"
        params = {"userName": account}

        response = self.session.get(url, params=params, verify=False)
        response.raise_for_status()

        result = response.json()
        # 根据实际返回结构获取 publicKey
        public_key = result.get("result", {}).get("data", {}).get("publicKey")
        if not public_key:
            raise ValueError(f"获取公钥失败: {result}")
        return public_key

    def encrypt_password(self, password: str, pubKey: str) -> str:
        # 确保公钥有正确的PEM格式
        public_key_pem = pubKey.strip()

        # 如果没有PEM头尾，添加它们
        if not public_key_pem.startswith('-----BEGIN PUBLIC KEY-----'):
            # 假设是纯base64格式的DER编码
            public_key_pem = f'-----BEGIN PUBLIC KEY-----\n{public_key_pem}\n-----END PUBLIC KEY-----'

        # 确保每行不超过64字符
        if '-----BEGIN PUBLIC KEY-----' in public_key_pem:
            lines = public_key_pem.split('\n')
            formatted_lines = []
            for line in lines:
                if line.startswith('-----') or len(line) <= 64:
                    formatted_lines.append(line)
                else:
                    # 将长行拆分为64字符一行
                    for i in range(0, len(line), 64):
                        formatted_lines.append(line[i:i + 64])
            public_key_pem = '\n'.join(formatted_lines)

        # 加载公钥
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode('utf-8'),
            backend=default_backend()
        )

        # 使用 PKCS1v15 填充（与JSEncrypt兼容）
        encrypted = public_key.encrypt(
            password.encode('utf-8'),
            padding.PKCS1v15()
        )

        # 返回base64编码的加密密码
        encrypted_password = base64.b64encode(encrypted).decode('utf-8')
        return encrypted_password

    def login(self, account, password, tenant_id=None, remember_client=False):
        """
        用户登录

        Args:
            account: 用户名或邮箱
            password: 明文密码
            tenant_id: 租户ID（可选）
            remember_client: 是否记住登录

        Returns:
            dict: 登录响应数据
        """
        # 1. 获取公钥
        print(f"正在获取公钥，账号: {account}")
        public_key = self.get_public_key(account)
        print("获取公钥成功")

        # 2. 加密密码
        encrypted_password = self.encrypt_password(password,pubKey=public_key)

        # 3. 发送登录请求
        url = f"{self.base_url}/api/v1/SysUser/Authenticate"
        login_data = {
            "password": encrypted_password,
            "userNameOrEmailAddress": account,
            "tenantId": tenant_id,
            "rememberClient": remember_client,
            "mode": "none"  # 不要默认的错误提示
        }

        print(f"正在登录，账号: {account}")
        response = self.session.post(url, json=login_data, verify=False)
        response.raise_for_status()

        result = response.json()
        return result


# 使用示例
if __name__ == "__main__":

    # 创建参数解析器
    parser = argparse.ArgumentParser(description='用户登录脚本')
    parser.add_argument('--account', '-a', type=str, required=True, help='用户名或邮箱')
    parser.add_argument('--password', '-p', type=str, required=True, help='密码')
    parser.add_argument('--tenant_id', '-t', type=str,required=True, default=None, help='租户ID（可选）')

    args = parser.parse_args()
    config={}
    script_dir = Path(__file__).parent
    with open(script_dir.parent / 'config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
    # 配置后端地址
    client = LoginClient(base_url=config.get('baseUrl'))  # 替换为您的后端地址

    # 登录参数
    ACCOUNT = args.account  # 用户名或邮箱
    PASSWORD = args.password  # 明文密码
    TENANT_ID = args.tenant_id  # 租户ID（如需要）
    REMEMBER_ME = True  # 是否记住登录

    try:
        # 执行登录
        result = client.login(
            account=ACCOUNT,
            password=PASSWORD,
            tenant_id=TENANT_ID,
            remember_client=REMEMBER_ME
        )

        # 处理登录结果
        if result.get("success") and result.get("result", {}).get("code") == 0:
            user_info = result.get("result", {}).get("data", {})
            token = user_info.get('accessToken')
            if token:
                print(f"\n登录成功！")
                print(f"token: {token}")
                # 保存 token 到环境变量
                import os, subprocess
                subprocess.run(
                    ['powershell', '-Command',
                     f"[Environment]::SetEnvironmentVariable('K1_KZClOUD_TOKEN', '{token}', 'User')"],
                    capture_output=True
                )
                os.environ['K1_KZClOUD_TOKEN'] = token
                print(f"Token 已保存到用户环境变量 K1_KZClOUD_TOKEN")
            else:
                print(f"\n登录失败: 未获取到 token，响应: {result}")
        else:
            msg = result.get("result", {}).get("msg") or result.get("message") or "未知错误"
            print(f"\n登录失败: {msg}")

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    except Exception as e:
        print(f"其他错误: {e}")