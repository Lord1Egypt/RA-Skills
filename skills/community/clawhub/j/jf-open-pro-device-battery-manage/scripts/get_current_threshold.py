#!/usr/bin/env python3
"""
查询设备当前低电量阈值（开发版）

API: POST /gwp/v3/rtc/device/getconfig/{deviceToken}
Name: Ability.AovAbility
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
    """生成请求头"""
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


def get_current_threshold(device_token: str, uuid: str, app_key: str, app_secret: str, move_card: int, endpoint: str):
    """
    获取当前低电量阈值
    
    API: POST /gwp/v3/rtc/device/getconfig/{deviceToken}
    Name: Dev.LowElectrMode
    
    官方文档：https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=9bf993f3140ad9f9b4390fee750ba740&lang=zh
    """
    base_url = f"https://{endpoint}/gwp/v3"
    url = f"{base_url}/rtc/device/getconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "Name": "Dev.LowElectrMode"
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") == 2000:
        data = result.get("data", {})
        low_elect_mode = data.get("Dev.LowElectrMode", {})
        return {
            "PowerThreshold": low_elect_mode.get("PowerThreshold"),
            "LowElectrMin": low_elect_mode.get("LowElectrMin"),
            "LowElectrMax": low_elect_mode.get("LowElectrMax")
        }
    else:
        raise RuntimeError(f"查询失败：{result.get('msg', '未知错误')}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="查询当前低电量阈值")
    parser.add_argument("--device-sn", required=True, help="设备序列号")
    parser.add_argument("--device-token", required=True, help="设备 Token")
    parser.add_argument("--uuid", default=os.getenv("JF_UUID"), help="开放平台用户 uuid")
    parser.add_argument("--app-key", default=os.getenv("JF_APP_KEY"), help="应用 appKey")
    parser.add_argument("--app-secret", default=os.getenv("JF_APP_SECRET"), help="应用密钥")
    parser.add_argument("--move-card", type=int, default=os.getenv("JF_MOVE_CARD", "2"), help="移动卡标识")
    parser.add_argument("--endpoint", default=os.getenv("JF_ENDPOINT", "api-cn.jftechws.com"), help="API 接入地址")
    
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
        print(f"正在查询设备 {args.device_sn} 的当前低电量阈值...")
        print()
        
        result = get_current_threshold(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            endpoint=args.endpoint
        )
        
        print("✅ 查询成功")
        print()
        print("设备信息:")
        print(f"  设备：{args.device_sn}")
        if result['PowerThreshold'] is not None:
            print(f"  当前阈值：{result['PowerThreshold']}%")
        else:
            print(f"  当前阈值：未设置")
        print(f"  最小阈值：{result['LowElectrMin']}%")
        print(f"  最大阈值：{result['LowElectrMax']}%")
        print()
        print(f"💡 提示：设置阈值时请在 {result['LowElectrMin']}% ~ {result['LowElectrMax']}% 范围内")
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}")
        sys.exit(1)
