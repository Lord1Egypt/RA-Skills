#!/usr/bin/env python3
"""
岗位巡检脚本 - 服务状态查询和设置

支持平台：JF Tech（杰峰）
用法：
    python inspection.py --action status --sn <序列号> --user <用户 ID> --uuid <uuid> --appkey <appKey> --secret <secret> --auth <authorization> --movecard <moveCard>
    python inspection.py --action switch --enable true --sn <序列号> --user <用户 ID> --uuid <uuid> --appkey <appKey> --secret <secret> --auth <authorization> --movecard <moveCard>

签名算法：
    - timeMillis: 使用 TimeMillisUtil.getTimMillis() 生成（counter 7 位 + timestamp 13 位 = 20 位）
    - signature: 使用 SignatureUtil.getEncryptStr() 生成（移位 + 合并 + MD5）

重要：
    - 所有查询直接使用 API，不使用缓存
    - 输出包含完整 curl 命令和原始响应
    - 以实际 API 响应为准，不编造解释
"""

import argparse
import json
import sys
import subprocess
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 导入杰峰签名工具
from jf_signature import generate_signature


def get_switch_status(sn: str, user: str, uuid: str, appkey: str, 
                       secret: str, authorization: str, movecard: int, verbose: bool = False) -> dict:
    """
    查询岗位巡检服务状态
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        movecard: 移动卡标识
        verbose: 是否输出详细 curl 信息
    
    Returns:
        API 响应字典
    """
    # 使用杰峰官方签名算法生成 timeMillis 和 signature
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/joblover/ai/analysis/switch/get"
    
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
    
    # 生成 curl 命令（用于验证）
    curl_cmd = f'''curl -X POST "{url}" \\
  -H "Content-Type: application/json" \\
  -H "uuid: {uuid}" \\
  -H "appKey: {appkey}" \\
  -H "timeMillis: {time_millis}" \\
  -H "signature: {signature}" \\
  -H "Authorization: {authorization}" \\
  -d '{json.dumps(body)}\''''
    
    if verbose:
        print("=" * 60)
        print("🔧 CURL 命令（用于验证）")
        print("=" * 60)
        print(curl_cmd)
        print()
    
    # 直接调用 API，不使用缓存
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            
            if verbose:
                print("=" * 60)
                print("📊 API 响应结果")
                print("=" * 60)
                print(json.dumps(result, indent=2, ensure_ascii=False))
                print()
            
            return result
    except HTTPError as e:
        error_result = {"error": f"HTTP {e.code}", "message": e.read().decode()}
        if verbose:
            print("=" * 60)
            print("❌ API 错误")
            print("=" * 60)
            print(json.dumps(error_result, indent=2, ensure_ascii=False))
            print()
        return error_result
    except URLError as e:
        error_result = {"error": "Network error", "message": str(e)}
        if verbose:
            print("=" * 60)
            print("❌ 网络错误")
            print("=" * 60)
            print(json.dumps(error_result, indent=2, ensure_ascii=False))
            print()
        return error_result


def set_switch(sn: str, user: str, enable: bool, uuid: str, appkey: str, 
               secret: str, authorization: str, movecard: int) -> dict:
    """
    开启或关闭岗位巡检服务
    
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
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/joblover/ai/analysis/switch/change"
    
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
        code = result.get('code')
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通岗位巡检套餐，请登录开放平台绑定套餐卡"
        elif code == 28007:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 Header 参数错误，请检查 uuid、appKey、timeMillis、signature"
        elif code == 40103:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 无效 Token，authorization 可能过期"
        return f"❌ API 错误码：{code}\n{msg}"
    
    data = result.get("data", {})
    switch_status = data.get("aiAnalysisSwitch", False)
    
    if switch_status:
        return "✅ 岗位巡检服务：已开启"
    else:
        return "⏸️  岗位巡检服务：已关闭"


def format_switch_result(result: dict, enable: bool) -> str:
    """格式化服务开关结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    if result.get("code") != 2000:
        code = result.get('code')
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通岗位巡检套餐，请登录开放平台绑定套餐卡"
        elif code == 28007:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 Header 参数错误，请检查 uuid、appKey、timeMillis、signature"
        elif code == 40103:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 无效 Token，authorization 可能过期"
        return f"❌ API 错误码：{code}\n{msg}"
    
    action = "开启" if enable else "关闭"
    return f"✅ 岗位巡检服务已{action}"


def main():
    parser = argparse.ArgumentParser(description="岗位巡检 - 服务状态查询和设置")
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
    parser.add_argument("--endpoint", default="api-cn.jftechws.com", help="API 接入地址")
    
    args = parser.parse_args()
    
    if args.action == "status":
        result = get_switch_status(
            sn=args.sn,
            user=args.user,
            uuid=args.uuid,
            appkey=args.appkey,
            secret=args.secret,
            authorization=args.auth,
            movecard=args.movecard,
            verbose=args.verbose
        )
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif not args.verbose:
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
            authorization=args.auth,
            movecard=args.movecard
        )
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_switch_result(result, enable))


if __name__ == "__main__":
    main()
