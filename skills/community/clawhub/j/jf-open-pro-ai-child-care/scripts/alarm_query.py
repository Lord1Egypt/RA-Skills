#!/usr/bin/env python3
"""
告警查询脚本 - 查询异常告警列表

支持平台：JF Tech（杰峰）
用法：
    python alarm_query.py --action list --sn <序列号> --user <用户 ID> --uuid <uuid> --appkey <appKey> --secret <secret> --auth <authorization> --movecard <moveCard> --msg-type <类型> --start-time <开始时间> --end-time <结束时间> --page <页码> --rows <条数>

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


def query_alarms(sn: str, user: str, start_time: str, end_time: str,
                 msg_type: str, page: int, rows: int,
                 uuid: str, appkey: str, secret: str, authorization: str, movecard: int) -> dict:
    """
    查询异常告警列表
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        start_time: 开始时间（秒值）
        end_time: 结束时间（秒值）
        msg_type: 告警类型
        page: 页码
        rows: 每页条数
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
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/child/alarm/page"
    
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
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


# 告警类型映射
MSG_TYPE_MAP = {
    "VehicleParking": "可疑车辆停留",
    "PIRAlarm": "可疑人员徘徊",
    "NonMotorVehicleParking": "非机动车停留",
    "FireDetection": "明火检测"
}


def format_alarm_result(result: dict) -> str:
    """格式化告警列表结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    code = result.get("code", 0)
    if code != 2000:
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通儿童看护套餐，请登录开放平台绑定套餐卡"
        return f"❌ API 错误码：{code}\n{msg}"
    
    data = result.get("data", {})
    records = data.get("records", [])
    total = data.get("total", 0)
    
    if not records:
        return "📭 未找到告警记录"
    
    output = [f"✅ 共 {total} 条告警记录（显示 {len(records)} 条）\n"]
    
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


def main():
    parser = argparse.ArgumentParser(description="告警查询 - 儿童看护告警列表")
    parser.add_argument("--action", required=True, choices=["list"], 
                        help="操作类型")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token")
    parser.add_argument("--movecard", type=int, required=True, help="移动卡标识")
    parser.add_argument("--msg-type", required=True, 
                        choices=["VehicleParking", "PIRAlarm", "NonMotorVehicleParking", "FireDetection"],
                        help="告警类型")
    parser.add_argument("--start-time", required=True, help="开始时间（时间戳秒值）")
    parser.add_argument("--end-time", required=True, help="结束时间（时间戳秒值）")
    parser.add_argument("--page", type=int, default=1, help="页码")
    parser.add_argument("--rows", type=int, default=10, help="每页条数")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细 curl 命令和原始响应（重要查询必须使用）")
    
    args = parser.parse_args()
    
    if args.action == "list":
        result = query_alarms(
            sn=args.sn, user=args.user,
            start_time=args.start_time, end_time=args.end_time,
            msg_type=args.msg_type,
            page=args.page, rows=args.rows,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth,
            movecard=args.movecard
        )
        
        if args.json:
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            msg_type_name = MSG_TYPE_MAP.get(args.msg_type, args.msg_type)
            header = f"📋 {msg_type_name} 告警查询\n\n"
            output = header + format_alarm_result(result)
    
    print(output)


if __name__ == "__main__":
    main()
