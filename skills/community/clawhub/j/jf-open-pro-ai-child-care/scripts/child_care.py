#!/usr/bin/env python3
"""
儿童看护脚本 - 服务状态查询和设置

支持平台：JF Tech（杰峰）
用法：
    python child_care.py --action status --sn <序列号> --user <用户 ID> --uuid <uuid> --appkey <appKey> --secret <secret> --auth <authorization> --movecard <moveCard>
    python child_care.py --action switch --enable true --sn <序列号> --user <用户 ID> --uuid <uuid> --appkey <appKey> --secret <secret> --auth <authorization> --movecard <moveCard>

签名算法：
    - timeMillis: 使用 TimeMillisUtil.getTimMillis() 生成（counter 7 位 + timestamp 13 位 = 20 位）
    - signature: 使用 SignatureUtil.getEncryptStr() 生成（移位 + 合并 + MD5）
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
    查询儿童看护服务状态
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        movecard: 移动卡标识
    
    Returns:
        API 响应字典
    """
    # 使用杰峰官方签名算法生成 timeMillis 和 signature
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/child/ai/analysis/switch/get"
    
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
               secret: str, authorization: str, movecard: int) -> dict:
    """
    开启或关闭儿童看护服务
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        enable: true 开启，false 关闭
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        movecard: 移动卡标识
    
    Returns:
        API 响应字典
    """
    # 使用杰峰官方签名算法生成 timeMillis 和 signature
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/child/ai/analysis/switch/change"
    
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


def format_result(result: dict, action: str, enable: bool = None) -> str:
    """格式化结果输出"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    code = result.get("code", 0)
    if code != 2000:
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通儿童看护套餐，请登录开放平台绑定套餐卡"
        return f"❌ API 错误码：{code}\n{msg}"
    
    if action == "status":
        data = result.get("data", {})
        status = "已开启" if data.get("aiAnalysisSwitch") else "已关闭"
        return f"✅ 儿童看护服务：{status}"
    else:
        action_text = "开启" if enable else "关闭"
        return f"✅ 儿童看护服务已{action_text}"


def main():
    parser = argparse.ArgumentParser(description="儿童看护 - 服务状态查询和设置")
    parser.add_argument("--action", required=True, choices=["status", "switch"], 
                        help="操作类型")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token")
    parser.add_argument("--movecard", type=int, required=True, help="移动卡标识")
    parser.add_argument("--enable", type=str, choices=["true", "false"], 
                        help="开关状态（仅 switch 操作需要）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细 curl 命令和原始响应（重要查询必须使用）")
    
    args = parser.parse_args()
    
    if args.action == "status":
        result = get_switch_status(
            sn=args.sn, user=args.user, uuid=args.uuid,
            appkey=args.appkey, secret=args.secret, authorization=args.auth,
            movecard=args.movecard
        )
        output = format_result(result, "status") if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    elif args.action == "switch":
        if not args.enable:
            print("❌ switch 操作需要指定 --enable 参数 (true/false)")
            sys.exit(1)
        enable = args.enable.lower() == "true"
        result = set_switch(
            sn=args.sn, user=args.user, enable=enable, uuid=args.uuid,
            appkey=args.appkey, secret=args.secret, authorization=args.auth,
            movecard=args.movecard
        )
        output = format_result(result, "switch", enable) if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    print(output)


if __name__ == "__main__":
    main()
