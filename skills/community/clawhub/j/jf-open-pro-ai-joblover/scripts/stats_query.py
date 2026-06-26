#!/usr/bin/env python3
"""
统计数据查询脚本 - 查询岗位巡检行为统计数据

支持平台：JF Tech（杰峰）
用法：
    python stats_query.py --action count --type phone --start-time <时间戳> --end-time <时间戳> [其他参数]
    python stats_query.py --action time --type leavePost --start-time <时间戳> --end-time <时间戳> [其他参数]
    python stats_query.py --action week-chart --type phone [其他参数]
    python stats_query.py --action day-chart --type phone [其他参数]

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


def query_count(sn: str, user: str, behavior_type: str, start_time: str, end_time: str,
                uuid: str, appkey: str, secret: str, authorization: str, movecard: int) -> dict:
    """
    查询行为次数统计
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        behavior_type: 行为类型（phone/smoking/sleep/leave/leavePost）
        start_time: 开始时间（秒级时间戳）
        end_time: 结束时间（秒级时间戳）
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        movecard: 移动卡标识
    
    Returns:
        API 响应字典
    """
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/joblover/static/queryCount"
    
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
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def query_time(sn: str, user: str, behavior_type: str, start_time: str, end_time: str,
               uuid: str, appkey: str, secret: str, authorization: str, movecard: int) -> dict:
    """
    查询行为时长统计
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        behavior_type: 行为类型（phone/smoking/sleep/leave/leavePost）
        start_time: 开始时间（秒级时间戳）
        end_time: 结束时间（秒级时间戳）
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        movecard: 移动卡标识
    
    Returns:
        API 响应字典
    """
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/joblover/static/queryTime"
    
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
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def query_time_for_day_chart(sn: str, user: str, behavior_type: str, start_time: str, end_time: str,
                             uuid: str, appkey: str, secret: str, authorization: str, movecard: int) -> dict:
    """
    查询七天行为时长图表数据
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        behavior_type: 行为类型
        start_time: 开始时间（秒级时间戳）
        end_time: 结束时间（秒级时间戳）
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        movecard: 移动卡标识
    
    Returns:
        API 响应字典
    """
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/joblover/static/queryTimeForDayChart"
    
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
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def query_count_for_week_chart(sn: str, user: str, behavior_type: str, start_time: str, end_time: str,
                               uuid: str, appkey: str, secret: str, authorization: str, movecard: int) -> dict:
    """
    查询七天行为次数图表数据
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        behavior_type: 行为类型
        start_time: 开始时间（秒级时间戳）
        end_time: 结束时间（秒级时间戳）
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        movecard: 移动卡标识
    
    Returns:
        API 响应字典
    """
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/joblover/static/queryCountForWeekChart"
    
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
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def format_stats_result(result: dict, action: str) -> str:
    """格式化统计数据查询结果"""
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
    
    if action == "count":
        count = data.get("count", 0)
        return f"✅ 行为次数：{count} 次"
    
    elif action == "time":
        duration = data.get("time", 0)
        minutes = duration // 60
        seconds = duration % 60
        return f"✅ 行为时长：{minutes}分{seconds}秒"
    
    elif action == "day-chart":
        chart_data = data.get("chartData", [])
        if not chart_data:
            return "ℹ️ 暂无图表数据"
        
        output = "✅ 七天行为时长图表数据:\n"
        for item in chart_data:
            date = item.get("date", "")
            value = item.get("value", 0)
            output += f"  {date}: {value}秒\n"
        return output
    
    elif action == "week-chart":
        chart_data = data.get("chartData", [])
        if not chart_data:
            return "ℹ️ 暂无图表数据"
        
        output = "✅ 七天行为次数图表数据:\n"
        for item in chart_data:
            date = item.get("date", "")
            value = item.get("value", 0)
            output += f"  {date}: {value}次\n"
        return output
    
    return "✅ 查询成功"


def main():
    parser = argparse.ArgumentParser(description="岗位巡检 - 统计数据查询")
    parser.add_argument("--action", required=True, 
                        choices=["count", "time", "day-chart", "week-chart"],
                        help="操作类型：count=次数，time=时长，day-chart=七天时长图表，week-chart=七天次数图表")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token (Authorization)")
    parser.add_argument("--movecard", type=int, default=7, help="移动卡标识（用于签名）")
    parser.add_argument("--type", required=True, 
                        help="行为类型：phone=玩手机，smoking=吸烟，sleep=睡觉，leave=离开，leavePost=离岗")
    parser.add_argument("--start-time", help="开始时间（秒级时间戳）")
    parser.add_argument("--end-time", help="结束时间（秒级时间戳）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    # 如果没有提供时间参数，使用默认值（最近 7 天）
    import time
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
            sn=args.sn,
            user=args.user,
            behavior_type=args.type,
            start_time=start_time,
            end_time=end_time,
            uuid=args.uuid,
            appkey=args.appkey,
            secret=args.secret,
            authorization=args.auth,
            movecard=args.movecard
        )
    
    elif args.action == "time":
        result = query_time(
            sn=args.sn,
            user=args.user,
            behavior_type=args.type,
            start_time=start_time,
            end_time=end_time,
            uuid=args.uuid,
            appkey=args.appkey,
            secret=args.secret,
            authorization=args.auth,
            movecard=args.movecard
        )
    
    elif args.action == "day-chart":
        result = query_time_for_day_chart(
            sn=args.sn,
            user=args.user,
            behavior_type=args.type,
            start_time=start_time,
            end_time=end_time,
            uuid=args.uuid,
            appkey=args.appkey,
            secret=args.secret,
            authorization=args.auth,
            movecard=args.movecard
        )
    
    elif args.action == "week-chart":
        result = query_count_for_week_chart(
            sn=args.sn,
            user=args.user,
            behavior_type=args.type,
            start_time=start_time,
            end_time=end_time,
            uuid=args.uuid,
            appkey=args.appkey,
            secret=args.secret,
            authorization=args.auth,
            movecard=args.movecard
        )
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_stats_result(result, args.action))


if __name__ == "__main__":
    main()
