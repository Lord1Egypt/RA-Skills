#!/usr/bin/env python3
"""
室外安防统计查询脚本 - 查询统计数据和图表

支持平台：JF Tech（杰峰）
用法：
    python stats_query.py --action count --type vehicle --start-time <时间戳> --end-time <时间戳> [其他参数]
    python stats_query.py --action day-chart --type vehicle [其他参数]
    python stats_query.py --action week-chart --type vehicle [其他参数]

签名算法：
    - timeMillis: 使用 TimeMillisUtil.getTimMillis() 生成（counter 7 位 + timestamp 13 位 = 20 位）
    - signature: 使用 SignatureUtil.getEncryptStr() 生成（移位 + 合并 + MD5）
"""

import argparse
import json
import sys
import time
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 导入杰峰签名工具
from jf_signature import generate_signature


def query_count(sn: str, user: str, behavior_type: str, start_time: str, end_time: str,
                uuid: str, appkey: str, secret: str, authorization: str, movecard: int) -> dict:
    """查询标签出现次数统计"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/outdoorSecurity/static/count"
    
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
        "type": behavior_type,
        "startTime": start_time,
        "endTime": end_time
    }
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def query_day_chart(sn: str, user: str, behavior_type: str, start_time: str, end_time: str,
                    uuid: str, appkey: str, secret: str, authorization: str, movecard: int) -> dict:
    """查询当日统计（小时图表）"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/outdoorSecurity/static/day/chart"
    
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
        "type": behavior_type,
        "startTime": start_time,
        "endTime": end_time
    }
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def query_week_chart(sn: str, user: str, behavior_type: str, start_time: str, end_time: str,
                     uuid: str, appkey: str, secret: str, authorization: str, movecard: int) -> dict:
    """查询周统计（天图表）"""
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/outdoorSecurity/static/week/chart"
    
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
        "type": behavior_type,
        "startTime": start_time,
        "endTime": end_time
    }
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def format_result(result: dict, action: str) -> str:
    """格式化查询结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    if result.get("code") != 2000:
        code = result.get('code')
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通室外安防套餐，请登录开放平台绑定套餐卡"
        elif code == 28007:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 Header 参数错误，请检查 uuid、appKey、timeMillis、signature"
        elif code == 40103:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 无效 Token，authorization 可能过期"
        return f"❌ API 错误码：{code}\n{msg}"
    
    data = result.get("data", {})
    
    if action == "count":
        count = data.get("count", 0)
        return f"✅ 统计次数：{count} 次"
    
    elif action == "day-chart":
        chart_data = data.get("chartData", [])
        if not chart_data:
            return "ℹ️ 暂无图表数据"
        
        output = "✅ 当日统计图表数据:\n"
        for item in chart_data:
            hour = item.get("hour", "")
            value = item.get("value", 0)
            output += f"  {hour}:00 - {value}次\n"
        return output
    
    elif action == "week-chart":
        chart_data = data.get("chartData", [])
        if not chart_data:
            return "ℹ️ 暂无图表数据"
        
        output = "✅ 周统计图表数据:\n"
        for item in chart_data:
            date = item.get("date", "")
            value = item.get("value", 0)
            output += f"  {date}: {value}次\n"
        return output
    
    return "✅ 查询成功"


def main():
    parser = argparse.ArgumentParser(description="室外安防 - 统计查询")
    parser.add_argument("--action", required=True, choices=["count", "day-chart", "week-chart"],
                        help="操作类型：count=次数统计，day-chart=当日图表，week-chart=周图表")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token (Authorization)")
    parser.add_argument("--movecard", type=int, default=7, help="移动卡标识（用于签名）")
    parser.add_argument("--type", default="vehicle", help="统计类型：vehicle=车辆，person=人员")
    parser.add_argument("--start-time", help="开始时间（秒级时间戳）")
    parser.add_argument("--end-time", help="结束时间（秒级时间戳）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细 curl 命令和原始响应（重要查询必须使用）")
    
    args = parser.parse_args()
    
    # 如果没有提供时间参数，使用默认值（最近 7 天）
    if not args.start_time or not args.end_time:
        end_ts = int(time.time())
        start_ts = end_ts - (7 * 24 * 60 * 60)
        start_time = str(start_ts)
        end_time = str(end_ts)
    else:
        start_time = args.start_time
        end_time = args.end_time
    
    if args.action == "count":
        result = query_count(
            sn=args.sn, user=args.user, behavior_type=args.type,
            start_time=start_time, end_time=end_time,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret,
            authorization=args.auth, movecard=args.movecard
        )
    elif args.action == "day-chart":
        result = query_day_chart(
            sn=args.sn, user=args.user, behavior_type=args.type,
            start_time=start_time, end_time=end_time,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret,
            authorization=args.auth, movecard=args.movecard
        )
    elif args.action == "week-chart":
        result = query_week_chart(
            sn=args.sn, user=args.user, behavior_type=args.type,
            start_time=start_time, end_time=end_time,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret,
            authorization=args.auth, movecard=args.movecard
        )
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_result(result, args.action))


if __name__ == "__main__":
    main()
