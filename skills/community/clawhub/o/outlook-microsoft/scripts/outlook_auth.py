#!/usr/bin/env python3
"""
Microsoft Outlook OAuth 授权脚本 - 世纪互联版
使用 Device Code Flow 实现用户自行授权
"""

import json
import os
import sys
import io
import time
import requests
from pathlib import Path

# 确保 stdout 输出 UTF-8 编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = Path.home() / ".outlook-microsoft"
CONFIG_FILE = CONFIG_DIR / "config.json"
CREDS_FILE = CONFIG_DIR / "credentials.json"
ENV_FILE = SCRIPT_DIR / ".env"


def load_env():
    """从 .env 文件加载环境变量"""
    if not ENV_FILE.exists():
        return
    with open(ENV_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key and value and not os.getenv(key):
                    os.environ[key] = value


load_env()


def load_config():
    if not CONFIG_FILE.exists():
        return None
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def load_credentials():
    if not CREDS_FILE.exists():
        return None
    with open(CREDS_FILE, "r") as f:
        return json.load(f)


def save_credentials(creds):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CREDS_FILE, "w") as f:
        json.dump(creds, f, indent=2)


def get_client_config():
    """获取 Client 配置"""
    client_id = os.getenv("OUTLOOK_CLIENT_ID")
    tenant_id = os.getenv("OUTLOOK_TENANT_ID")
    client_secret = os.getenv("OUTLOOK_CLIENT_SECRET")

    if not client_id or not tenant_id:
        config = load_config()
        if config:
            client_id = client_id or config.get("client_id")
            tenant_id = tenant_id or config.get("tenant_id")
            client_secret = client_secret or config.get("client_secret")

    if not client_id or not tenant_id:
        print(json.dumps({
            "error": "AUTH_001",
            "message": "未配置 OUTLOOK_CLIENT_ID 或 OUTLOOK_TENANT_ID。请在 .env 文件中配置。"
        }, ensure_ascii=False))
        sys.exit(1)

    return client_id, tenant_id, client_secret


