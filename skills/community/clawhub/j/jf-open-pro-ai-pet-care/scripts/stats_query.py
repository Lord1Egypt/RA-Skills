#!/usr/bin/env python3
"""
统计数据查询脚本 - 查询宠物行为次数、时间、数据图表

支持平台：JF Tech（杰峰）
用法：
    python stats_query.py --action count --type eating --start-time <时间戳> --end-time <时间戳> [其他参数]
    python stats_query.py --action time --type walking [其他参数]
    python stats_query.py --action day-chart --type eating [其他参数]
    python stats_query.py --action week-chart --type lying [其他参数]
"""

import argparse
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 导入杰峰签名工具
from jf_signature import generate_signature



def query_count(sn: str, user: str, start_time: str, end_time: str, 
                behavior_type: str, uuid: str, appkey: str, 
                secret: str, authorization: str, custom_id: str = None) -> dict:
    """
    查询宠物行为的次数
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        start_time: 开始时间（时间戳秒值）
        end_time: 结束时间（时间戳秒值）
        behavior_type: 行为类型（eating/walking/lying）
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        custom_id: 自定义 ID（可选）
    
    Returns:
        API 响应字典
    """
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet/static/queryCount"
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
        "startTime": str(start_time),
        "endTime": str(end_time),
        "type": behavior_type
    }
    
    if custom_id:
        body["customId"] = custom_id
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def query_time(sn: str, user: str, start_time: str, end_time: str, 
               behavior_type: str, uuid: str, appkey: str, 
               secret: str, authorization: str, custom_id: str = None) -> dict:
    """
    查询宠物行为的时间
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        start_time: 开始时间（时间戳秒值）
        end_time: 结束时间（时间戳秒值）
        behavior_type: 行为类型（eating/walking/lying）
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        custom_id: 自定义 ID（可选）
    
    Returns:
        API 响应字典
    """
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet/static/queryTime"
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
        "startTime": str(start_time),
        "endTime": str(end_time),
        "type": behavior_type
    }
    
    if custom_id:
        body["customId"] = custom_id
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def query_day_chart(sn: str, user: str, start_time: str, end_time: str, 
                    behavior_type: str, uuid: str, appkey: str, 
                    secret: str, authorization: str, custom_id: str = None,
                    dimension: str = "count") -> dict:
    """
    获取当日数据图
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        start_time: 开始时间（时间戳秒值）
        end_time: 结束时间（时间戳秒值）
        behavior_type: 行为类型（eating/walking/lying）
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        custom_id: 自定义 ID（可选）
        dimension: 统计维度（count=time 查询次数，time=查询时间）
    
    Returns:
        API 响应字典
    """
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet/static/queryDayChart"
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
        "startTime": str(start_time),
        "endTime": str(end_time),
        "type": behavior_type,
        "staticDimension": dimension
    }
    
    if custom_id:
        body["customId"] = custom_id
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def query_week_chart(sn: str, user: str, start_time: str, end_time: str, 
                     behavior_type: str, uuid: str, appkey: str, 
                     secret: str, authorization: str, custom_id: str = None,
                     dimension: str = "count") -> dict:
    """
    获取一周数据图
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        start_time: 开始时间（时间戳秒值）
        end_time: 结束时间（时间戳秒值）
        behavior_type: 行为类型（eating/walking/lying）
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        custom_id: 自定义 ID（可选）
        dimension: 统计维度（count=time 查询次数，time=查询时间）
    
    Returns:
        API 响应字典
    """
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet/static/queryWeekChart"
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
        "startTime": str(start_time),
        "endTime": str(end_time),
        "type": behavior_type,
        "staticDimension": dimension
    }
    
    if custom_id:
        body["customId"] = custom_id
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


BEHAVIOR_TYPE_MAP = {
    "eating": "吃喝",
    "walking": "走动",
    "lying": "躺着"
}


