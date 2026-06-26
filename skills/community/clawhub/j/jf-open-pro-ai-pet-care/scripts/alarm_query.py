#!/usr/bin/env python3
"""
异常告警查询脚本 - 查询异常提醒告警列表和设置

支持平台：JF Tech（杰峰）
用法：
    python alarm_query.py --action list --start-time <时间戳> --end-time <时间戳> [其他参数]
    python alarm_query.py --action config --sn <序列号> --user <用户 ID> [其他参数]
    python alarm_query.py --action set-config --msg-type <类型> --enable 1 [其他参数]
"""

import argparse
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 导入杰峰签名工具
from jf_signature import generate_signature



def query_alarms(sn: str, user: str, start_time: str, end_time: str,
                 uuid: str, appkey: str, secret: str, authorization: str,
                 msg_type: str = "", page: int = 1, rows: int = 10,
                 msg_type_list: list = None) -> dict:
    """
    查询异常提醒告警列表
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        start_time: 开始时间（时间戳秒值）
        end_time: 结束时间（时间戳秒值）
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        msg_type: 异常类型（可选）
        page: 页号
        rows: 每页条数
        msg_type_list: 异常类型集合（可选）
    
    Returns:
        API 响应字典
    """
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet/alarm/page"
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
        "msgType": msg_type,
        "page": page,
        "rows": rows
    }
    
    if msg_type_list:
        body["msgTypeList"] = msg_type_list
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def get_alarm_config(sn: str, user: str, uuid: str, appkey: str, 
                     secret: str, authorization: str, movecard: int) -> dict:
    """
    查询用户异常提醒设置项
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
    
    Returns:
        API 响应字典
    """
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet/abnormalAlarmConfig/list"
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
        "user": user
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


