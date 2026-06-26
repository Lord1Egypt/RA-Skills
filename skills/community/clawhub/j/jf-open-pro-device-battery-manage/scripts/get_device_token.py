#!/usr/bin/env python3
"""
获取设备 Token（开发版）

API: POST /gwp/v3/rtc/device/token
参考：jf-open-pro-capture 技能实现
"""

import os
import sys
import requests

# 导入加密工具
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from crypto import get_time_millis, generate_signature
except ImportError:
    print("❌ 错误：找不到 crypto.py 模块")
    sys.exit(1)


def get_headers(uuid: str, app_key: str, app_secret: str, move_card: int) -> dict:
    """生成请求头（包含签名和时间戳）"""
    time_millis = get_time_millis()
    signature = generate_signature(uuid, app_key, app_secret, time_millis, move_card)
    
    return {
        "Content-Type": "application/json; charset=UTF-8",
        "uuid": uuid,
        "appKey": app_key,
        "timeMillis": time_millis,
        "signature": signature,
        "X-Request-Id": os.urandom(16).hex()
    }


def get_device_token(device_sn: str, uuid: str, app_key: str, app_secret: str,
                     move_card: int, endpoint: str,
                     access_token: str = "") -> str:
    """
    获取设备 Token
    
    API: POST /gwp/v3/rtc/device/token
    
    Args:
        device_sn: 设备序列号
        uuid: 开放平台用户 uuid
        app_key: 应用 appKey
        app_secret: 应用密钥
        move_card: 移动卡标识
        endpoint: API 接入地址
        access_token: 用户 accessToken（可选）
    
    Returns:
        设备 Token
    
    Raises:
        RuntimeError: 获取失败时抛出
    """
    base_url = f"https://{endpoint}/gwp/v3"
    url = f"{base_url}/rtc/device/token"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "sns": [device_sn],
        "accessToken": access_token
    }
    
    print(f"请求 URL: {url}")
    print(f"请求体：sns={[device_sn]}")
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    print(f"HTTP 状态码：{response.status_code}")
    print(f"响应原始内容：{response.text}")
    
    result = response.json()
    
    if result.get("code") == 2000:
        data = result.get("data", [])
        if data and len(data) > 0:
            token = data[0].get("token")
            return token
        else:
            raise RuntimeError("返回数据为空，设备可能未绑定")
    else:
        raise RuntimeError(f"获取设备 Token 失败：{result.get('msg', '未知错误')} (code={result.get('code')})")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="获取设备 Token（开发版）")
    parser.add_argument("--device-sn", required=True, help="设备序列号")
    parser.add_argument("--uuid", default=os.getenv("JF_UUID"), help="开放平台用户 uuid")
    parser.add_argument("--app-key", default=os.getenv("JF_APP_KEY"), help="应用 appKey")
    parser.add_argument("--app-secret", default=os.getenv("JF_APP_SECRET"), help="应用密钥")
    parser.add_argument("--move-card", type=int, default=os.getenv("JF_MOVE_CARD", "7"), help="移动卡标识")
    parser.add_argument("--endpoint", default=os.getenv("JF_ENDPOINT", "api-cn.jftechws.com"), help="API 接入地址")
    parser.add_argument("--access-token", default="", help="用户 accessToken（可选）")
    
    args = parser.parse_args()
    
    # 验证必需参数
    if not args.uuid:
        print("❌ 错误：缺少 --uuid 或 JF_UUID 环境变量")
        sys.exit(1)
    if not args.app_key:
        print("❌ 错误：缺少 --app-key 或 JF_APP_KEY 环境变量")
        sys.exit(1)
    if not args.app_secret:
        print("❌ 错误：缺少 --app-secret 或 JF_APP_SECRET 环境变量")
        sys.exit(1)
    
    try:
        print(f"正在获取设备 {args.device_sn} 的 Token...")
        print(f"网关：{args.endpoint}")
        print()
        
        token = get_device_token(
            device_sn=args.device_sn,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            endpoint=args.endpoint,
            access_token=args.access_token
        )
        
        print()
        print(f"✅ 获取设备 Token 成功")
        print(f"   设备：{args.device_sn}")
        print(f"   Token: {token}")
        print()
        print(f"💡 提示：设置环境变量后使用 battery_manage.py 查询电量阈值")
        print(f"   export JF_DEVICE_TOKEN=\"{token}\"")
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}")
        print()
        print("💡 可能原因:")
        print("   1. 设备未绑定到开放平台账号")
        print("   2. 设备序列号不正确")
        print("   3. 开放平台凭证（uuid/appKey/appSecret）不正确")
        sys.exit(1)
