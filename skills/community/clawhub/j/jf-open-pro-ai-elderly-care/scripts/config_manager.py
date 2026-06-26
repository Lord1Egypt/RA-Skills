#!/usr/bin/env python3
"""
异常配置管理脚本 - 查询和更新异常提醒设置

支持平台：JF Tech（杰峰）
用法：
    python config_manager.py --action list --sn <序列号> --user <用户 ID> [其他参数]
    python config_manager.py --action update --behavior-type 1 --enable 1 --threshold 3600 [其他参数]
"""

import argparse
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 导入杰峰签名工具
from jf_signature import generate_signature



def find_config_list(sn: str, user: str, uuid: str, appkey: str, 
                     secret: str, authorization: str, movecard: int) -> dict:
    """查询异常提醒配置列表"""
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/elderly/abnormalBehavior/findConfigList"
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


def update_config(sn: str, user: str, behavior_type: int, uuid: str, appkey: str, 
                  secret: str, authorization: str, enable: int = None,
                  behavior_time: int = None, time_unit: int = 2,
                  monitor_times: list = None) -> dict:
    """更新异常提醒配置"""
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/elderly/abnormalBehavior/updateConfig"
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
        "behaviorType": behavior_type
    }
    
    if enable is not None:
        body["enable"] = enable
    if behavior_time is not None:
        body["behaviorTime"] = behavior_time
    if time_unit is not None:
        body["timeUnit"] = time_unit
    if monitor_times:
        body["monitorTimes"] = monitor_times
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


BEHAVIOR_TYPE_MAP = {0: "久未出现", 1: "久坐", 2: "久卧"}


def format_config_list_result(result: dict) -> str:
    """格式化配置列表结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    code = result.get("code", 0)
    if code != 2000:
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通老人看护套餐，请登录开放平台绑定套餐卡"
        return f"❌ API 错误码：{code}\n{msg}"
    
    data = result.get("data", [])
    if not data:
        return "📭 暂无异常提醒配置"
    
    output = ["✅ 异常提醒配置\n"]
    for cfg in data:
        btype = cfg.get('behaviorType', 0)
        btype_name = BEHAVIOR_TYPE_MAP.get(btype, f"未知 ({btype})")
        enable = "✅ 开启" if cfg.get('enable') else "⏸️ 关闭"
        threshold = cfg.get('behaviorTime', 0)
        hours = threshold // 3600
        mins = (threshold % 3600) // 60
        
        output.append(f"📋 {btype_name}:")
        output.append(f"   状态：{enable}")
        output.append(f"   阈值：{hours}小时{mins}分钟 ({threshold}秒)")
        
        monitor_times = cfg.get('monitorTimes', [])
        if monitor_times:
            output.append(f"   监控时间:")
            for mt in monitor_times:
                output.append(f"     {mt.get('startTime', 'N/A')} - {mt.get('endTime', 'N/A')}")
        output.append("")
    
    return "\n".join(output)


def format_update_result(result: dict) -> str:
    """格式化更新结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    code = result.get("code", 0)
    if code != 2000:
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通老人看护套餐，请登录开放平台绑定套餐卡"
        return f"❌ API 错误码：{code}\n{msg}"
    
    return "✅ 配置更新成功"


def main():
    parser = argparse.ArgumentParser(description="异常配置管理 - 查询和更新异常提醒设置")
    parser.add_argument("--action", required=True, choices=["list", "update"], 
                        help="操作类型")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token")
    
    # update 操作参数
    parser.add_argument("--behavior-type", type=int, choices=[0, 1, 2], 
                        help="异常行为类型：0=久未出现，1=久坐，2=久卧")
    parser.add_argument("--enable", type=int, choices=[0, 1], help="是否开启提醒")
    parser.add_argument("--threshold", type=int, help="异常行为时间阈值（秒）")
    parser.add_argument("--time-unit", type=int, default=2, help="时间单位")
    
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细 curl 命令和原始响应（重要查询必须使用）")
    
    args = parser.parse_args()
    
    if args.action == "list":
        result = find_config_list(
            sn=args.sn, user=args.user, uuid=args.uuid,
            appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_config_list_result(result) if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    elif args.action == "update":
        if args.behavior_type is None:
            print("❌ update 操作需要指定 --behavior-type 参数")
            sys.exit(1)
        
        result = update_config(
            sn=args.sn, user=args.user, behavior_type=args.behavior_type,
            enable=args.enable, behavior_time=args.threshold, time_unit=args.time_unit,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_update_result(result) if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    print(output)


if __name__ == "__main__":
    main()