def set_alarm_config(sn: str, user: str, msg_type: str, uuid: str, appkey: str, 
                     secret: str, authorization: str, enable: int = None,
                     call_remind: int = None, app_remind: int = None,
                     long_time_threshold: int = None) -> dict:
    """
    更新用户异常提醒设置项
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        msg_type: 异常类型
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        enable: 是否启用提醒 (0 否，1 是)
        call_remind: 是否开启电话提醒 (0 关闭，1 开启)
        app_remind: 手机提醒是否开启 (0 关闭，1 开启)
        long_time_threshold: 久未出现时间阀值 (单位 s)
    
    Returns:
        API 响应字典
    """
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet/abnormalAlarmConfig/save"
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
        "msgType": msg_type
    }
    
    if enable is not None:
        body["enable"] = enable
    if call_remind is not None:
        body["callRemind"] = call_remind
    if app_remind is not None:
        body["appRemind"] = app_remind
    
    if long_time_threshold is not None:
        body["config"] = {
            "longTimeDisappearThreshold": long_time_threshold
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


MSG_TYPE_MAP = {
    "GrainBloack": "卡粮",
    "PetAppetiteAbnormal": "食量异常",
    "WaitFeeding": "等待投喂",
    "PetAbsent": "宠物久未出现"
}


def format_alarm_list_result(result: dict) -> str:
    """格式化告警列表结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    if result.get("code") != 2000:
        return f"❌ API 错误码：{result.get('code')}\n{result.get('msg', '')}"
    
    data = result.get("data", {})
    records = data.get("records", [])
    total = data.get("total", 0)
    
    if not records:
        return "📭 未找到告警记录"
    
    output = []
    output.append(f"✅ 共 {total} 条告警记录（显示 {len(records)} 条）\n")
    
    for i, alarm in enumerate(records, 1):
        output.append(f"🚨 告警 {i}:")
        output.append(f"   告警 ID: {alarm.get('alarmId', 'N/A')}")
        output.append(f"   设备：{alarm.get('sn', 'N/A')}")
        output.append(f"   时间：{alarm.get('alarmTime', 'N/A')}")
        if alarm.get('picUrl'):
            output.append(f"   图片：有")
        if alarm.get('videoUrl'):
            output.append(f"   视频：有")
        output.append("")
    
    return "\n".join(output)


def format_config_result(result: dict) -> str:
    """格式化配置查询结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    if result.get("code") != 2000:
        return f"❌ API 错误码：{result.get('code')}\n{result.get('msg', '')}"
    
    data = result.get("data", [])
    
    if not data:
        return "📭 暂无配置"
    
    output = []
    output.append("✅ 异常提醒设置\n")
    
    for config in data:
        msg_type = config.get('msgType', 'Unknown')
        msg_name = MSG_TYPE_MAP.get(msg_type, msg_type)
        enable = config.get('enable', 0)
        call_remind = config.get('callRemind', 0)
        app_remind = config.get('appRemind', 0)
        
        output.append(f"📋 {msg_name} ({msg_type}):")
        output.append(f"   启用状态：{'✅ 开启' if enable else '⏸️ 关闭'}")
        output.append(f"   电话提醒：{'✅ 开启' if call_remind else '⏸️ 关闭'}")
        output.append(f"   手机提醒：{'✅ 开启' if app_remind else '⏸️ 关闭'}")
        
        cfg = config.get('config', {})
        if cfg and cfg.get('longTimeDisappearThreshold'):
            threshold = cfg['longTimeDisappearThreshold']
            output.append(f"   久未出现阈值：{threshold}秒 ({threshold // 60}分钟)")
        output.append("")
    
    return "\n".join(output)


def format_set_config_result(result: dict) -> str:
    """格式化配置设置结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    if result.get("code") != 2000:
        return f"❌ API 错误码：{result.get('code')}\n{result.get('msg', '')}"
    
    return "✅ 配置更新成功"


def main():
    parser = argparse.ArgumentParser(description="异常告警查询 - 查询告警列表和提醒设置")
    parser.add_argument("--action", required=True, 
                        choices=["list", "config", "set-config"], 
                        help="操作类型")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token")
    
    # list 操作参数
    parser.add_argument("--start-time", help="开始时间（时间戳秒值）")
    parser.add_argument("--end-time", help="结束时间（时间戳秒值）")
    parser.add_argument("--msg-type", help="异常类型（GrainBloack/PetAppetiteAbnormal/WaitFeeding/PetAbsent）")
    parser.add_argument("--page", type=int, default=1, help="页号")
    parser.add_argument("--rows", type=int, default=10, help="每页条数")
    
    # set-config 操作参数
    parser.add_argument("--enable", type=int, choices=[0, 1], help="是否启用提醒")
    parser.add_argument("--call-remind", type=int, choices=[0, 1], help="是否开启电话提醒")
    parser.add_argument("--app-remind", type=int, choices=[0, 1], help="是否开启手机提醒")
    parser.add_argument("--threshold", type=int, help="久未出现时间阀值（秒）")
    
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细 curl 命令和原始响应（重要查询必须使用）")
    
    args = parser.parse_args()
    
    if args.action == "list":
        if not args.start_time or not args.end_time:
            print("❌ list 操作需要指定 --start-time 和 --end-time 参数")
            sys.exit(1)
        
        result = query_alarms(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            msg_type=args.msg_type or "",
            page=args.page, rows=args.rows,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        
        if args.json:
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = format_alarm_list_result(result)
    
    elif args.action == "config":
        result = get_alarm_config(
            sn=args.sn, user=args.user,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        
        if args.json:
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = format_config_result(result)
    
    elif args.action == "set-config":
        if not args.msg_type:
            print("❌ set-config 操作需要指定 --msg-type 参数")
            sys.exit(1)
        
        result = set_alarm_config(
            sn=args.sn, user=args.user, msg_type=args.msg_type,
            enable=args.enable, call_remind=args.call_remind, 
            app_remind=args.app_remind, long_time_threshold=args.threshold,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        
        if args.json:
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = format_set_config_result(result)
    
    else:
        print(f"❌ 未知操作：{args.action}")
        sys.exit(1)
    
    print(output)


if __name__ == "__main__":
    main()