def cmd_authorize():
    """使用 Device Code Flow 获取用户授权"""
    client_id, tenant_id, client_secret = get_client_config()

    # 世纪互联 Device Code 端点
    device_code_url = f"https://login.chinacloudapi.cn/{tenant_id}/oauth2/v2.0/devicecode"

    # 请求设备码 - 注意：不需要 client_secret
    device_payload = {
        "client_id": client_id,
        "scope": "offline_access Mail.ReadWrite Mail.Send Calendars.ReadWrite User.Read profile openid"
    }

    print(json.dumps({
        "status": "getting_device_code",
        "message": "正在获取授权码..."
    }, ensure_ascii=False))

    try:
        resp = requests.post(device_code_url, data=device_payload, timeout=30)
        resp.raise_for_status()
        device_data = resp.json()
    except requests.exceptions.HTTPError as e:
        try:
            err_data = e.response.json()
        except:
            err_data = {}
        print(json.dumps({
            "error": "AUTH_002",
            "message": f"获取设备码失败: {err_data.get('error_description', str(e))}",
            "details": err_data
        }, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "error": "AUTH_001",
            "message": f"网络请求失败: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)

    user_code = device_data.get("user_code", "")
    device_code = device_data.get("device_code", "")
    interval = device_data.get("interval", 5)
    expires_in = device_data.get("expires_in", 900)
    # 世纪互联的 verification_url 可能是 microsoft.com/deviceloginchina
    verification_url = device_data.get("verification_uri") or device_data.get("verification_url") or "https://microsoft.com/deviceloginchina"

    print(json.dumps({
        "status": "pending",
        "message": f"请在浏览器中打开以下网址完成授权：\n{verification_url}\n\n输入代码：{user_code}\n\n提示：使用你的世纪互联账号登录并授权。\n授权有效期：{expires_in // 60} 分钟。",
        "url": verification_url,
        "code": user_code,
        "expires_in": expires_in
    }, ensure_ascii=False))

    # 同时打印到 stderr 确保可见
    print(f"\n===== 授权信息 =====", file=sys.stderr)
    print(f"请在浏览器打开: {verification_url}", file=sys.stderr)
    print(f"输入代码: {user_code}", file=sys.stderr)
    print(f"===================\n", file=sys.stderr)

    # 轮询等待授权
    print("等待用户在浏览器完成授权...（完成后按 Ctrl+C 停止）", file=sys.stderr)

    token_url = f"https://login.chinacloudapi.cn/{tenant_id}/oauth2/v2.0/token"
    start_time = time.time()

    while time.time() - start_time < expires_in:
        time.sleep(interval)

        # 换取 token 的请求 - 注意：设备码流不需要 client_secret
        token_payload = {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "client_id": client_id,
            "device_code": device_code
        }

        try:
            resp = requests.post(token_url, data=token_payload, timeout=30)
            resp.raise_for_status()
            token_resp = resp.json()

            access_token = token_resp.get("access_token")
            refresh_token = token_resp.get("refresh_token")
            expires_in_token = token_resp.get("expires_in", 3600)

            if not access_token:
                print(json.dumps({
                    "error": "AUTH_002",
                    "message": "Token 响应中没有 access_token",
                    "response": token_resp
                }, ensure_ascii=False))
                sys.exit(1)

            # 保存凭据
            creds = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": time.time() + expires_in_token - 60,
                "token_type": token_resp.get("token_type", "Bearer")
            }
            save_credentials(creds)

            # 保存配置
            config = {
                "client_id": client_id,
                "tenant_id": tenant_id,
                "client_secret": client_secret
            }
            save_config(config)

            print(json.dumps({
                "status": "success",
                "message": "授权成功！凭据已保存。",
                "expires_in": expires_in_token
            }, ensure_ascii=False))
            return

        except requests.exceptions.HTTPError as e:
            try:
                err_data = e.response.json()
            except:
                err_data = {}
            error = err_data.get("error", "")
            error_desc = err_data.get("error_description", "")

            if error == "authorization_pending":
                print(".", end="", file=sys.stderr)
                continue
            elif error == "slow_down":
                interval += 1
                print(".", end="", file=sys.stderr)
                continue
            elif error == "authorization_declined":
                print(json.dumps({
                    "error": "AUTH_002",
                    "message": "用户拒绝了授权请求"
                }, ensure_ascii=False))
                sys.exit(1)
            elif error == "invalid_grant":
                print(json.dumps({
                    "error": "AUTH_002",
                    "message": f"授权无效: {error_desc}",
                    "hint": "设备码可能已过期，请重新运行 authorize 命令",
                    "details": err_data
                }, ensure_ascii=False))
                sys.exit(1)
            else:
                print(json.dumps({
                    "error": "AUTH_002",
                    "message": f"授权失败: {error} - {error_desc}",
                    "details": err_data
                }, ensure_ascii=False))
                sys.exit(1)

    print(json.dumps({
        "error": "AUTH_001",
        "message": "授权超时，请重新运行 authorize 命令。"
    }, ensure_ascii=False))
    sys.exit(1)


def cmd_refresh():
    """刷新 Access Token"""
    creds = load_credentials()
    if not creds or not creds.get("refresh_token"):
        print(json.dumps({
            "error": "AUTH_001",
            "message": "没有 refresh_token，需要重新运行 authorize 完成授权。"
        }, ensure_ascii=False))
        sys.exit(1)

    client_id, tenant_id, client_secret = get_client_config()

    token_url = f"https://login.chinacloudapi.cn/{tenant_id}/oauth2/v2.0/token"
    token_payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "refresh_token": creds["refresh_token"]
    }
    if client_secret:
        token_payload["client_secret"] = client_secret

    try:
        resp = requests.post(token_url, data=token_payload, timeout=30)
        resp.raise_for_status()
        token_resp = resp.json()

        new_creds = {
            "access_token": token_resp.get("access_token"),
            "refresh_token": token_resp.get("refresh_token", creds["refresh_token"]),
            "expires_at": time.time() + token_resp.get("expires_in", 3600) - 60,
            "token_type": token_resp.get("token_type", "Bearer")
        }
        save_credentials(new_creds)

        print(json.dumps({
            "status": "success",
            "message": "Token 刷新成功",
            "expires_in": token_resp.get("expires_in", 3600)
        }, ensure_ascii=False))

    except requests.exceptions.HTTPError as e:
        try:
            err_data = e.response.json()
        except:
            err_data = {}
        print(json.dumps({
            "error": "AUTH_002",
            "message": f"Token 刷新失败: {err_data.get('error_description', str(e))}",
            "details": err_data
        }, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "error": "AUTH_002",
            "message": f"请求异常: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)


def get_access_token():
    """获取有效的 Access Token"""
    creds = load_credentials()

    if not creds:
        print(json.dumps({
            "error": "AUTH_001",
            "message": "未授权，请先运行 authorize 完成授权。"
        }, ensure_ascii=False))
        sys.exit(1)

    # 检查是否即将过期
    if time.time() < creds.get("expires_at", 0):
        return creds["access_token"]

    # Token 过期，尝试刷新
    print("Token 已过期，尝试刷新...", file=sys.stderr)
    cmd_refresh()
    creds = load_credentials()
    return creds["access_token"] if creds else None


def cmd_test():
    """测试连接"""
    try:
        token = get_access_token()
        if not token:
            sys.exit(1)

        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(
            "https://microsoftgraph.chinacloudapi.cn/v1.0/me",
            headers=headers,
            timeout=30
        )

        if resp.status_code == 200:
            user = resp.json()
            user_email = user.get('mail') or user.get('userPrincipalName', 'N/A')
            print(json.dumps({
                "status": "success",
                "message": f"连接正常！当前用户：{user.get('displayName', 'N/A')} <{user_email}>"
            }, ensure_ascii=False))
        else:
            try:
                err_data = resp.json()
            except:
                err_data = {}
            print(json.dumps({
                "error": "API_002",
                "message": f"API 调用失败: {err_data.get('error', {}).get('message', f'HTTP {resp.status_code}')}",
                "details": err_data
            }, ensure_ascii=False))
            sys.exit(1)

    except Exception as e:
        print(json.dumps({
            "error": "API_001",
            "message": f"连接测试失败: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)


def cmd_status():
    """查看当前授权状态"""
    creds = load_credentials()
    config = load_config()

    if not creds:
        print(json.dumps({
            "authorized": False,
            "message": "未授权或授权已过期"
        }, ensure_ascii=False))
        return

    expires_at = creds.get("expires_at", 0)
    remaining = max(0, expires_at - time.time())

    print(json.dumps({
        "authorized": True,
        "access_token_exists": bool(creds.get("access_token")),
        "refresh_token_exists": bool(creds.get("refresh_token")),
        "expires_at": expires_at,
        "expires_at_readable": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expires_at)) if expires_at else None,
        "remaining_seconds": int(remaining)
    }, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: outlook_auth.py <authorize|refresh|test|status>")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "authorize":
        cmd_authorize()
    elif cmd == "refresh":
        cmd_refresh()
    elif cmd == "test":
        cmd_test()
    elif cmd == "status":
        cmd_status()
    else:
        print(f"未知命令: {cmd}")
        print("可用命令: authorize, refresh, test, status")
        sys.exit(1)
