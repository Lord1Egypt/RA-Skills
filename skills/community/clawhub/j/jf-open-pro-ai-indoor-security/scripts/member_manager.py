#!/usr/bin/env python3
"""
成员管理脚本 - 新增、删除、修改、查询成员

支持平台：JF Tech（杰峰）
"""

import argparse
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 导入杰峰签名工具
from jf_signature import generate_signature



def add_member(sn: str, user: str, name: str, pictures: list, uuid: str, appkey: str, 
               secret: str, authorization: str, avatar: str = None, notice: int = 1) -> dict:
    """新增成员"""
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/indoor/face/sample/add"
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
        "faceSampleName": name,
        "pictureList": pictures,
        "notice": notice
    }
    
    if avatar:
        body["avatar"] = avatar
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def delete_member(sn: str, user: str, member_id: int, uuid: str, appkey: str, 
                  secret: str, authorization: str) -> dict:
    """删除成员"""
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/indoor/face/sample/delete"
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        "Content-Type": "application/json",
        "uuid": uuid,
        "appKey": appkey,
        "timeMillis": time_millis,
        "signature": signature,
        "Authorization": authorization
    }
    
    body = {"sn": sn, "user": user, "faceSampleId": member_id}
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def update_member(sn: str, user: str, member_id: int, name: str, pictures: list,
                  uuid: str, appkey: str, secret: str, authorization: str,
                  avatar: str = None, notice: int = None) -> dict:
    """修改成员"""
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/indoor/face/sample/update"
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
        "id": member_id,
        "faceSampleName": name,
        "pictureList": pictures
    }
    
    if avatar:
        body["avatar"] = avatar
    if notice is not None:
        body["notice"] = notice
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def list_members(sn: str, user: str, uuid: str, appkey: str, 
                 secret: str, authorization: str, movecard: int, member_id: int = None,
                 notice: int = None, static_flag: int = None) -> dict:
    """查询成员列表"""
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/indoor/face/sample/list"
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        "Content-Type": "application/json",
        "uuid": uuid,
        "appKey": appkey,
        "timeMillis": time_millis,
        "signature": signature,
        "Authorization": authorization
    }
    
    body = {"sn": sn, "user": user}
    
    if member_id is not None:
        body["faceSampleId"] = member_id
    if notice is not None:
        body["notice"] = notice
    if static_flag is not None:
        body["staticFlag"] = static_flag
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def format_member_result(result: dict, action: str) -> str:
    """格式化成员操作结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    code = result.get("code", 0)
    if code != 2000:
        msg = result.get('msg', '')
        if code == 12504:
            return f"❌ API 错误码：{code}\n{msg}\n\n💡 设备未开通室内安防套餐，请登录开放平台绑定套餐卡"
        return f"❌ API 错误码：{code}\n{msg}"
    
    if action == "add":
        return "✅ 成员添加成功"
    elif action == "delete":
        return "✅ 成员删除成功"
    elif action == "update":
        return "✅ 成员信息更新成功"
    
    return json.dumps(result, indent=2, ensure_ascii=False)


def format_list_result(result: dict) -> str:
    """格式化成员列表结果"""
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
        return "📭 暂无成员记录"
    
    output = [f"✅ 共 {len(data)} 个成员\n"]
    
    for i, member in enumerate(data, 1):
        output.append(f"👤 成员 {i}:")
        output.append(f"   ID: {member.get('id', 'N/A')}")
        output.append(f"   名称：{member.get('faceSampleName', 'N/A')}")
        output.append(f"   家人通知：{'✅' if member.get('notice') else '⏸️'}")
        output.append(f"   统计标记：{'✅' if member.get('staticFlag') else '⏸️'}")
        if member.get('avatar'):
            output.append(f"   头像：有")
        face_pics = member.get('facePics', [])
        if face_pics:
            output.append(f"   照片数：{len(face_pics)}")
        output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="成员管理 - 新增、删除、修改、查询成员")
    parser.add_argument("--action", required=True, 
                        choices=["add", "delete", "update", "list"], 
                        help="操作类型")
    parser.add_argument("--sn", required=True, help="设备序列号")
    parser.add_argument("--user", required=True, help="用户 ID")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token")
    
    # add/update 操作参数
    parser.add_argument("--name", help="成员名称")
    parser.add_argument("--picture", action="append", help="成员图片（base64，可多次指定）")
    parser.add_argument("--avatar", help="成员头像（base64）")
    parser.add_argument("--notice", type=int, choices=[0, 1], help="家人通知（0 关闭，1 开启）")
    
    # delete/update 操作参数
    parser.add_argument("--id", type=int, help="成员 ID")
    
    # list 操作参数
    parser.add_argument("--member-id", type=int, help="指定成员 ID（list 操作）")
    parser.add_argument("--static-flag", type=int, help="统计标记（list 操作）")
    
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细 curl 命令和原始响应（重要查询必须使用）")
    
    args = parser.parse_args()
    
    if args.action == "add":
        if not args.name or not args.picture:
            print("❌ add 操作需要指定 --name 和 --picture 参数")
            sys.exit(1)
        
        result = add_member(
            sn=args.sn, user=args.user, name=args.name, pictures=args.picture,
            avatar=args.avatar, notice=args.notice if args.notice is not None else 1,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_member_result(result, "add") if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    elif args.action == "delete":
        if not args.id:
            print("❌ delete 操作需要指定 --id 参数")
            sys.exit(1)
        
        result = delete_member(
            sn=args.sn, user=args.user, member_id=args.id,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_member_result(result, "delete") if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    elif args.action == "update":
        if not args.id or not args.name or not args.picture:
            print("❌ update 操作需要指定 --id, --name, --picture 参数")
            sys.exit(1)
        
        result = update_member(
            sn=args.sn, user=args.user, member_id=args.id, name=args.name, pictures=args.picture,
            avatar=args.avatar, notice=args.notice,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_member_result(result, "update") if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    elif args.action == "list":
        result = list_members(
            sn=args.sn, user=args.user,
            member_id=args.member_id, static_flag=args.static_flag,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_list_result(result) if not args.json else json.dumps(result, indent=2, ensure_ascii=False)
    
    print(output)


if __name__ == "__main__":
    main()
