#!/usr/bin/env python3
"""
告警查询脚本 - 查询跌倒告警和异常行为告警列表

支持平台：JF Tech（杰峰）
用法：
    python alarm_query.py --action falldown --start-time <时间戳> --end-time <时间戳> [其他参数]
    python alarm_query.py --action behavior --behavior-type 0 --start-time <时间戳> --end-time <时间戳> [其他参数]
"""

import argparse
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 导入杰峰签名工具
from jf_signature import generate_signature



def query_falldown_alarms(sn: str, user: str, start_time: int, end_time: int,
                          page: int, rows: int, uuid: str, appkey: str, 
                          secret: str, authorization: str) -> dict:
    """查询跌倒告警列表"""
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/elderly/falldown/alarm/page"
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
        "startTime": start_time,
        "endTime": end_time,
        "page": page,
        "rows": rows
    }
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def query_behavior_alarms(sn: str, user: str, behavior_type: int, 
                          start_time: int, end_time: int,
                          page: int, rows: int, uuid: str, appkey: str, 
                          secret: str, authorization: str) -> dict:
    """查询异常行为告警列表"""
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/elderly/behavior/alarm/page"
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
        "behaviorType": behavior_type,
        "startTime": start_time,
        "endTime": end_time,
        "page": page,
        "rows": rows
    }
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


BEHAVIOR_TYPE_MAP = {0: "久未出现", 1: "久坐", 2: "久卧"}


def format_alarm_result(result: dict, alarm_type: str, behavior_type: int = None) -> str:
    """格式化告警列表结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    code = result.get("code", 0)
    if code != 2000:
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通老人看护套餐，请登录开放平台绑定套餐卡"
        return f"❌ API 错误码：{code}\n{msg}"
    
    data = result.get("data", {})
    records = data.get("records", [])
    total = data.get("total", 0)
    
    if not records:
        return "📭 未找到告警记录"
    
    if alarm_type == "falldown":
        title = "🚨 跌倒告警"
    else:
        btype_name = BEHAVIOR_TYPE_MAP.get(behavior_type, f"异常行为")
        title = f"🚨 {btype_name}告警"
    
    output = [f"{title}（共 {total} 条，显示 {len(records)} 条）\n"]
    
    for i, alarm in enumerate(records, 1):
        output.append(f"告警 {i}:")
        output.append(f"   告警 ID: {alarm.get('alarmId', 'N/A')}")
        output.append(f"   设备：{alarm.get('sn', 'N/A')}")
        output.append(f"   时间：{alarm.get('alarmTime', 'N/A')}")
        if alarm.get('picUrl'):
            output.append(f"   图片：有")
        if alarm.get('videoUrl'):
            output.append(f"   视频：有")
        output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="告警查询 - 跌倒告警和异常行为告警")
    parser.add_argument("--action", required=True, choices=["falldown", "behavior"], 
                        help="操作类型")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token")
    parser.add_argument("--start-time", type=int, required=True, help="开始时间（时间戳秒值）")
    parser.add_argument("--end-time", type=int, required=True, help="结束时间（时间戳秒值）")
    parser.add_argument("--page", type=int, default=1, help="页码")
    parser.add_argument("--rows", type=int, default=10, help="每页条数")
    
    # behavior 操作参数
    parser.add_argument("--behavior-type", type=int, choices=[0, 1, 2], 
                        help="异常行为类型：0=久未出现，1=久坐，2=久卧")
    
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细 curl 命令和原始响应（重要查询必须使用）")
    
    args = parser.parse_args()
    
    if args.action == "falldown":
        result = query_falldown_alarms(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            page=args.page, rows=args.rows,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_alarm_result(result, "falldown") if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    elif args.action == "behavior":
        if args.behavior_type is None:
            print("❌ behavior 操作需要指定 --behavior-type 参数")
            sys.exit(1)
        
        result = query_behavior_alarms(
            sn=args.sn, user=args.user, behavior_type=args.behavior_type,
            start_time=args.start_time, end_time=args.end_time,
            page=args.page, rows=args.rows,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_alarm_result(result, "behavior", args.behavior_type) if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    print(output)


if __name__ == "__main__":
    main()
