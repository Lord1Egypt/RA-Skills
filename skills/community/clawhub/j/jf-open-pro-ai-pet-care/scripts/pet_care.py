#!/usr/bin/env python3
"""
宠物看护脚本 - 服务状态查询和设置

支持平台：JF Tech（杰峰）
用法：
    python pet_care.py --action status --sn <序列号> --user <用户 ID> [其他凭证参数]
    python pet_care.py --action switch --enable true --sn <序列号> --user <用户 ID> [其他凭证参数]
"""

import argparse
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 导入杰峰签名工具
from jf_signature import generate_signature



def get_switch_status(sn: str, user: str, uuid: str, appkey: str, 
                       secret: str, authorization: str, movecard: int) -> dict:
    """
    查询宠物看护服务状态
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
    
    Returns:
        API 响应字典
    """
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet/ai/analysis/switch/get"
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
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
        "user": user
    }
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def set_switch(sn: str, user: str, enable: bool, uuid: str, appkey: str, 
               secret: str, authorization: str) -> dict:
    """
    开启或关闭宠物看护服务
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        enable: true 开启，false 关闭
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
    
    Returns:
        API 响应字典
    """
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet/ai/analysis/switch/change"
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
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
        "aiAnalysisSwitch": enable
    }
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def format_status_result(result: dict) -> str:
    """格式化服务状态查询结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    if result.get("code") != 2000:
        return f"❌ API 错误码：{result.get('code')}\n{result.get('msg', '')}"
    
    data = result.get("data", {})
    switch_status = data.get("aiAnalysisSwitch", False)
    
    if switch_status:
        return "✅ 宠物看护服务：已开启"
    else:
        return "⏸️  宠物看护服务：已关闭"


def format_switch_result(result: dict, enable: bool) -> str:
    """格式化服务开关结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    if result.get("code") != 2000:
        return f"❌ API 错误码：{result.get('code')}\n{result.get('msg', '')}"
    
    action = "开启" if enable else "关闭"
    return f"✅ 宠物看护服务已{action}"


def main():
    parser = argparse.ArgumentParser(description="宠物看护 - 服务状态查询和设置")
    parser.add_argument("--action", required=True, choices=["status", "switch"], 
                        help="操作类型：status=查询状态，switch=开关设置")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token (Authorization)")
    parser.add_argument("--movecard", type=int, default=7, help="移动卡标识（用于签名）")
    parser.add_argument("--enable", type=str, choices=["true", "false"], 
                        help="开关状态（仅 switch 操作需要）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细 curl 命令和原始响应（重要查询必须使用）")
    
    args = parser.parse_args()
    
    if args.action == "status":
        result = get_switch_status(
            sn=args.sn,
            user=args.user,
            uuid=args.uuid,
            appkey=args.appkey,
            secret=args.secret,
            authorization=args.auth, movecard=args.movecard
        )
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_status_result(result))
    
    elif args.action == "switch":
        if not args.enable:
            print("❌ switch 操作需要指定 --enable 参数 (true/false)")
            sys.exit(1)
        
        enable = args.enable.lower() == "true"
        result = set_switch(
            sn=args.sn,
            user=args.user,
            enable=enable,
            uuid=args.uuid,
            appkey=args.appkey,
            secret=args.secret,
            authorization=args.auth, movecard=args.movecard
        )
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_switch_result(result, enable))


if __name__ == "__main__":
    main()
