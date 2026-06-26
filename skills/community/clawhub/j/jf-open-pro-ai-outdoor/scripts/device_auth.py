#!/usr/bin/env python3
"""
室外安防设备认证脚本 - 同步设备登录凭证

支持平台：JF Tech（杰峰）
用法：
    python device_auth.py --action save --device-username <用户名> --device-password <密码> [其他参数]

签名算法：
    - timeMillis: 使用 TimeMillisUtil.getTimMillis() 生成
    - signature: 使用 SignatureUtil.getEncryptStr() 生成
"""

import argparse
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 导入杰峰签名工具
from jf_signature import generate_signature


def save_device_auth(sn: str, user: str, device_username: str, device_password: str,
                     uuid: str, appkey: str, secret: str, authorization: str, movecard: int) -> dict:
    """同步设备登录凭证"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/outdoorSecurity/dev/save"
    
    headers = {
        "Content-Type": "application/json",
        "uuid": uuid,
        "appKey": appkey,
        "timeMillis": time_millis,
        "signature": signature,
        "Authorization": authorization
    }
    
    body = {
        "sn": sn,
        "user": user,
        "deviceUsername": device_username,
        "devicePassword": device_password
    }
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def format_result(result: dict) -> str:
    """格式化结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    if result.get("code") != 2000:
        code = result.get('code')
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通室外安防套餐"
        elif code == 28007:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 Header 参数错误"
        elif code == 40103:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 无效 Token"
        return f"❌ API 错误码：{code}\n{msg}"
    
    return "✅ 设备登录凭证同步成功"


def main():
    parser = argparse.ArgumentParser(description="室外安防 - 设备认证")
    parser.add_argument("--action", required=True, choices=["save"], help="操作类型")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token (Authorization)")
    parser.add_argument("--movecard", type=int, default=7, help="移动卡标识（用于签名）")
    parser.add_argument("--device-username", required=True, help="设备登录用户名")
    parser.add_argument("--device-password", required=True, help="设备登录密码")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细 curl 命令和原始响应（重要查询必须使用）")
    
    args = parser.parse_args()
    
    result = save_device_auth(
        sn=args.sn, user=args.user,
        device_username=args.device_username,
        device_password=args.device_password,
        uuid=args.uuid, appkey=args.appkey, secret=args.secret,
        authorization=args.auth, movecard=args.movecard
    )
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_result(result))


if __name__ == "__main__":
    main()
