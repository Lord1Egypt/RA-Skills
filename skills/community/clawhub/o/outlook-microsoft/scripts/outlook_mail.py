#!/usr/bin/env python3
"""
Microsoft Outlook 邮件操作脚本 - 世纪互联版
支持读取、搜索、标记、发送邮件
"""

import json
import os
import sys
import io
import requests
import base64
import re
from pathlib import Path

# 确保 stdout 输出 UTF-8 编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 世纪互联版 Graph API 端点
GRAPH_BASE_URL = "https://microsoftgraph.chinacloudapi.cn"
SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = Path.home() / ".outlook-microsoft"
CREDS_FILE = CONFIG_DIR / "credentials.json"
ENV_FILE = SCRIPT_DIR / ".env"


def load_env():
    """从 .env 文件加载环境变量"""
    if not ENV_FILE.exists():
        return
    with open(ENV_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key and value and not os.getenv(key):
                    os.environ[key] = value


load_env()  # 启动时加载 .env 文件


def load_credentials():
    if not CREDS_FILE.exists():
        return None
    with open(CREDS_FILE, "r") as f:
        return json.load(f)


def get_access_token():
    """获取有效的 Access Token"""
    creds = load_credentials()
    if not creds:
        print(json.dumps({
            "error": "AUTH_001",
            "message": "未授权，请先运行 outlook_auth.py authorize 完成授权。"
        }, ensure_ascii=False))
        sys.exit(1)

    import time
    if time.time() < creds.get("expires_at", 0) - 300:
        return creds["access_token"]

    # Token 过期，尝试刷新
    import subprocess
    result = subprocess.run(
        ["python3", str(Path(__file__).parent / "outlook_auth.py"), "refresh"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(json.dumps({
            "error": "AUTH_002",
            "message": "Token 已过期且刷新失败，请重新运行 authorize。"
        }, ensure_ascii=False))
        sys.exit(1)

    creds = load_credentials()
    return creds["access_token"] if creds else None


def api_call(method, path, token, data=None, params=None):
    """调用 Microsoft Graph API"""
    url = f"{GRAPH_BASE_URL}/v1.0{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        if method.upper() == "GET":
            resp = requests.get(url, headers=headers, params=params, timeout=30)
        elif method.upper() == "POST":
            resp = requests.post(url, headers=headers, json=data, timeout=30)
        elif method.upper() == "PATCH":
            resp = requests.patch(url, headers=headers, json=data, timeout=30)
        elif method.upper() == "DELETE":
            resp = requests.delete(url, headers=headers, timeout=30)
        else:
            raise ValueError(f"Unknown method: {method}")

        resp.raise_for_status()
        return resp.json() if resp.content else {}

    except requests.exceptions.HTTPError as e:
        try:
            err_body = e.response.json()
            err_msg = err_body.get("error", {}).get("message", str(e))
        except:
            err_msg = str(e)

        print(json.dumps({
            "error": "API_002",
            "message": f"Graph API 调用失败: {err_msg}",
            "http_status": e.response.status_code
        }, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "error": "API_001",
            "message": f"网络请求失败: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)


def cmd_inbox(args):
    """读取收件箱"""
    token = get_access_token()
    count = args.get("count", 10)

    result = api_call("GET", "/me/mailFolders/inbox/messages", token, params={
        "$top": count,
        "$orderby": "receivedDateTime desc",
        "$select": "id,subject,from,toRecipients,receivedDateTime,isRead,importance,hasAttachments"
    })

    messages = result.get("value", [])
    output = []
    for i, msg in enumerate(messages, 1):
        output.append({
            "n": i,
            "subject": msg.get("subject", "(无主题)"),
            "from": msg.get("from", {}).get("emailAddress", {}).get("address", "N/A"),
            "to": [r.get("emailAddress", {}).get("address") for r in msg.get("toRecipients", [])],
            "date": msg.get("receivedDateTime", ""),
            "read": msg.get("isRead", False),
            "importance": msg.get("importance", "normal"),
            "has_attachments": msg.get("hasAttachments", False),
            "id": msg.get("id", "")
        })

    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_unread(args):
    """读取未读邮件"""
    token = get_access_token()
    count = args.get("count", 10)

    result = api_call("GET", "/me/mailFolders/inbox/messages", token, params={
        "$top": count,
        "$filter": "isRead eq false",
        "$orderby": "receivedDateTime desc",
        "$select": "id,subject,from,receivedDateTime,importance,hasAttachments"
    })

    messages = result.get("value", [])
    output = []
    for i, msg in enumerate(messages, 1):
        output.append({
            "n": i,
            "subject": msg.get("subject", "(无主题)"),
            "from": msg.get("from", {}).get("emailAddress", {}).get("address", "N/A"),
            "date": msg.get("receivedDateTime", ""),
            "importance": msg.get("importance", "normal"),
            "has_attachments": msg.get("hasAttachments", False),
            "id": msg.get("id", "")
        })

    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_search(args):
    """搜索邮件"""
    token = get_access_token()
    query = args.get("query", "")
    count = args.get("count", 10)

    if not query:
        print(json.dumps({"error": "API_002", "message": "搜索关键词不能为空"}))
        sys.exit(1)

    result = api_call("GET", "/me/messages", token, params={
        "$top": count,
        "$search": f'"{query}"',
        "$orderby": "receivedDateTime desc",
        "$select": "id,subject,from,receivedDateTime,isRead,importance"
    })

    messages = result.get("value", [])
    output = []
    for i, msg in enumerate(messages, 1):
        output.append({
            "n": i,
            "subject": msg.get("subject", "(无主题)"),
            "from": msg.get("from", {}).get("emailAddress", {}).get("address", "N/A"),
            "date": msg.get("receivedDateTime", ""),
            "read": msg.get("isRead", False),
            "importance": msg.get("importance", "normal"),
            "id": msg.get("id", "")
        })

    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_from(args):
    """按发件人筛选"""
    token = get_access_token()
    sender = args.get("sender", "")
    count = args.get("count", 10)

    if not sender:
        print(json.dumps({"error": "API_002", "message": "发件人邮箱不能为空"}))
        sys.exit(1)

    result = api_call("GET", "/me/messages", token, params={
        "$top": count,
        "$filter": f"from/emailAddress/address eq '{sender}'",
        "$orderby": "receivedDateTime desc",
        "$select": "id,subject,from,receivedDateTime,isRead,importance"
    })

    messages = result.get("value", [])
    output = []
    for i, msg in enumerate(messages, 1):
        output.append({
            "n": i,
            "subject": msg.get("subject", "(无主题)"),
            "from": msg.get("from", {}).get("emailAddress", {}).get("address", "N/A"),
            "date": msg.get("receivedDateTime", ""),
            "read": msg.get("isRead", False),
            "id": msg.get("id", "")
        })

    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_read(args):
    """读取单封邮件详情"""
    token = get_access_token()
    message_id = args.get("message_id", "")

    if not message_id:
        print(json.dumps({"error": "API_002", "message": "message_id 不能为空"}))
        sys.exit(1)

    msg = api_call("GET", f"/me/messages/{message_id}", token, params={
        "$select": "id,subject,from,toRecipients,ccRecipients,bccRecipients,"
                  "receivedDateTime,sentDateTime,body,importance,hasAttachments,"
                  "attachments,internetMessageHeaders"
    })

    # 提取邮件正文
    body_content = ""
    body_type = msg.get("body", {}).get("contentType", "")
    body_raw = msg.get("body", {}).get("content", "")

    if body_type == "html":
        # 简单处理 HTML：去除标签
        import re
        body_content = re.sub(r'<[^>]+>', '', body_raw)
        body_content = body_content.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')
    else:
        body_content = body_raw

    output = {
        "id": msg.get("id"),
        "subject": msg.get("subject", "(无主题)"),
        "from": {
            "name": msg.get("from", {}).get("emailAddress", {}).get("name", ""),
            "address": msg.get("from", {}).get("emailAddress", {}).get("address", "")
        },
        "to": [r.get("emailAddress", {}).get("address") for r in msg.get("toRecipients", [])],
        "cc": [r.get("emailAddress", {}).get("address") for r in msg.get("ccRecipients", [])],
        "date": msg.get("receivedDateTime", ""),
        "sent_date": msg.get("sentDateTime", ""),
        "importance": msg.get("importance", "normal"),
        "has_attachments": msg.get("hasAttachments", False),
        "body_type": body_type,
        "body": body_content[:5000] if len(body_content) > 5000 else body_content,  # 限制长度
        "attachments": [
            {"name": a.get("name"), "size": a.get("size"), "id": a.get("id")}
            for a in msg.get("attachments", []) if a.get("@odata.type", "").endswith("fileAttachment")
        ]
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_attachments(args):
    """获取邮件附件列表"""
    token = get_access_token()
    message_id = args.get("message_id", "")

    if not message_id:
        print(json.dumps({"error": "API_002", "message": "message_id 不能为空"}))
        sys.exit(1)

    attachments = api_call("GET", f"/me/messages/{message_id}/attachments", token)

    output = []
    for a in attachments.get("value", []):
        if a.get("@odata.type", "").endswith("fileAttachment"):
            output.append({
                "name": a.get("name"),
                "size": a.get("size"),
                "content_type": a.get("contentType"),
                "id": a.get("id"),
                "is_inline": a.get("isInline", False)
            })

    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_mark_read(args):
    """标记为已读"""
    token = get_access_token()
    message_id = args.get("message_id", "")

    if not message_id:
        print(json.dumps({"error": "API_002", "message": "message_id 不能为空"}))
        sys.exit(1)

    api_call("PATCH", f"/me/messages/{message_id}", token, data={"isRead": True})
    print(json.dumps({"status": "success", "message": "✅ 已标记为已读"}))


def cmd_mark_unread(args):
    """标记为未读"""
    token = get_access_token()
    message_id = args.get("message_id", "")

    if not message_id:
        print(json.dumps({"error": "API_002", "message": "message_id 不能为空"}))
        sys.exit(1)

    api_call("PATCH", f"/me/messages/{message_id}", token, data={"isRead": False})
    print(json.dumps({"status": "success", "message": "✅ 已标记为未读"}))


def cmd_flag(args):
    """标记重要"""
    token = get_access_token()
    message_id = args.get("message_id", "")

    if not message_id:
        print(json.dumps({"error": "API_002", "message": "message_id 不能为空"}))
        sys.exit(1)

    api_call("PATCH", f"/me/messages/{message_id}", token, data={"importance": "high"})
    print(json.dumps({"status": "success", "message": "✅ 已标记为重要"}))


def cmd_unflag(args):
    """取消重要标记"""
    token = get_access_token()
    message_id = args.get("message_id", "")

    if not message_id:
        print(json.dumps({"error": "API_002", "message": "message_id 不能为空"}))
        sys.exit(1)

    api_call("PATCH", f"/me/messages/{message_id}", token, data={"importance": "normal"})
    print(json.dumps({"status": "success", "message": "✅ 已取消重要标记"}))


def cmd_delete(args):
    """删除邮件（移至回收站）"""
    token = get_access_token()
    message_id = args.get("message_id", "")

    if not message_id:
        print(json.dumps({"error": "API_002", "message": "message_id 不能为空"}))
        sys.exit(1)

    api_call("DELETE", f"/me/messages/{message_id}", token)
    print(json.dumps({"status": "success", "message": "✅ 邮件已删除"}))


def cmd_archive(args):
    """归档邮件"""
    token = get_access_token()
    message_id = args.get("message_id", "")

    if not message_id:
        print(json.dumps({"error": "API_002", "message": "message_id 不能为空"}))
        sys.exit(1)

    # 先获取归档文件夹 ID
    folders = api_call("GET", "/me/mailFolders", token)
    archive_folder = next(
        (f["id"] for f in folders.get("value", []) if f.get("displayName") == "Archive"),
        None
    )

    if not archive_folder:
        print(json.dumps({"error": "API_002", "message": "未找到 Archive 文件夹"}))
        sys.exit(1)

    # 移动到归档
    api_call("POST", f"/me/messages/{message_id}/move", token, data={
        "destinationId": archive_folder
    })
    print(json.dumps({"status": "success", "message": "✅ 邮件已归档"}))


def cmd_move(args):
    """移动邮件到指定文件夹"""
    token = get_access_token()
    message_id = args.get("message_id", "")
    folder = args.get("folder", "")

    if not message_id or not folder:
        print(json.dumps({"error": "API_002", "message": "message_id 和 folder 不能为空"}))
        sys.exit(1)

    # 获取目标文件夹 ID
    folders = api_call("GET", "/me/mailFolders", token)
    target_folder = next(
        (f["id"] for f in folders.get("value", []) if f.get("displayName", "").lower() == folder.lower()),
        None
    )

    if not target_folder:
        print(json.dumps({"error": "API_002", "message": f"未找到文件夹: {folder}"}))
        sys.exit(1)

    api_call("POST", f"/me/messages/{message_id}/move", token, data={
        "destinationId": target_folder
    })
    print(json.dumps({"status": "success", "message": f"✅ 邮件已移动到 {folder}"}))


def cmd_send(args):
    """发送新邮件"""
    token = get_access_token()
    to = args.get("to", "")
    subject = args.get("subject", "")
    body = args.get("body", "")
    cc = args.get("cc")
    bcc = args.get("bcc")

    if not to or not subject or not body:
        print(json.dumps({
            "error": "API_002",
            "message": "to（收件人）、subject（主题）、body（正文）不能为空"
        }))
        sys.exit(1)

    email_msg = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                {"emailAddress": {"address": addr.strip()}}
                for addr in to.split(",") if addr.strip()
            ]
        },
        "saveToSentItems": "true"
    }

    if cc:
        email_msg["message"]["ccRecipients"] = [
            {"emailAddress": {"address": addr.strip()}}
            for addr in cc.split(",") if addr.strip()
        ]

    if bcc:
        email_msg["message"]["bccRecipients"] = [
            {"emailAddress": {"address": addr.strip()}}
            for addr in bcc.split(",") if addr.strip()
        ]

    result = api_call("POST", "/me/sendMail", token, data=email_msg)
    print(json.dumps({"status": "success", "message": f"✅ 邮件已发送给 {to}"}))


def cmd_reply(args):
    """回复邮件"""
    token = get_access_token()
    message_id = args.get("message_id", "")
    body = args.get("body", "")

    if not message_id or not body:
        print(json.dumps({
            "error": "API_002",
            "message": "message_id 和 body 不能为空"
        }))
        sys.exit(1)

    email_msg = {
        "message": {
            "subject": "Re: " + args.get("subject", ""),  # subject 会被服务器自动处理
            "body": {
                "contentType": "Text",
                "content": body
            }
        },
        "saveToSentItems": "true"
    }

    result = api_call("POST", f"/me/messages/{message_id}/reply", token, data=email_msg)
    print(json.dumps({"status": "success", "message": "✅ 已发送回复"}))


def cmd_folders(args):
    """列出所有邮件文件夹"""
    token = get_access_token()

    result = api_call("GET", "/me/mailFolders", token)

    output = []
    for f in result.get("value", []):
        output.append({
            "name": f.get("displayName"),
            "id": f.get("id"),
            "total": f.get("totalItemCount", 0),
            "unread": f.get("unreadItemCount", 0)
        })

    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_stats(args):
    """获取邮箱统计信息"""
    token = get_access_token()

    folders = api_call("GET", "/me/mailFolders", token)

    output = []
    for f in folders.get("value", []):
        if f.get("totalItemCount", 0) > 0:
            output.append({
                "folder": f.get("displayName"),
                "total": f.get("totalItemCount", 0),
                "unread": f.get("unreadItemCount", 0)
            })

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: outlook_mail.py <command> '<json_params>'")
        print("\n可用命令：inbox, unread, search, from, read, attachments, "
              "mark-read, mark-unread, flag, unflag, delete, archive, move, "
              "send, reply, folders, stats")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    # 从 stdin 读取 JSON 参数
    args = {}
    if len(sys.argv) >= 3:
        try:
            args = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(json.dumps({"error": "API_002", "message": f"JSON 参数解析失败: {e}"}))
            sys.exit(1)

    # 命令路由
    commands = {
        "inbox": cmd_inbox,
        "unread": cmd_unread,
        "search": cmd_search,
        "from": cmd_from,
        "read": cmd_read,
        "attachments": cmd_attachments,
        "mark-read": cmd_mark_read,
        "mark-unread": cmd_mark_unread,
        "flag": cmd_flag,
        "unflag": cmd_unflag,
        "delete": cmd_delete,
        "archive": cmd_archive,
        "move": cmd_move,
        "send": cmd_send,
        "reply": cmd_reply,
        "folders": cmd_folders,
        "stats": cmd_stats,
    }

    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
