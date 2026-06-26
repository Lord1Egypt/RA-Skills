#!/usr/bin/env python3
"""
宠物管理脚本 - 新增、删除、修改、查询宠物

支持平台：JF Tech（杰峰）
用法：
    python pet_manage.py --action add --name <宠物名> --type <品种> --image <图片> [其他参数]
    python pet_manage.py --action delete --id <宠物 ID> [其他参数]
    python pet_manage.py --action update --id <宠物 ID> --name <新名字> [其他参数]
    python pet_manage.py --action list [其他参数]
"""

import argparse
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# 导入杰峰签名工具
from jf_signature import generate_signature



def add_pet(sn: str, user: str, name: str, pet_type: str, images: list, 
            uuid: str, appkey: str, secret: str, authorization: str,
            avatar: str = None) -> dict:
    """
    新增宠物
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        name: 宠物名称
        pet_type: 宠物品种
        images: 图片列表（base64 或 URL）
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        avatar: 头像（可选）
    
    Returns:
        API 响应字典
    """
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet/face/sample/add"
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        "Content-Type": "application/json",
        "uuid": uuid,
        "appKey": appkey,
        "timeMillis": time_millis,
        "signature": signature,
        "Authorization": authorization
    }
    
    picture_list = [{"picture": img, "no": i + 1} for i, img in enumerate(images[:5])]
    
    body = {
        "sn": sn,
        "user": user,
        "faceSampleName": name,
        "pictureList": picture_list,
        "petType": pet_type
    }
    
    if avatar:
        body["avatar"] = avatar
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def delete_pet(sn: str, user: str, pet_id: str, uuid: str, appkey: str, 
               secret: str, authorization: str) -> dict:
    """
    删除宠物
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        pet_id: 宠物 ID
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
    
    Returns:
        API 响应字典
    """
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet/face/sample/delete"
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
        "faceSampleId": pet_id
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


def update_pet(sn: str, user: str, pet_id: str, name: str, images: list, 
               uuid: str, appkey: str, secret: str, authorization: str,
               pet_type: str = None, avatar: str = None) -> dict:
    """
    编辑宠物信息
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        pet_id: 宠物 ID
        name: 宠物名称
        images: 图片列表
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        pet_type: 宠物品种（可选）
        avatar: 头像（可选）
    
    Returns:
        API 响应字典
    """
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet/face/sample/update"
    time_millis, signature = generate_signature(uuid, appkey, secret, movecard)
    
    headers = {
        "Content-Type": "application/json",
        "uuid": uuid,
        "appKey": appkey,
        "timeMillis": time_millis,
        "signature": signature,
        "Authorization": authorization
    }
    
    picture_list = [{"picture": img, "no": i + 1} for i, img in enumerate(images[:5])]
    
    body = {
        "id": pet_id,
        "sn": sn,
        "user": user,
        "faceSampleName": name,
        "pictureList": picture_list
    }
    
    if pet_type:
        body["petType"] = pet_type
    if avatar:
        body["avatar"] = avatar
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def list_pets(sn: str, user: str, uuid: str, appkey: str, 
              secret: str, authorization: str, movecard: int, pet_id: str = None) -> dict:
    """
    查询宠物列表
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
        pet_id: 指定宠物 ID（可选）
    
    Returns:
        API 响应字典
    """
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet/face/sample/list"
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
    
    if pet_id:
        body["faceSampleId"] = pet_id
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def preview_image(sn: str, user: str, image: str, uuid: str, appkey: str, 
                  secret: str, authorization: str) -> dict:
    """
    宠物图片预览（校验图片是否符合入库要求）
    
    Args:
        sn: 设备序列号
        user: 用户 ID
        image: 图片（base64）
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
    
    Returns:
        API 响应字典
    """
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet/face/sample/previewApp"
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
        "image": image
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


def list_pet_types(language: str = "zh", subject: str = None, 
                   pet_name: str = None, uuid: str = None, appkey: str = None,
                   secret: str = None, authorization: str = None) -> dict:
    """
    查询宠物品类列表
    
    Args:
        language: 语言环境（en 英文，zh 中文）
        subject: 科目（cat 猫，dog 狗）
        pet_name: 名称搜索
        uuid: 开放平台用户 uuid
        appkey: 应用 appKey
        secret: 应用密钥
        authorization: 用户 token
    
    Returns:
        API 响应字典
    """
    url = "https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet/face/type/list"
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
        "language": language
    }
    
    if subject:
        body["subject"] = subject
    if pet_name:
        body["petName"] = pet_name
    
    req = Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            return result
    except HTTPError as e:
        return {"error": f"HTTP {e.code}", "message": e.read().decode()}
    except URLError as e:
        return {"error": "Network error", "message": str(e)}


