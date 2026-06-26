#!/usr/bin/env python3
"""
统计数据查询脚本 - 查询行为统计和存在统计数据

支持平台：JF Tech（杰峰）
"""

import argparse
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 导入杰峰签名工具
from jf_signature import generate_signature



def query_behavior_count(sn: str, user: str, start_time: str, end_time: str,
                         behavior_type: str, uuid: str, appkey: str, 
                         secret: str, authorization: str, face_id: str = None) -> dict:
    """查询行为总次数（进入/离开）"""
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/indoor/static/behavior/count"
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
    
    if face_id:
        body["faceSampleId"] = face_id
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def query_behavior_chart(sn: str, user: str, start_time: str, end_time: str,
                         behavior_type: str, chart_type: str, uuid: str, appkey: str, 
                         secret: str, authorization: str, face_id: str = None) -> dict:
    """查询行为图表（日/周）"""
    if chart_type == "day":
        url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/indoor/static/behavior/dayDataChart"
    else:
        url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/indoor/static/behavior/weekDataChart"
    
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
    
    if face_id:
        body["faceSampleId"] = face_id
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def query_exist_count(sn: str, user: str, start_time: str, end_time: str,
                      exist_type: str, uuid: str, appkey: str, 
                      secret: str, authorization: str, face_id: str = None) -> dict:
    """查询存在统计（最大人数/存在时长）"""
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/indoor/static/exist/count"
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
        "type": exist_type
    }
    
    if face_id:
        body["faceSampleId"] = face_id
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def query_exist_chart(sn: str, user: str, start_time: str, end_time: str,
                      exist_type: str, chart_type: str, uuid: str, appkey: str, 
                      secret: str, authorization: str, face_id: str = None) -> dict:
    """查询存在图表（日/周）"""
    if chart_type == "day":
        url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/indoor/static/exist/dayDataChart"
    else:
        url = "https://api-cn.jftechws.com/aisvr/v2/gateway/api/indoor/static/exist/weekDataChart"
    
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
        "type": exist_type
    }
    
    if face_id:
        body["faceSampleId"] = face_id
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


# 类型映射
BEHAVIOR_TYPE_MAP = {
    "SomeoneEntered": "进入",
    "SomeoneLeft": "离开"
}

EXIST_TYPE_MAP = {
    "MaxPersonCount": "最大人数",
    "ExistTime": "存在时长"
}


def format_count_result(result: dict, stat_name: str) -> str:
    """格式化次数/数值结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    code = result.get("code", 0)
    if code != 2000:
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通室内安防套餐，请登录开放平台绑定套餐卡"
        return f"❌ API 错误码：{code}\n{msg}"
    
    data = result.get("data", 0)
    return f"✅ {stat_name}: {data}"


def format_chart_result(result: dict, chart_name: str) -> str:
    """格式化图表结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    code = result.get("code", 0)
    if code != 2000:
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通室内安防套餐，请登录开放平台绑定套餐卡"
        return f"❌ API 错误码：{code}\n{msg}"
    
    data = result.get("data", [])
    
    if not data:
        return f"📭 {chart_name}：暂无数据"
    
    output = [f"📊 {chart_name}（共 {len(data)} 个数据点）\n"]
    
    for item in data[:10]:
        key = item.get('key', 'N/A')
        count = item.get('count', 0)
        output.append(f"   {key}: {count}")
    
    if len(data) > 10:
        output.append(f"   ... 还有 {len(data) - 10} 个数据点")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="统计数据查询 - 室内安防统计")
    parser.add_argument("--action", required=True, 
                        choices=["behavior-count", "behavior-chart", "exist-count", "exist-chart"], 
                        help="操作类型")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token")
    parser.add_argument("--start-time", required=True, help="开始时间（时间戳秒值）")
    parser.add_argument("--end-time", required=True, help="结束时间（时间戳秒值）")
    parser.add_argument("--face-id", help="成员 ID（可选）")
    
    # behavior 相关参数
    parser.add_argument("--type", help="类型（SomeoneEntered/SomethingLeft 或 MaxPersonCount/ExistTime）")
    
    # chart 相关参数
    parser.add_argument("--chart-type", choices=["day", "week"], help="图表类型（day/week）")
    
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细 curl 命令和原始响应（重要查询必须使用）")
    
    args = parser.parse_args()
    
    if args.action == "behavior-count":
        if not args.type or args.type not in ["SomeoneEntered", "SomeoneLeft"]:
            print("❌ behavior-count 需要指定 --type (SomeoneEntered/SomeoneLeft)")
            sys.exit(1)
        
        type_name = BEHAVIOR_TYPE_MAP.get(args.type, args.type)
        result = query_behavior_count(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            behavior_type=args.type, face_id=args.face_id,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_count_result(result, f"{type_name}次数") if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    elif args.action == "behavior-chart":
        if not args.type or args.type not in ["SomeoneEntered", "SomeoneLeft"]:
            print("❌ behavior-chart 需要指定 --type (SomeoneEntered/SomeoneLeft)")
            sys.exit(1)
        if not args.chart_type:
            print("❌ behavior-chart 需要指定 --chart-type (day/week)")
            sys.exit(1)
        
        type_name = BEHAVIOR_TYPE_MAP.get(args.type, args.type)
        chart_name = "当日" if args.chart_type == "day" else "近七日"
        result = query_behavior_chart(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            behavior_type=args.type, chart_type=args.chart_type, face_id=args.face_id,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_chart_result(result, f"{chart_name}{type_name}图表") if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    elif args.action == "exist-count":
        if not args.type or args.type not in ["MaxPersonCount", "ExistTime"]:
            print("❌ exist-count 需要指定 --type (MaxPersonCount/ExistTime)")
            sys.exit(1)
        
        type_name = EXIST_TYPE_MAP.get(args.type, args.type)
        result = query_exist_count(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            exist_type=args.type, face_id=args.face_id,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_count_result(result, type_name) if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    elif args.action == "exist-chart":
        if not args.type or args.type not in ["MaxPersonCount", "ExistTime"]:
            print("❌ exist-chart 需要指定 --type (MaxPersonCount/ExistTime)")
            sys.exit(1)
        if not args.chart_type:
            print("❌ exist-chart 需要指定 --chart-type (day/week)")
            sys.exit(1)
        
        type_name = EXIST_TYPE_MAP.get(args.type, args.type)
        chart_name = "当日" if args.chart_type == "day" else "近七日"
        result = query_exist_chart(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            exist_type=args.type, chart_type=args.chart_type, face_id=args.face_id,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_chart_result(result, f"{chart_name}{type_name}图表") if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    print(output)


if __name__ == "__main__":
    main()
