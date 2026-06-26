#!/usr/bin/env python3
"""
异常告警查询脚本 - 查询岗位巡检异常告警列表

支持平台：JF Tech（杰峰）
用法：
    python alarm_query.py --action list --msg-type <类型> --start-time <时间戳> --end-time <时间戳> [其他参数]

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
        start_time: 开始时间（时间戳秒值）
        end_time: 结束时间（时间戳秒值）
        msg_type: 异常类型
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
        "startTime": start_time,
        "endTime": end_time,
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


def format_alarm_result(result: dict) -> str:
    """格式化告警查询结果"""
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
    total = data.get("total", 0)
    records = data.get("records", [])
    
    output = f"✅ 共查询到 {total} 条告警记录\n"
    
    if not records:
        output += "\n暂无告警记录"
        return output
    
    for record in records[:10]:  # 只显示前 10 条
        alarm_id = record.get("alarmId", "")
        alarm_time = record.get("alarmTime", "")
        pic_url = record.get("picUrl", "")
        sn = record.get("sn", "")
        
        output += f"\n📋 告警 ID: {alarm_id}"
        output += f"\n   时间：{alarm_time}"
        output += f"\n   设备：{sn}"
        if pic_url:
            output += f"\n   图片：{pic_url}"
        output += "\n" + "-" * 40
    
    return output


def main():
    parser = argparse.ArgumentParser(description="岗位巡检 - 异常告警查询")
    parser.add_argument("--action", required=True, choices=["list"], 
                        help="操作类型：list=查询告警列表")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token (Authorization)")
    parser.add_argument("--movecard", type=int, default=7, help="移动卡标识（用于签名）")
    parser.add_argument("--msg-type", required=True, 
                        help="异常类型：StaffOffDuty=离岗，PlayPhoneOnDuty=玩手机，SleepOnDuty=睡觉，SmokeOnDuty=抽烟")
    parser.add_argument("--start-time", required=True, help="开始时间（秒级时间戳）")
    parser.add_argument("--end-time", required=True, help="结束时间（秒级时间戳）")
    parser.add_argument("--page", type=int, default=1, help="页码")
    parser.add_argument("--rows", type=int, default=10, help="每页条数")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    result = query_alarms(
        sn=args.sn,
        user=args.user,
        start_time=args.start_time,
        end_time=args.end_time,
        msg_type=args.msg_type,
        page=args.page,
        rows=args.rows,
        uuid=args.uuid,
        appkey=args.appkey,
        secret=args.secret,
        authorization=args.auth,
        movecard=args.movecard
    )
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_alarm_result(result))


if __name__ == "__main__":
    main()