def format_pet_result(result: dict, action: str) -> str:
    """格式化宠物管理操作结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    if result.get("code") != 2000:
        return f"❌ API 错误码：{result.get('code')}\n{result.get('msg', '')}"
    
    if action == "add":
        return "✅ 宠物添加成功"
    elif action == "delete":
        return "✅ 宠物删除成功"
    elif action == "update":
        return "✅ 宠物信息更新成功"
    elif action == "preview":
        return "✅ 图片校验通过"
    elif action == "types":
        data = result.get("data", [])
        if not data:
            return "📭 未找到宠物品类"
        output = [f"✅ 找到 {len(data)} 个宠物品类\n"]
        for pet in data:
            output.append(f"🐾 {pet.get('petName', 'N/A')} ({pet.get('petCode', 'N/A')}) - {pet.get('subject', 'N/A')}")
        return "\n".join(output)
    
    return json.dumps(result, indent=2, ensure_ascii=False)


def format_list_result(result: dict) -> str:
    """格式化宠物列表结果"""
    if "error" in result:
        return f"❌ 错误：{result.get('error', 'Unknown')}\n{result.get('message', '')}"
    
    if result.get("code") != 2000:
        return f"❌ API 错误码：{result.get('code')}\n{result.get('msg', '')}"
    
    data = result.get("data", [])
    
    if not data:
        return "📭 暂无宠物记录"
    
    output = []
    output.append(f"✅ 共 {len(data)} 只宠物\n")
    
    for i, pet in enumerate(data, 1):
        output.append(f"🐾 宠物 {i}:")
        output.append(f"   名称：{pet.get('faceSampleName', 'N/A')}")
        output.append(f"   品种：{pet.get('petType', 'N/A')}")
        output.append(f"   ID: {pet.get('id', 'N/A')}")
        if pet.get('avatar'):
            output.append(f"   头像：有")
        face_pics = pet.get('facePics', [])
        if face_pics:
            output.append(f"   照片数：{len(face_pics)}")
        output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="宠物管理 - 新增、删除、修改、查询宠物")
    parser.add_argument("--action", required=True, 
                        choices=["add", "delete", "update", "list", "preview", "types"], 
                        help="操作类型")
    parser.add_argument("--sn", help="设备序列号（除 types 外都需要）")
    parser.add_argument("--user", help="用户 ID（除 types 外都需要）")
    parser.add_argument("--uuid", required=True, help="开放平台用户 uuid")
    parser.add_argument("--appkey", required=True, help="应用 appKey")
    parser.add_argument("--secret", required=True, help="应用密钥")
    parser.add_argument("--auth", required=True, help="用户 token")
    parser.add_argument("--id", help="宠物 ID（delete/update 需要）")
    parser.add_argument("--name", help="宠物名称（add/update 需要）")
    parser.add_argument("--type", dest="pet_type", help="宠物品种（add/update 需要）")
    parser.add_argument("--image", action="append", help="宠物图片（可多次指定）")
    parser.add_argument("--avatar", help="宠物头像")
    parser.add_argument("--language", default="zh", help="语言环境（types 操作）")
    parser.add_argument("--subject", help="科目：cat/dog（types 操作）")
    parser.add_argument("--pet-name-search", help="名称搜索（types 操作）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细 curl 命令和原始响应（重要查询必须使用）")
    
    args = parser.parse_args()
    
    # 验证必需参数
    if args.action in ["add", "delete", "update", "list", "preview"]:
        if not args.sn or not args.user:
            print("❌ 此操作需要指定 --sn 和 --user 参数")
            sys.exit(1)
    
    if args.action == "add":
        if not args.name or not args.pet_type or not args.image:
            print("❌ add 操作需要指定 --name, --type, --image 参数")
            sys.exit(1)
        result = add_pet(
            sn=args.sn, user=args.user, name=args.name, pet_type=args.pet_type,
            images=args.image, avatar=args.avatar,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_pet_result(result, "add")
    
    elif args.action == "delete":
        if not args.id:
            print("❌ delete 操作需要指定 --id 参数")
            sys.exit(1)
        result = delete_pet(
            sn=args.sn, user=args.user, pet_id=args.id,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_pet_result(result, "delete")
    
    elif args.action == "update":
        if not args.id or not args.name or not args.image:
            print("❌ update 操作需要指定 --id, --name, --image 参数")
            sys.exit(1)
        result = update_pet(
            sn=args.sn, user=args.user, pet_id=args.id, name=args.name,
            images=args.image, pet_type=args.pet_type, avatar=args.avatar,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_pet_result(result, "update")
    
    elif args.action == "list":
        result = list_pets(
            sn=args.sn, user=args.user, pet_id=args.id,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        if args.json:
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = format_list_result(result)
    
    elif args.action == "preview":
        if not args.image:
            print("❌ preview 操作需要指定 --image 参数")
            sys.exit(1)
        result = preview_image(
            sn=args.sn, user=args.user, image=args.image[0],
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        output = format_pet_result(result, "preview")
    
    elif args.action == "types":
        result = list_pet_types(
            language=args.language, subject=args.subject, pet_name=args.pet_name_search,
            uuid=args.uuid, appkey=args.appkey, secret=args.secret, authorization=args.auth
        )
        if args.json:
            output = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output = format_pet_result(result, "types")
    
    else:
        print(f"❌ 未知操作：{args.action}")
        sys.exit(1)
    
    print(output)


if __name__ == "__main__":
    main()
