#!/usr/bin/env python3
"""
值岗计划管理脚本 - 新增、删除、查询值岗计划

支持平台：JF Tech（杰峰）
用法：
    python plan_manager.py --action add --start-time "09:00:00" --end-time "18:00:00" --pri-days 1,2,3,4,5 [其他参数]
    python plan_manager.py --action delete --id 10 [其他参数]
    python plan_manager.py --action list [其他参数]

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


def add_plan(sn: str, user: str, monitor_times: list, pri_days: list,
             uuid: str, appkey: str, secret: str, authorization: str, movecard: int) -> dict:
    """
    添加值岗计划
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        monitor_times: 值岗时间列表 [{"startTime": "09:00:00", "endTime": "18:00:00"}]
        pri_days: 值岗工作日 [1,2,3,4,5]
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        movecard: 移动卡标识
    
    Returns:
        API 响应字典
    """
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/joblover/plan/add"
    
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
        "monitorTimes": monitor_times,
        "config": {"priDays": pri_days}
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


def delete_plan(plan_id: int, uuid: str, appkey: str, secret: str, 
                authorization: str, movecard: int, sn: str = None, user: str = None) -> dict:
    """
    删除值岗计划
    
    Args:
        plan_id: 值岗计划 ID
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        movecard: 移动卡标识
        sn: 设备序列号（可选）
        user: 用户 ID（可选）
    
    Returns:
        API 响应字典
    """
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/joblover/plan/remove"
    
    headers = {
        "Content-Type": "application/json",
        "uuid": uuid,
        "appKey": appkey,
        "timeMillis": time_millis,
        "signature": signature,
        "Authorization": authorization
    }
    
    body = {"id": plan_id}
    if sn:
        body["sn"] = sn
    if user:
        body["user"] = user
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def list_plans(sn: str, user: str, uuid: str, appkey: str, secret: str, 
               authorization: str, movecard: int) -> dict:
    """
    查询值岗计划列表
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        movecard: 移动卡标识
    
    Returns:
        API 响应字典
    """
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/joblover/plan/list"
    
    headers = {
        "Content-Type": "application/json",
        "uuid": uuid,
        "appKey": appkey,
        "timeMillis": time_millis,
        "signature": signature,
        "Authorization": authorization
    }
    
    body = {"sn": sn, "user": user}
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def format_plan_result(result: dict, action: str) -> str:
    """格式化值岗计划操作结果"""
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
    
    if action == "add":
        return "✅ 值岗计划添加成功"
    elif action == "delete":
        return "✅ 值岗计划删除成功"
    elif action == "list":
        data = result.get("data", [])
        if not data:
            return "ℹ️ 暂无值岗计划"
        
        output = f"✅ 共查询到 {len(data)} 个值岗计划\n"
        for plan in data:
            plan_id = plan.get("id", "")
            pri_days = plan.get("config", {}).get("priDays", [])
            monitor_times = plan.get("monitorTimes", [])
            
            day_map = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "日"}
            days_str = ",".join([f"周{day_map.get(d, d)}" for d in pri_days])
            
            times_str = ""
            for t in monitor_times:
                times_str += f"{t.get('startTime', '')}-{t.get('endTime', '')} "
            
            output += f"\n📋 计划 ID: {plan_id}"
            output += f"\n   工作日：{days_str}"
            output += f"\n   时间：{times_str}"
            output += "\n" + "-" * 40
        
        return output
    
    return "✅ 操作成功"


def main():
    parser = argparse.ArgumentParser(description="岗位巡检 - 值岗计划管理")
    parser.add_argument("--action", required=True, choices=["add", "delete", "list"], 
                        help="操作类型：add=添加，delete=删除，list=查询")
    parser.add_argument("--sn", help="设备序列号")
    parser.add_argument("--user", help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token (Authorization)")
    parser.add_argument("--movecard", type=int, default=7, help="移动卡标识（用于签名）")
    parser.add_argument("--start-time", help="开始时间（HH:mm:ss）")
    parser.add_argument("--end-time", help="结束时间（HH:mm:ss）")
    parser.add_argument("--pri-days", help="值岗工作日，逗号分隔（1-7，1=周一）")
    parser.add_argument("--id", type=int, help="值岗计划 ID（delete 操作需要）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    if args.action == "add":
        if not args.start_time or not args.end_time or not args.pri_days:
            print("❌ add 操作需要指定 --start-time、--end-time 和 --pri-days")
            sys.exit(1)
        
        monitor_times = [{"startTime": args.start_time, "endTime": args.end_time}]
        pri_days = [int(d.strip()) for d in args.pri_days.split(",")]
        
        result = add_plan(
            sn=args.sn,
            user=args.user,
            monitor_times=monitor_times,
            pri_days=pri_days,
            uuid=args.uuid,
            appkey=args.appkey,
            secret=args.secret,
            authorization=args.auth,
            movecard=args.movecard
        )
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_plan_result(result, "add"))
    
    elif args.action == "delete":
        if not args.id:
            print("❌ delete 操作需要指定 --id")
            sys.exit(1)
        
        result = delete_plan(
            plan_id=args.id,
            uuid=args.uuid,
            appkey=args.appkey,
            secret=args.secret,
            authorization=args.auth,
            movecard=args.movecard,
            sn=args.sn,
            user=args.user
        )
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_plan_result(result, "delete"))
    
    elif args.action == "list":
        result = list_plans(
            sn=args.sn,
            user=args.user,
            uuid=args.uuid,
            appkey=args.appkey,
            secret=args.secret,
            authorization=args.auth,
            movecard=args.movecard
        )
        
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_plan_result(result, "list"))


if __name__ == "__main__":
    main()