def format_count_result(result: dict, behavior_type: str) -> str:
    """格式化次数查询结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    if result.get("code") != 2000:
        return f"❌ API 错误码：{result.get('code')}\n{result.get('msg', '')}"
    
    data = result.get("data", 0)
    behavior_name = BEHAVIOR_TYPE_MAP.get(behavior_type, behavior_type)
    
    return f"✅ {behavior_name}行为次数：{data} 次"


def format_time_result(result: dict, behavior_type: str) -> str:
    """格式化时间查询结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    if result.get("code") != 2000:
        return f"❌ API 错误码：{result.get('code')}\n{result.get('msg', '')}"
    
    data = result.get("data", 0)
    behavior_name = BEHAVIOR_TYPE_MAP.get(behavior_type, behavior_type)
    
    minutes = data // 60
    seconds = data % 60
    
    return f"✅ {behavior_name}行为时长：{minutes}分{seconds}秒 ({data}秒)"


def format_chart_result(result: dict, chart_type: str, behavior_type: str) -> str:
    """格式化图表数据结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    if result.get("code") != 2000:
        return f"❌ API 错误码：{result.get('code')}\n{result.get('msg', '')}"
    
    data = result.get("data", [])
    behavior_name = BEHAVIOR_TYPE_MAP.get(behavior_type, behavior_type)
    chart_name = "当日" if chart_type == "day" else "一周"
    
    if not data:
        return f"📭 {chart_name}{behavior_name}数据：暂无数据"
    
    output = []
    output.append(f"📊 {chart_name}{behavior_name}数据（共 {len(data)} 个时间点）\n")
    
    # 只显示前 10 个数据点，避免输出过长
    display_data = data[:10]
    for item in display_data:
        key = item.get('key', 'N/A')
        value = item.get('value', 0)
        output.append(f"   {key}: {value}")
    
    if len(data) > 10:
        output.append(f"   ... 还有 {len(data) - 10} 个数据点")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="统计数据查询 - 宠物行为统计")
    parser.add_argument("--action", required=True, 
                        choices=["count", "time", "day-chart", "week-chart"], 
                        help="操作类型")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token")
    parser.add_argument("--start-time", help="开始时间（时间戳秒值）")
    parser.add_argument("--end-time", help="结束时间（时间戳秒值）")
    parser.add_argument("--type", required=True, choices=["eating", "walking", "lying"],
                        help="行为类型")
    parser.add_argument("--custom-id", help="自定义 ID")
    parser.add_argument("--dimension", choices=["count", "time"], default="count",
                        help="统计维度（chart 操作）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细 curl 命令和原始响应（重要查询必须使用）")
    
    args = parser.parse_args()
    
    # 验证必需参数
    if args.action in ["count", "time"]:
        if not args.start_time or not args.end_time:
            print("❌ 此操作需要指定 --start-time 和 --end-time 参数")
            sys.exit(1)
    elif args.action in ["day-chart", "week-chart"]:
        if not args.start_time or not args.end_time:
            print("❌ 此操作需要指定 --start-time 和 --end-time 参数")
            sys.exit(1)
    
    if args.action == "count":
        result = query_count(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            behavior_type=args.type, custom_id=args.custom_id,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        
        if args.json:
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = format_count_result(result, args.type)
    
    elif args.action == "time":
        result = query_time(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            behavior_type=args.type, custom_id=args.custom_id,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        
        if args.json:
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = format_time_result(result, args.type)
    
    elif args.action == "day-chart":
        result = query_day_chart(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            behavior_type=args.type, custom_id=args.custom_id,
            dimension=args.dimension,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        
        if args.json:
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = format_chart_result(result, "day", args.type)
    
    elif args.action == "week-chart":
        result = query_week_chart(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            behavior_type=args.type, custom_id=args.custom_id,
            dimension=args.dimension,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        
        if args.json:
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = format_chart_result(result, "week", args.type)
    
    else:
        print(f"❌ 未知操作：{args.action}")
        sys.exit(1)
    
    print(output)


if __name__ == "__main__":
    main()
