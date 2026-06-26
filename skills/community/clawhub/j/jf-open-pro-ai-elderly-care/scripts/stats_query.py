#!/usr/bin/env python3
"""
统计数据查询脚本 - 查询今日统计和近七日统计数据

支持平台：JF Tech（杰峰）
用法：
    python stats_query.py --action daily-routine --start-time <时间戳> --end-time <时间戳> [其他参数]
    python stats_query.py --action week-diet --start-time <时间戳> --end-time <时间戳> [其他参数]
"""

import argparse
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 导入杰峰签名工具
from jf_signature import generate_signature



def query_daily_routine(sn: str, user: str, start_time: int, end_time: int,
                        stat_type: str, uuid: str, appkey: str, 
                        secret: str, authorization: str) -> dict:
    """查询今日作息统计"""
    base_url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/elderly/static/dailyRoutineRecord"
    type_map = {
        "walk-count": "/walkCount",
        "walk-time": "/walkTime",
        "sit-count": "/sitAndLyingCount",
        "sit-time": "/sitAndLyingTime",
        "play-count": "/playCount",
        "play-time": "/playTime"
    }
    
    url = base_url + type_map.get(stat_type, "")
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        "Content-Type": "application/json",
        "uuid": uuid,
        "appKey": appkey,
        "timeMillis": time_millis,
        "signature": signature,
        "Authorization": authorization
    }
    
    body = {"sn": sn, "user": user, "startTime": start_time, "endTime": end_time}
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def query_daily_diet(sn: str, user: str, start_time: int, end_time: int,
                     stat_type: str, uuid: str, appkey: str, 
                     secret: str, authorization: str) -> dict:
    """查询今日饮食统计"""
    base_url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/elderly/static/dailyDietRecord"
    type_map = {
        "eat-count": "/eatCount",
        "eat-time": "/eatTime",
        "drink-count": "/drinkCount",
        "drink-time": "/drinkTime"
    }
    
    url = base_url + type_map.get(stat_type, "")
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        "Content-Type": "application/json",
        "uuid": uuid,
        "appKey": appkey,
        "timeMillis": time_millis,
        "signature": signature,
        "Authorization": authorization
    }
    
    body = {"sn": sn, "user": user, "startTime": start_time, "endTime": end_time}
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def query_week_routine(sn: str, user: str, start_time: int, end_time: int,
                       uuid: str, appkey: str, secret: str, authorization: str) -> dict:
    """查询近七日作息记录"""
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/elderly/static/weekRoutineRecord"
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        "Content-Type": "application/json",
        "uuid": uuid,
        "appKey": appkey,
        "timeMillis": time_millis,
        "signature": signature,
        "Authorization": authorization
    }
    
    body = {"sn": sn, "user": user, "startTime": start_time, "endTime": end_time}
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def query_week_diet(sn: str, user: str, start_time: int, end_time: int,
                    uuid: str, appkey: str, secret: str, authorization: str) -> dict:
    """查询近七日饮食记录"""
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/elderly/static/weekDietRecord"
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        "Content-Type": "application/json",
        "uuid": uuid,
        "appKey": appkey,
        "timeMillis": time_millis,
        "signature": signature,
        "Authorization": authorization
    }
    
    body = {"sn": sn, "user": user, "startTime": start_time, "endTime": end_time}
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def format_daily_result(result: dict, stat_name: str) -> str:
    """格式化单日统计结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    code = result.get("code", 0)
    if code != 2000:
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通老人看护套餐，请登录开放平台绑定套餐卡"
        return f"❌ API 错误码：{code}\n{msg}"
    
    data = result.get("data", 0)
    return f"✅ {stat_name}: {data}"


def format_week_result(result: dict, record_type: str) -> str:
    """格式化周统计结果"""
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
        return "📭 暂无统计数据"
    
    title = "📊 近七日作息记录" if record_type == "routine" else "📊 近七日饮食记录"
    output = [f"{title}\n"]
    
    for record in data:
        day = record.get('day', 'N/A')
        if record_type == "routine":
            walk = record.get('walkTime', 0)
            sit = record.get('sitAndLieTime', 0)
            play = record.get('playTime', 0)
            output.append(f"📅 {day}:")
            output.append(f"   走动：{walk // 60}分钟")
            output.append(f"   坐卧：{sit // 60}分钟")
            output.append(f"   娱乐：{play // 60}分钟")
        else:
            eat = record.get('eatCount', 0)
            drink = record.get('drinkCount', 0)
            output.append(f"📅 {day}:")
            output.append(f"   吃饭：{eat}次")
            output.append(f"   喝水：{drink}次")
        output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="统计数据查询 - 今日统计和近七日统计")
    parser.add_argument("--action", required=True, 
                        choices=["daily-routine", "daily-diet", "week-routine", "week-diet"], 
                        help="操作类型")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token")
    parser.add_argument("--start-time", type=int, required=True, help="开始时间（时间戳秒值）")
    parser.add_argument("--end-time", type=int, required=True, help="结束时间（时间戳秒值）")
    
    # daily-routine 子类型
    parser.add_argument("--routine-type", choices=["walk-count", "walk-time", "sit-count", "sit-time", "play-count", "play-time"],
                        help="作息统计子类型")
    
    # daily-diet 子类型
    parser.add_argument("--diet-type", choices=["eat-count", "eat-time", "drink-count", "drink-time"],
                        help="饮食统计子类型")
    
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细 curl 命令和原始响应（重要查询必须使用）")
    
    args = parser.parse_args()
    
    if args.action == "daily-routine":
        if not args.routine_type:
            print("❌ daily-routine 操作需要指定 --routine-type 参数")
            sys.exit(1)
        
        type_names = {
            "walk-count": "走路次数", "walk-time": "走路时间",
            "sit-count": "坐卧次数", "sit-time": "坐卧时间",
            "play-count": "娱乐次数", "play-time": "娱乐时间"
        }
        result = query_daily_routine(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            stat_type=args.routine_type,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_daily_result(result, type_names[args.routine_type]) if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    elif args.action == "daily-diet":
        if not args.diet_type:
            print("❌ daily-diet 操作需要指定 --diet-type 参数")
            sys.exit(1)
        
        type_names = {
            "eat-count": "吃饭次数", "eat-time": "吃饭时间",
            "drink-count": "喝水次数", "drink-time": "喝水时间"
        }
        result = query_daily_diet(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            stat_type=args.diet_type,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_daily_result(result, type_names[args.diet_type]) if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    elif args.action == "week-routine":
        result = query_week_routine(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_week_result(result, "routine") if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    elif args.action == "week-diet":
        result = query_week_diet(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_week_result(result, "diet") if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    print(output)


if __name__ == "__main__":
    main()
