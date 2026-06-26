#!/usr/bin/env python3
"""
统计数据查询脚本 - 查询行为统计和七日图表

支持平台：JF Tech（杰峰）
用法：
    python stats_query.py --action count --sn <序列号> --user <用户 ID> --uuid <uuid> --appkey <appKey> --secret <secret> --auth <authorization> --movecard <moveCard> --type <行为类型> --start-time <开始时间> --end-time <结束时间>
    python stats_query.py --action time --sn <序列号> --user <用户 ID> --uuid <uuid> --appkey <appKey> --secret <secret> --auth <authorization> --movecard <moveCard> --type <行为类型> --start-time <开始时间> --end-time <结束时间>
    python stats_query.py --action week-chart --sn <序列号> --user <用户 ID> --uuid <uuid> --appkey <appKey> --secret <secret> --auth <authorization> --movecard <moveCard> --type <行为类型> --start-time <开始时间> --end-time <结束时间>

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


def query_count(sn: str, user: str, start_time: str, end_time: str,
                behavior_type: str, uuid: str, appkey: str, 
                secret: str, authorization: str, movecard: int) -> dict:
    """
    查询行为次数
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        start_time: 开始时间（秒值）
        end_time: 结束时间（秒值）
        behavior_type: 行为类型
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
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/child/static/queryCount"
    
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
               secret: str, authorization: str, movecard: int) -> dict:
    """
    查询行为时间
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        start_time: 开始时间（秒值）
        end_time: 结束时间（秒值）
        behavior_type: 行为类型
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
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/child/static/queryTime"
    
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
                     secret: str, authorization: str, movecard: int) -> dict:
    """
    查询七日行为时间图表
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        start_time: 开始时间（秒值）
        end_time: 结束时间（秒值）
        behavior_type: 行为类型
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
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/child/static/queryTimeForChart"
    
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
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


# 行为类型映射
BEHAVIOR_TYPE_MAP = {
    "studying": "学习",
    "playing": "娱乐",
    "eating": "吃喝",
    "walking": "走动",
    "sitting": "坐卧"
}


def format_count_result(result: dict, behavior_type: str) -> str:
    """格式化次数查询结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    code = result.get("code", 0)
    if code != 2000:
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通儿童看护套餐，请登录开放平台绑定套餐卡"
        return f"❌ API 错误码：{code}\n{msg}"
    
    data = result.get("data", 0)
    behavior_name = BEHAVIOR_TYPE_MAP.get(behavior_type, behavior_type)
    
    return f"✅ {behavior_name}次数：{data} 次"


def format_time_result(result: dict, behavior_type: str) -> str:
    """格式化时间查询结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    code = result.get("code", 0)
    if code != 2000:
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通儿童看护套餐，请登录开放平台绑定套餐卡"
        return f"❌ API 错误码：{code}\n{msg}"
    
    data = result.get("data", 0)
    behavior_name = BEHAVIOR_TYPE_MAP.get(behavior_type, behavior_type)
    
    minutes = data // 60
    seconds = data % 60
    
    return f"✅ {behavior_name}时长：{minutes}分{seconds}秒 ({data}秒)"


def format_chart_result(result: dict) -> str:
    """格式化图表结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    code = result.get("code", 0)
    if code != 2000:
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通儿童看护套餐，请登录开放平台绑定套餐卡"
        return f"❌ API 错误码：{code}\n{msg}"
    
    data = result.get("data", [])
    
    if not data:
        return "📭 暂无统计数据"
    
    output = [f"📊 近七日行为统计（共 {len(data)} 天）\n"]
    
    for item in data:
        static_date = item.get('staticDate', item.get('staticTime', 'N/A'))
        value = item.get('value', item.get('time', 0))
        minutes = value // 60
        output.append(f"   {static_date}: {minutes}分钟")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="统计数据查询 - 儿童看护行为统计")
    parser.add_argument("--action", required=True, 
                        choices=["count", "time", "week-chart"], 
                        help="操作类型")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token")
    parser.add_argument("--movecard", type=int, required=True, help="移动卡标识")
    parser.add_argument("--start-time", required=True, help="开始时间（时间戳秒值）")
    parser.add_argument("--end-time", required=True, help="结束时间（时间戳秒值）")
    parser.add_argument("--type", required=True, 
                        choices=["studying", "playing", "eating", "walking", "sitting"],
                        help="行为类型")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细 curl 命令和原始响应（重要查询必须使用）")
    
    args = parser.parse_args()
    
    if args.action == "count":
        result = query_count(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            behavior_type=args.type,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth,
            movecard=args.movecard
        )
        output = format_count_result(result, args.type) if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    elif args.action == "time":
        result = query_time(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            behavior_type=args.type,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth,
            movecard=args.movecard
        )
        output = format_time_result(result, args.type) if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    elif args.action == "week-chart":
        result = query_week_chart(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            behavior_type=args.type,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth,
            movecard=args.movecard
        )
        output = format_chart_result(result) if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    print(output)


if __name__ == "__main__":
    main()
