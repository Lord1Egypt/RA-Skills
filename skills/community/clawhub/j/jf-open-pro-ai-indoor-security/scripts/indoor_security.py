#!/usr/bin/env python3
"""
室内安防脚本 - 服务状态查询和设置

支持平台：JF Tech（杰峰）
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
    """查询室内安防服务状态"""
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/indoor/ai/analysis/switch/get"
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        "Content-Type": "application/json",
        "uuid": uuid,
        "appKey": appkey,
        "timeMillis": time_millis,
        "signature": signature,
        "Authorization": authorization
    }
    
    body = {"sn": sn, "user": user}
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def set_switch(sn: str, user: str, enable: bool, uuid: str, appkey: str, 
               secret: str, authorization: str) -> dict:
    """开启或关闭室内安防服务"""
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/indoor/ai/analysis/switch/change"
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        "Content-Type": "application/json",
        "uuid": uuid,
        "appKey": appkey,
        "timeMillis": time_millis,
        "signature": signature,
        "Authorization": authorization
    }
    
    body = {"sn": sn, "user": user, "aiAnalysisSwitch": enable}
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
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
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通室内安防套餐，请登录开放平台绑定套餐卡"
        return f"❌ API 错误码：{code}\n{msg}"
    
    if action == "status":
        data = result.get("data", {})
        status = "已开启" if data.get("aiAnalysisSwitch") else "已关闭"
        return f"✅ 室内安防服务：{status}"
    else:
        action_text = "开启" if enable else "关闭"
        return f"✅ 室内安防服务已{action_text}"


def main():
    parser = argparse.ArgumentParser(description="室内安防 - 服务状态查询和设置")
    parser.add_argument("--action", required=True, choices=["status", "switch"], 
                        help="操作类型")
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
