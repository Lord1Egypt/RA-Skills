#!/usr/bin/env python3
"""
陌生人管理脚本 - 添加/移除陌生人到人形库

支持平台：JF Tech（杰峰）
用法：
    python stranger_manager.py --action add --sn <序列号> --user <用户 ID> --alarm-id <报警 ID> --uuid <uuid> --appkey <appKey> --secret <secret> --auth <authorization> --movecard <moveCard> [--image <图片 URL>]
    python stranger_manager.py --action remove --sn <序列号> --user <用户 ID> --alarm-id <报警 ID> --uuid <uuid> --appkey <appKey> --secret <secret> --auth <authorization> --movecard <moveCard>

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


def add_stranger(sn: str, user: str, alarm_id: str, uuid: str, appkey: str, 
                 secret: str, authorization: str, movecard: int, image: str = None) -> dict:
    """
    添加陌生人到人形库
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        alarm_id: 报警 ID
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        movecard: 移动卡标识
        image: 报警图片 URL（可选）
    
    Returns:
        API 响应字典
    """
    # 使用杰峰官方签名算法生成 timeMillis 和 signature
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/child/stranger/add"
    
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
        "alarmId": alarm_id
    }
    
    if image:
        body["image"] = image
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def remove_stranger(sn: str, user: str, alarm_id: str, uuid: str, appkey: str, 
                    secret: str, authorization: str, movecard: int) -> dict:
    """
    从人形库移除陌生人
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        alarm_id: 报警 ID
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
    
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/child/stranger/remove"
    
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
        "alarmId": alarm_id
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


def format_result(result: dict, action: str) -> str:
    """格式化结果输出"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    code = result.get("code", 0)
    if code != 2000:
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通儿童看护套餐，请登录开放平台绑定套餐卡"
        return f"❌ API 错误码：{code}\n{msg}"
    
    data = result.get("data", False)
    
    if action == "add":
        if data:
            return "✅ 陌生人已添加到人形库"
        else:
            return "⚠️ 添加失败"
    else:
        if data:
            return "✅ 陌生人已从人形库移除"
        else:
            return "⚠️ 移除失败"


def main():
    parser = argparse.ArgumentParser(description="陌生人管理 - 添加/移除陌生人到人形库")
    parser.add_argument("--action", required=True, choices=["add", "remove"], 
                        help="操作类型")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token")
    parser.add_argument("--movecard", type=int, required=True, help="移动卡标识")
    parser.add_argument("--alarm-id", required=True, help="报警 ID")
    parser.add_argument("--image", help="报警图片 URL（add 操作可选）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细 curl 命令和原始响应（重要查询必须使用）")
    
    args = parser.parse_args()
    
    if args.action == "add":
        result = add_stranger(
            sn=args.sn, user=args.user, alarm_id=args.alarm_id, image=args.image,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth,
            movecard=args.movecard
        )
        output = format_result(result, "add") if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    elif args.action == "remove":
        result = remove_stranger(
            sn=args.sn, user=args.user, alarm_id=args.alarm_id,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth,
            movecard=args.movecard
        )
        output = format_result(result, "remove") if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    print(output)


if __name__ == "__main__":
    main()
