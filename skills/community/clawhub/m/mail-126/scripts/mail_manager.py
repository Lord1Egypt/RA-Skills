#!/usr/bin/env python3
"""
Mail-126: 网易 126.com 邮箱管理 CLI
支持 IMAP 收件、SMTP 发件、邮件搜索、管理和统计
仅使用 Python 标准库
"""

import argparse
import base64
import email
import email.header
import email.utils
import imaplib
import json
import os
import re
import smtplib
import ssl
import sys
import time
from datetime import datetime, timedelta
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate, make_msgid
from pathlib import Path

# ============================================================
# 常量
# ============================================================

DATA_DIR = Path.home() / "mail126_data"
CONFIG_FILE = DATA_DIR / "config.json"

IMAP_SERVER = "imap.126.com"
IMAP_PORT = 993
SMTP_SERVER = "smtp.126.com"
SMTP_PORT = 465

CONNECTION_TIMEOUT = 30
MAX_RETRIES = 2

FOLDER_MAP = {
    "收件箱": "INBOX",
    "已发送": "Sent Messages",
    "草稿": "Drafts",
    "已删除": "Trash",
    "垃圾邮件": "Junk",
    "病毒邮件": "Virus",
}


# ============================================================
# 工具函数
# ============================================================


def output_json(status, data=None, message=""):
    """统一 JSON 输出"""
    result = {"status": status, "data": data, "message": message}
    print(json.dumps(result, ensure_ascii=False, indent=2))


def decode_header_value(value):
    """解码邮件头部字段"""
    if not value:
        return ""
    decoded_parts = email.header.decode_header(value)
    result_parts = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            charset = charset or "utf-8"
            try:
                result_parts.append(part.decode(charset, errors="replace"))
            except (LookupError, UnicodeDecodeError):
                result_parts.append(part.decode("utf-8", errors="replace"))
        else:
            result_parts.append(part)
    return "".join(result_parts)


def parse_address(addr_str):
    """解析邮件地址，返回 '名称 <email>' 格式"""
    if not addr_str:
        return ""
    decoded = decode_header_value(addr_str)
    return decoded


def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


# ============================================================
# 配置管理
# ============================================================


def load_config():
    """加载配置文件"""
    if not CONFIG_FILE.exists():
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        # 解码授权码
        if "auth_code" in config:
            try:
                config["auth_code"] = base64.b64decode(config["auth_code"]).decode("utf-8")
            except Exception:
                pass
        return config
    except Exception as e:
        return None


def save_config(config):
    """保存配置文件"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    save_data = dict(config)
    # 编码授权码
    if "auth_code" in save_data:
        save_data["auth_code"] = base64.b64encode(
            save_data["auth_code"].encode("utf-8")
        ).decode("utf-8")
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)


def require_config():
    """获取配置，未配置时输出错误"""
    config = load_config()
    if not config:
        output_json("error", message="未配置邮箱账号，请先运行: config setup --email <邮箱> --auth-code <授权码>")
        sys.exit(0)
    return config


# ============================================================
# 连接管理
# ============================================================


def get_imap_connection(config, retries=MAX_RETRIES):
    """获取 IMAP 连接"""
    last_error = None
    for attempt in range(retries + 1):
        try:
            ctx = ssl.create_default_context()
            conn = imaplib.IMAP4_SSL(
                config["imap_server"],
                config.get("imap_port", IMAP_PORT),
                ssl_context=ctx,
            )
            conn.login(config["email"], config["auth_code"])
            return conn
        except Exception as e:
            last_error = e
            if attempt < retries:
                time.sleep(1)
    raise ConnectionError(f"IMAP 连接失败: {last_error}")


def get_smtp_connection(config, retries=MAX_RETRIES):
    """获取 SMTP 连接"""
    last_error = None
    for attempt in range(retries + 1):
        try:
            ctx = ssl.create_default_context()
            conn = smtplib.SMTP_SSL(
                config["smtp_server"],
                config.get("smtp_port", SMTP_PORT),
                context=ctx,
                timeout=CONNECTION_TIMEOUT,
            )
            conn.login(config["email"], config["auth_code"])
            return conn
        except Exception as e:
            last_error = e
            if attempt < retries:
                time.sleep(1)
    raise ConnectionError(f"SMTP 连接失败: {last_error}")


# ============================================================
# 邮件解析
# ============================================================


def parse_email_headers(msg):
    """解析邮件头部信息"""
    subject = decode_header_value(msg.get("Subject", ""))
    from_addr = parse_address(msg.get("From", ""))
    to_addr = parse_address(msg.get("To", ""))
    cc_addr = parse_address(msg.get("Cc", ""))
    date_str = msg.get("Date", "")

    # 解析日期
    try:
        date_tuple = email.utils.parsedate_to_datetime(date_str)
        date_formatted = date_tuple.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        date_formatted = date_str

    return {
        "subject": subject,
        "from": from_addr,
        "to": to_addr,
        "cc": cc_addr,
        "date": date_formatted,
    }


def parse_email_body(msg):
    """解析邮件正文和附件"""
    body_text = ""
    body_html = ""
    attachments = []

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))

            if "attachment" in content_disposition:
                # 附件
                filename = part.get_filename()
                if filename:
                    filename = decode_header_value(filename)
                    attachments.append({
                        "filename": filename,
                        "content_type": content_type,
                        "size": len(part.get_payload(decode=True) or b""),
                    })
            elif content_type == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    try:
                        body_text = payload.decode(charset, errors="replace")
                    except (LookupError, UnicodeDecodeError):
                        body_text = payload.decode("utf-8", errors="replace")
            elif content_type == "text/html":
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    try:
                        body_html = payload.decode(charset, errors="replace")
                    except (LookupError, UnicodeDecodeError):
                        body_html = payload.decode("utf-8", errors="replace")
    else:
        content_type = msg.get_content_type()
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            try:
                decoded = payload.decode(charset, errors="replace")
            except (LookupError, UnicodeDecodeError):
                decoded = payload.decode("utf-8", errors="replace")

            if content_type == "text/html":
                body_html = decoded
            else:
                body_text = decoded

    return {
        "body_text": body_text.strip(),
        "body_html": body_html.strip(),
        "attachments": attachments,
    }


# ============================================================
# 初始化
# ============================================================


def cmd_init():
    """初始化数据目录"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        output_json("success", data={"config_file": str(CONFIG_FILE)}, message="数据目录已存在")
    else:
        default_config = {
            "email": "",
            "auth_code": "",
            "imap_server": IMAP_SERVER,
            "imap_port": IMAP_PORT,
            "smtp_server": SMTP_SERVER,
            "smtp_port": SMTP_PORT,
            "created_at": datetime.now().isoformat(),
        }
        save_config(default_config)
        output_json("success", data={"config_file": str(CONFIG_FILE)}, message="初始化完成，请运行 config setup 配置邮箱")


# ============================================================
# 配置命令
# ============================================================


def cmd_config_setup(args):
    """配置邮箱账号"""
    email_addr = args.email
    auth_code = args.auth_code

    if not email_addr or not auth_code:
        output_json("error", message="请提供 --email 和 --auth-code 参数")
        return

    config = load_config() or {}
    config["email"] = email_addr
    config["auth_code"] = auth_code
    config["imap_server"] = IMAP_SERVER
    config["imap_port"] = IMAP_PORT
    config["smtp_server"] = SMTP_SERVER
    config["smtp_port"] = SMTP_PORT
    if "created_at" not in config:
        config["created_at"] = datetime.now().isoformat()

    save_config(config)
    output_json("success", data={"email": email_addr}, message="配置保存成功，请运行 config verify 验证连接")


def cmd_config_verify(args):
    """验证 IMAP/SMTP 连接"""
    config = require_config()

    results = {"imap": False, "smtp": False}

    # 测试 IMAP
    try:
        conn = get_imap_connection(config)
        conn.logout()
        results["imap"] = True
    except Exception as e:
        results["imap_error"] = str(e)

    # 测试 SMTP
    try:
        conn = get_smtp_connection(config)
        conn.quit()
        results["smtp"] = True
    except Exception as e:
        results["smtp_error"] = str(e)

    if results["imap"] and results["smtp"]:
        output_json("success", data=results, message="IMAP 和 SMTP 连接验证通过")
    else:
        output_json("error", data=results, message="连接验证失败，请检查邮箱地址和授权码")


# ============================================================
# 收件箱命令
# ============================================================


def cmd_inbox_list(args):
    """列出邮件"""
    config = require_config()
    folder = args.folder or "INBOX"
    # 支持中文文件夹名映射
    folder = FOLDER_MAP.get(folder, folder)
    limit = args.limit or 10
    offset = args.offset or 0
    unread_only = args.unread

    conn = None
    try:
        conn = get_imap_connection(config)
        conn.select(folder, readonly=True)

        # 搜索条件
        if unread_only:
            status, msg_ids = conn.search(None, "UNSEEN")
        else:
            status, msg_ids = conn.search(None, "ALL")

        if status != "OK":
            output_json("error", message="搜索邮件失败")
            return

        id_list = msg_ids[0].split()
        total = len(id_list)

        # 取最新的邮件（倒序取）
        id_list_rev = list(reversed(id_list))
        selected = id_list_rev[offset: offset + limit]

        emails = []
        for mid in selected:
            status, msg_data = conn.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM TO SUBJECT DATE)]) FLAGS")
            if status != "OK":
                continue

            # 获取 FLAGS
            flags = []
            uid = mid.decode()

            # 用 UID 方式获取
            status, uid_data = conn.fetch(mid, "(UID)")
            if status == "OK":
                uid_match = re.search(rb"UID (\d+)", uid_data[0])
                if uid_match:
                    uid = uid_match.group(1).decode()

            # 获取标记
            status, flag_data = conn.fetch(mid, "(FLAGS)")
            if status == "OK":
                flag_match = re.search(rb"FLAGS \(([^)]*)\)", flag_data[0])
                if flag_match:
                    flags_str = flag_match.group(1).decode()
                    flags = [f.strip().replace("\\", "").lower() for f in flags_str.split() if f.strip()]

            # 获取大小
            size = 0
            status, size_data = conn.fetch(mid, "(RFC822.SIZE)")
            if status == "OK":
                size_match = re.search(rb"RFC822\.SIZE (\d+)", size_data[0])
                if size_match:
                    size = int(size_match.group(1))

            # 解析头部
            raw_header = msg_data[0][1]
            msg = email.message_from_bytes(raw_header)
            headers = parse_email_headers(msg)

            emails.append({
                "uid": uid,
                "from": headers["from"],
                "to": headers["to"],
                "subject": headers["subject"],
                "date": headers["date"],
                "flags": flags,
                "size": size,
            })

        output_json("success", data={
            "folder": folder,
            "total": total,
            "emails": emails,
        }, message=f"列出 {len(emails)} 封邮件（共 {total} 封）")

    except Exception as e:
        output_json("error", message=f"列出邮件失败: {e}")
    finally:
        if conn:
            try:
                conn.logout()
            except Exception:
                pass


def cmd_inbox_read(args):
    """读取邮件详情"""
    config = require_config()
    uid = args.uid
    folder = args.folder or "INBOX"
    folder = FOLDER_MAP.get(folder, folder)

    conn = None
    try:
        conn = get_imap_connection(config)
        conn.select(folder, readonly=True)

        # 通过 UID 获取邮件
        status, msg_data = conn.uid("fetch", str(uid), "(RFC822)")
        if status != "OK" or not msg_data or not msg_data[0]:
            output_json("error", message=f"未找到 UID={uid} 的邮件")
            return

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # 解析头部
        headers = parse_email_headers(msg)

        # 解析正文和附件
        body = parse_email_body(msg)

        # 解析收件人列表
        to_list = []
        if headers["to"]:
            to_list = [addr.strip() for addr in headers["to"].split(",")]
        cc_list = []
        if headers["cc"]:
            cc_list = [addr.strip() for addr in headers["cc"].split(",")]

        result = {
            "uid": str(uid),
            "from": headers["from"],
            "to": to_list,
            "cc": cc_list,
            "subject": headers["subject"],
            "date": headers["date"],
            "body_text": body["body_text"],
            "body_html": body["body_html"],
            "attachments": body["attachments"],
        }

        output_json("success", data=result, message=f"读取邮件 UID {uid}")

    except Exception as e:
        output_json("error", message=f"读取邮件失败: {e}")
    finally:
        if conn:
            try:
                conn.logout()
            except Exception:
                pass


def cmd_inbox_search(args):
    """搜索邮件"""
    config = require_config()
    folder = args.folder or "INBOX"
    folder = FOLDER_MAP.get(folder, folder)
    limit = args.limit or 20
    offset = args.offset or 0

    # 构建搜索条件
    criteria = []
    if args.from_sender:
        criteria.append(f'FROM "{args.from_sender}"')
    if args.subject:
        criteria.append(f'SUBJECT "{args.subject}"')
    if args.to:
        criteria.append(f'TO "{args.to}"')
    if args.since:
        criteria.append(f'SINCE {args.since.replace("-", "-")}')
    if args.until:
        criteria.append(f'BEFORE {args.until.replace("-", "-")}')

    if not criteria:
        criteria.append("ALL")

    conn = None
    try:
        conn = get_imap_connection(config)
        conn.select(folder, readonly=True)

        search_str = " ".join(criteria)
        status, msg_ids = conn.search(None, *criteria)
        if status != "OK":
            output_json("error", message="搜索失败")
            return

        id_list = msg_ids[0].split()
        total = len(id_list)

        # 取最新的
        id_list_rev = list(reversed(id_list))
        selected = id_list_rev[offset: offset + limit]

        emails = []
        for mid in selected:
            # 获取 UID
            uid = mid.decode()
            status, uid_data = conn.fetch(mid, "(UID)")
            if status == "OK":
                uid_match = re.search(rb"UID (\d+)", uid_data[0])
                if uid_match:
                    uid = uid_match.group(1).decode()

            # 获取头部
            status, header_data = conn.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM TO SUBJECT DATE)])")
            flags = []
            status_f, flag_data = conn.fetch(mid, "(FLAGS)")
            if status_f == "OK":
                flag_match = re.search(rb"FLAGS \(([^)]*)\)", flag_data[0])
                if flag_match:
                    flags_str = flag_match.group(1).decode()
                    flags = [f.strip().replace("\\", "").lower() for f in flags_str.split() if f.strip()]

            size = 0
            status_s, size_data = conn.fetch(mid, "(RFC822.SIZE)")
            if status_s == "OK":
                size_match = re.search(rb"RFC822\.SIZE (\d+)", size_data[0])
                if size_match:
                    size = int(size_match.group(1))

            if status == "OK" and header_data and header_data[0]:
                msg = email.message_from_bytes(header_data[0][1])
                headers = parse_email_headers(msg)
                emails.append({
                    "uid": uid,
                    "from": headers["from"],
                    "to": headers["to"],
                    "subject": headers["subject"],
                    "date": headers["date"],
                    "flags": flags,
                    "size": size,
                })

        query_info = {
            "from": args.from_sender,
            "subject": args.subject,
            "to": args.to,
            "since": args.since,
            "until": args.until,
        }

        output_json("success", data={
            "query": query_info,
            "total": total,
            "emails": emails,
        }, message=f"找到 {total} 封匹配邮件，显示 {len(emails)} 封")

    except Exception as e:
        output_json("error", message=f"搜索邮件失败: {e}")
    finally:
        if conn:
            try:
                conn.logout()
            except Exception:
                pass


def cmd_inbox_download(args):
    """下载邮件附件"""
    config = require_config()
    uid = args.uid
    folder = args.folder or "INBOX"
    folder = FOLDER_MAP.get(folder, folder)
    output_dir = args.output_dir or str(Path.home() / "Downloads")
    target_attachment = args.attachment

    conn = None
    try:
        conn = get_imap_connection(config)
        conn.select(folder, readonly=True)

        status, msg_data = conn.uid("fetch", str(uid), "(RFC822)")
        if status != "OK" or not msg_data or not msg_data[0]:
            output_json("error", message=f"未找到 UID={uid} 的邮件")
            return

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        os.makedirs(output_dir, exist_ok=True)
        downloaded = []

        for part in msg.walk():
            content_disposition = str(part.get("Content-Disposition", ""))
            if "attachment" not in content_disposition:
                continue

            filename = part.get_filename()
            if not filename:
                continue
            filename = decode_header_value(filename)

            if target_attachment and filename != target_attachment:
                continue

            payload = part.get_payload(decode=True)
            if not payload:
                continue

            filepath = os.path.join(output_dir, filename)
            # 避免文件名冲突
            counter = 1
            base, ext = os.path.splitext(filepath)
            while os.path.exists(filepath):
                filepath = f"{base}_{counter}{ext}"
                counter += 1

            with open(filepath, "wb") as f:
                f.write(payload)

            downloaded.append({
                "filename": filename,
                "size": len(payload),
                "path": filepath,
            })

        if not downloaded:
            if target_attachment:
                output_json("error", message=f"未找到附件: {target_attachment}")
            else:
                output_json("error", message="该邮件没有附件")
        else:
            output_json("success", data={
                "uid": str(uid),
                "output_dir": output_dir,
                "downloaded": downloaded,
            }, message=f"下载 {len(downloaded)} 个附件到 {output_dir}")

    except Exception as e:
        output_json("error", message=f"下载附件失败: {e}")
    finally:
        if conn:
            try:
                conn.logout()
            except Exception:
                pass


# ============================================================
# 发送命令
# ============================================================


def cmd_send(args):
    """发送新邮件"""
    config = require_config()
    to_list = [addr.strip() for addr in args.to.split(",") if addr.strip()]
    if not to_list:
        output_json("error", message="请提供收件人地址 (--to)")
        return

    subject = args.subject or "(无主题)"
    body = args.body or ""
    html_body = args.html or ""

    cc_list = []
    if args.cc:
        cc_list = [addr.strip() for addr in args.cc.split(",") if addr.strip()]

    bcc_list = []
    if args.bcc:
        bcc_list = [addr.strip() for addr in args.bcc.split(",") if addr.strip()]

    # 构建邮件
    msg = MIMEMultipart()
    msg["From"] = config["email"]
    msg["To"] = ", ".join(to_list)
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()

    if cc_list:
        msg["Cc"] = ", ".join(cc_list)

    # 正文
    if html_body:
        msg.attach(MIMEText(body, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))
    else:
        msg.attach(MIMEText(body, "plain", "utf-8"))

    # 附件
    attachments_count = 0
    if args.attachments:
        for filepath in args.attachments.split(","):
            filepath = filepath.strip()
            if not os.path.isfile(filepath):
                output_json("error", message=f"附件不存在: {filepath}")
                return
            with open(filepath, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            email.encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                "attachment",
                filename=os.path.basename(filepath),
            )
            msg.attach(part)
            attachments_count += 1

    # 发送
    all_recipients = to_list + cc_list + bcc_list
    conn = None
    try:
        conn = get_smtp_connection(config)
        conn.sendmail(config["email"], all_recipients, msg.as_string())

        output_json("success", data={
            "to": to_list,
            "cc": cc_list,
            "bcc": bcc_list,
            "subject": subject,
            "size": len(msg.as_string()),
            "attachments_count": attachments_count,
        }, message="邮件发送成功")

    except Exception as e:
        output_json("error", message=f"发送邮件失败: {e}")
    finally:
        if conn:
            try:
                conn.quit()
            except Exception:
                pass


def cmd_reply(args):
    """回复邮件"""
    config = require_config()
    uid = args.uid
    body = args.body or ""
    reply_all = args.all
    folder = args.folder or "INBOX"
    folder = FOLDER_MAP.get(folder, folder)

    conn = None
    try:
        conn = get_imap_connection(config)
        conn.select(folder, readonly=True)

        # 获取原邮件
        status, msg_data = conn.uid("fetch", str(uid), "(RFC822)")
        if status != "OK" or not msg_data or not msg_data[0]:
            output_json("error", message=f"未找到 UID={uid} 的邮件")
            return

        raw_email = msg_data[0][1]
        orig_msg = email.message_from_bytes(raw_email)
        orig_headers = parse_email_headers(orig_msg)

        # 构建回复
        reply_msg = MIMEMultipart()
        reply_msg["From"] = config["email"]

        # 回复地址
        reply_to = orig_msg.get("Reply-To") or orig_msg.get("From", "")
        reply_to = decode_header_value(reply_to)
        to_addrs = [reply_to]

        if reply_all:
            # 回复全部
            orig_to = decode_header_value(orig_msg.get("To", ""))
            orig_cc = decode_header_value(orig_msg.get("Cc", ""))
            if orig_to:
                for addr in orig_to.split(","):
                    addr = addr.strip()
                    if addr and config["email"] not in addr:
                        to_addrs.append(addr)
            cc_list = []
            if orig_cc:
                for addr in orig_cc.split(","):
                    addr = addr.strip()
                    if addr and config["email"] not in addr:
                        cc_list.append(addr)
            if cc_list:
                reply_msg["Cc"] = ", ".join(cc_list)

        reply_msg["To"] = ", ".join(to_addrs)

        # 主题
        orig_subject = orig_headers["subject"]
        if not orig_subject.startswith("Re:"):
            reply_msg["Subject"] = f"Re: {orig_subject}"
        else:
            reply_msg["Subject"] = orig_subject

        reply_msg["Date"] = formatdate(localtime=True)
        reply_msg["Message-ID"] = make_msgid()

        # In-Reply-To 和 References
        orig_msg_id = orig_msg.get("Message-ID", "")
        if orig_msg_id:
            reply_msg["In-Reply-To"] = orig_msg_id
            orig_refs = orig_msg.get("References", "")
            refs = f"{orig_refs} {orig_msg_id}".strip() if orig_refs else orig_msg_id
            reply_msg["References"] = refs

        # 正文 + 引用原文
        orig_body = parse_email_body(orig_msg)["body_text"]
        quoted_body = "\n\n" + "─" * 40 + "\n"
        quoted_body += f"原始邮件来自: {orig_headers['from']}\n"
        quoted_body += f"日期: {orig_headers['date']}\n"
        quoted_body += f"主题: {orig_headers['subject']}\n"
        quoted_body += "─" * 40 + "\n"
        for line in orig_body.split("\n"):
            quoted_body += f"> {line}\n"

        reply_msg.attach(MIMEText(body + quoted_body, "plain", "utf-8"))

        # 发送
        smtp_conn = get_smtp_connection(config)
        try:
            smtp_conn.sendmail(config["email"], to_addrs, reply_msg.as_string())
            output_json("success", data={
                "uid": str(uid),
                "to": to_addrs,
                "subject": reply_msg["Subject"],
            }, message="回复邮件成功")
        finally:
            smtp_conn.quit()

    except Exception as e:
        output_json("error", message=f"回复邮件失败: {e}")
    finally:
        if conn:
            try:
                conn.logout()
            except Exception:
                pass


def cmd_forward(args):
    """转发邮件"""
    config = require_config()
    uid = args.uid
    to_list = [addr.strip() for addr in args.to.split(",") if addr.strip()]
    note = args.note or ""
    folder = args.folder or "INBOX"
    folder = FOLDER_MAP.get(folder, folder)

    if not to_list:
        output_json("error", message="请提供转发目标地址 (--to)")
        return

    conn = None
    try:
        conn = get_imap_connection(config)
        conn.select(folder, readonly=True)

        status, msg_data = conn.uid("fetch", str(uid), "(RFC822)")
        if status != "OK" or not msg_data or not msg_data[0]:
            output_json("error", message=f"未找到 UID={uid} 的邮件")
            return

        raw_email = msg_data[0][1]
        orig_msg = email.message_from_bytes(raw_email)
        orig_headers = parse_email_headers(orig_msg)

        # 构建转发邮件
        fwd_msg = MIMEMultipart()
        fwd_msg["From"] = config["email"]
        fwd_msg["To"] = ", ".join(to_list)

        orig_subject = orig_headers["subject"]
        if not orig_subject.startswith("Fwd:"):
            fwd_msg["Subject"] = f"Fwd: {orig_subject}"
        else:
            fwd_msg["Subject"] = orig_subject

        fwd_msg["Date"] = formatdate(localtime=True)
        fwd_msg["Message-ID"] = make_msgid()

        # 转发说明
        fwd_body = ""
        if note:
            fwd_body = note + "\n\n"
        fwd_body += "─" * 40 + "\n"
        fwd_body += "---------- 转发邮件 ----------\n"
        fwd_body += f"来自: {orig_headers['from']}\n"
        fwd_body += f"日期: {orig_headers['date']}\n"
        fwd_body += f"主题: {orig_headers['subject']}\n"
        fwd_body += f"收件人: {orig_headers['to']}\n"
        fwd_body += "─" * 40 + "\n\n"

        orig_body = parse_email_body(orig_msg)["body_text"]
        fwd_body += orig_body

        fwd_msg.attach(MIMEText(fwd_body, "plain", "utf-8"))

        # 附加原始附件
        for part in orig_msg.walk():
            content_disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in content_disposition:
                fwd_msg.attach(part)

        smtp_conn = get_smtp_connection(config)
        try:
            smtp_conn.sendmail(config["email"], to_list, fwd_msg.as_string())
            output_json("success", data={
                "uid": str(uid),
                "to": to_list,
                "subject": fwd_msg["Subject"],
            }, message="转发邮件成功")
        finally:
            smtp_conn.quit()

    except Exception as e:
        output_json("error", message=f"转发邮件失败: {e}")
    finally:
        if conn:
            try:
                conn.logout()
            except Exception:
                pass


# ============================================================
# 管理命令
# ============================================================


def cmd_manage_mark(args):
    """标记邮件"""
    config = require_config()
    uid = args.uid
    flag = args.flag
    folder = args.folder or "INBOX"
    folder = FOLDER_MAP.get(folder, folder)

    conn = None
    try:
        conn = get_imap_connection(config)
        conn.select(folder, readonly=False)

        flag_map = {
            "read": ("+FLAGS", "\\Seen"),
            "unread": ("-FLAGS", "\\Seen"),
            "starred": ("+FLAGS", "\\Flagged"),
            "unstarred": ("-FLAGS", "\\Flagged"),
        }

        if flag not in flag_map:
            output_json("error", message=f"不支持的标记: {flag}，支持: read/unread/starred/unstarred")
            return

        op, imap_flag = flag_map[flag]
        status, _ = conn.uid("store", str(uid), op, imap_flag)

        if status == "OK":
            flag_names = {"read": "已读", "unread": "未读", "starred": "星标", "unstarred": "取消星标"}
            output_json("success", data={"uid": str(uid), "action": "mark", "flag": flag},
                        message=f"邮件已标记为{flag_names.get(flag, flag)}")
        else:
            output_json("error", message=f"标记邮件失败")

    except Exception as e:
        output_json("error", message=f"标记邮件失败: {e}")
    finally:
        if conn:
            try:
                conn.close()
                conn.logout()
            except Exception:
                pass


def cmd_manage_delete(args):
    """删除邮件"""
    config = require_config()
    uid = args.uid
    folder = args.folder or "INBOX"
    folder = FOLDER_MAP.get(folder, folder)

    conn = None
    try:
        conn = get_imap_connection(config)
        conn.select(folder, readonly=False)

        # 标记为删除
        status, _ = conn.uid("store", str(uid), "+FLAGS", "\\Deleted")
        if status == "OK":
            conn.expunge()
            output_json("success", data={"uid": str(uid), "action": "delete"},
                        message="邮件已删除")
        else:
            output_json("error", message="删除邮件失败")

    except Exception as e:
        output_json("error", message=f"删除邮件失败: {e}")
    finally:
        if conn:
            try:
                conn.close()
                conn.logout()
            except Exception:
                pass


def cmd_manage_move(args):
    """移动邮件"""
    config = require_config()
    uid = args.uid
    target_folder = args.folder
    source_folder = args.source or "INBOX"
    source_folder = FOLDER_MAP.get(source_folder, source_folder)
    target_folder = FOLDER_MAP.get(target_folder, target_folder)

    conn = None
    try:
        conn = get_imap_connection(config)
        conn.select(source_folder, readonly=False)

        # 复制到目标文件夹
        status, _ = conn.uid("copy", str(uid), target_folder)
        if status == "OK":
            # 从原文件夹删除
            conn.uid("store", str(uid), "+FLAGS", "\\Deleted")
            conn.expunge()
            output_json("success", data={"uid": str(uid), "action": "move",
                                         "from": source_folder, "to": target_folder},
                        message=f"邮件已从 {source_folder} 移动到 {target_folder}")
        else:
            output_json("error", message=f"移动邮件失败，目标文件夹: {target_folder}")

    except Exception as e:
        output_json("error", message=f"移动邮件失败: {e}")
    finally:
        if conn:
            try:
                conn.close()
                conn.logout()
            except Exception:
                pass


# ============================================================
# 统计命令
# ============================================================


def cmd_stats_today(args):
    """今日邮件统计"""
    config = require_config()
    today = datetime.now().strftime("%d-%b-%Y")

    conn = None
    try:
        conn = get_imap_connection(config)

        stats = {
            "period": datetime.now().strftime("%Y-%m-%d"),
            "total": 0,
            "unread": 0,
            "by_folder": {},
            "top_senders": [],
        }

        folders = ["INBOX", "Sent Messages", "Drafts", "Trash", "Junk"]
        all_senders = {}

        for folder in folders:
            try:
                status, _ = conn.select(folder, readonly=True)
                if status != "OK":
                    continue

                # 今日所有邮件
                status, ids = conn.search(None, f'SINCE {today}')
                if status != "OK":
                    continue

                id_list = ids[0].split()
                count = len(id_list)
                stats["by_folder"][folder] = count
                stats["total"] += count

                # 未读
                status, unread_ids = conn.search(None, "UNSEEN", f'SINCE {today}')
                if status == "OK":
                    stats["unread"] += len(unread_ids[0].split())

                # 发件人统计（只统计 INBOX）
                if folder == "INBOX" and id_list:
                    for mid in id_list[-50:]:  # 最多分析50封
                        try:
                            status, header_data = conn.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM)])")
                            if status == "OK" and header_data and header_data[0]:
                                msg = email.message_from_bytes(header_data[0][1])
                                sender = decode_header_value(msg.get("From", ""))
                                if sender:
                                    # 提取 email 地址
                                    addr_match = re.search(r'<([^>]+)>', sender)
                                    addr = addr_match.group(1) if addr_match else sender
                                    all_senders[addr] = all_senders.get(addr, 0) + 1
                        except Exception:
                            pass
            except Exception:
                continue

        # Top 发件人
        stats["top_senders"] = [
            {"sender": s, "count": c}
            for s, c in sorted(all_senders.items(), key=lambda x: x[1], reverse=True)[:10]
        ]

        output_json("success", data=stats, message=f"今日共 {stats['total']} 封邮件，{stats['unread']} 封未读")

    except Exception as e:
        output_json("error", message=f"统计失败: {e}")
    finally:
        if conn:
            try:
                conn.logout()
            except Exception:
                pass


def cmd_stats_range(args):
    """日期范围统计"""
    config = require_config()
    since = args.since
    until = args.until

    if not since:
        output_json("error", message="请提供 --since 参数 (格式: 2026-04-01)")
        return

    # 转换日期格式 (2026-04-01 -> 01-Apr-2026)
    try:
        since_dt = datetime.strptime(since, "%Y-%m-%d")
        since_imap = since_dt.strftime("%d-%b-%Y")
    except ValueError:
        output_json("error", message="日期格式错误，请使用 YYYY-MM-DD")
        return

    until_imap = None
    if until:
        try:
            until_dt = datetime.strptime(until, "%Y-%m-%d")
            until_imap = until_dt.strftime("%d-%b-%Y")
        except ValueError:
            output_json("error", message="日期格式错误，请使用 YYYY-MM-DD")
            return

    conn = None
    try:
        conn = get_imap_connection(config)

        stats = {
            "period": f"{since} ~ {until or '今天'}",
            "total": 0,
            "unread": 0,
            "by_folder": {},
            "top_senders": [],
        }

        all_senders = {}
        folders = ["INBOX", "Sent Messages", "Drafts", "Trash", "Junk"]

        for folder in folders:
            try:
                status, _ = conn.select(folder, readonly=True)
                if status != "OK":
                    continue

                criteria = [f'SINCE {since_imap}']
                if until_imap:
                    criteria.append(f'BEFORE {until_imap}')

                status, ids = conn.search(None, *criteria)
                if status != "OK":
                    continue

                id_list = ids[0].split()
                count = len(id_list)
                stats["by_folder"][folder] = count
                stats["total"] += count

                # 未读
                criteria_unread = criteria + ["UNSEEN"]
                status, unread_ids = conn.search(None, *criteria_unread)
                if status == "OK":
                    stats["unread"] += len(unread_ids[0].split())

                # 发件人统计
                if folder == "INBOX" and id_list:
                    for mid in id_list[-50:]:
                        try:
                            status, header_data = conn.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM)])")
                            if status == "OK" and header_data and header_data[0]:
                                msg = email.message_from_bytes(header_data[0][1])
                                sender = decode_header_value(msg.get("From", ""))
                                if sender:
                                    addr_match = re.search(r'<([^>]+)>', sender)
                                    addr = addr_match.group(1) if addr_match else sender
                                    all_senders[addr] = all_senders.get(addr, 0) + 1
                        except Exception:
                            pass
            except Exception:
                continue

        stats["top_senders"] = [
            {"sender": s, "count": c}
            for s, c in sorted(all_senders.items(), key=lambda x: x[1], reverse=True)[:10]
        ]

        output_json("success", data=stats,
                    message=f"{stats['period']} 共 {stats['total']} 封邮件，{stats['unread']} 封未读")

    except Exception as e:
        output_json("error", message=f"统计失败: {e}")
    finally:
        if conn:
            try:
                conn.logout()
            except Exception:
                pass


def cmd_stats_by_sender(args):
    """按发件人统计"""
    config = require_config()
    limit = args.limit or 10
    days = args.days or 30

    since_date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")

    conn = None
    try:
        conn = get_imap_connection(config)

        senders = {}
        try:
            conn.select("INBOX", readonly=True)
            status, ids = conn.search(None, f'SINCE {since_date}')
            if status == "OK":
                id_list = ids[0].split()
                for mid in id_list:
                    try:
                        status, header_data = conn.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM DATE)])")
                        if status == "OK" and header_data and header_data[0]:
                            msg = email.message_from_bytes(header_data[0][1])
                            sender = decode_header_value(msg.get("From", ""))
                            date_str = decode_header_value(msg.get("Date", ""))

                            if sender:
                                addr_match = re.search(r'<([^>]+)>', sender)
                                addr = addr_match.group(1) if addr_match else sender

                                if addr not in senders:
                                    # 提取日期
                                    latest = ""
                                    try:
                                        dt = email.utils.parsedate_to_datetime(date_str)
                                        latest = dt.strftime("%Y-%m-%d")
                                    except Exception:
                                        latest = date_str
                                    senders[addr] = {"sender": sender, "count": 0, "latest": latest}
                                senders[addr]["count"] += 1

                                # 更新最新日期
                                try:
                                    dt = email.utils.parsedate_to_datetime(date_str)
                                    new_date = dt.strftime("%Y-%m-%d")
                                    if new_date > senders[addr]["latest"]:
                                        senders[addr]["latest"] = new_date
                                except Exception:
                                    pass
                    except Exception:
                        pass
        except Exception:
            pass

        # 排序
        sorted_senders = sorted(senders.values(), key=lambda x: x["count"], reverse=True)[:limit]

        output_json("success", data={
            "period": f"最近{days}天",
            "senders": sorted_senders,
        }, message=f"Top {len(sorted_senders)} 发件人统计（最近 {days} 天）")

    except Exception as e:
        output_json("error", message=f"统计失败: {e}")
    finally:
        if conn:
            try:
                conn.logout()
            except Exception:
                pass


def cmd_stats_folders(args):
    """文件夹概览"""
    config = require_config()

    conn = None
    try:
        conn = get_imap_connection(config)

        # 列出所有文件夹
        status, folder_list = conn.list()
        folders_info = []

        # 网易常用文件夹
        check_folders = {
            "INBOX": "收件箱",
            "Sent Messages": "已发送",
            "Drafts": "草稿",
            "Trash": "已删除",
            "Junk": "垃圾邮件",
            "Virus": "病毒邮件",
        }

        for folder_name, display_name in check_folders.items():
            try:
                status, data = conn.select(folder_name, readonly=True)
                if status == "OK":
                    total = int(data[0])

                    # 获取未读数
                    unread = 0
                    status_s, search_data = conn.search(None, "UNSEEN")
                    if status_s == "OK":
                        unread = len(search_data[0].split())

                    folders_info.append({
                        "name": folder_name,
                        "display": display_name,
                        "total": total,
                        "unread": unread,
                    })
            except Exception:
                continue

        output_json("success", data={"folders": folders_info},
                    message=f"共 {len(folders_info)} 个文件夹")

    except Exception as e:
        output_json("error", message=f"获取文件夹概览失败: {e}")
    finally:
        if conn:
            try:
                conn.logout()
            except Exception:
                pass


# ============================================================
# 主入口
# ============================================================


def main():
    parser = argparse.ArgumentParser(
        description="Mail-126: 网易 126.com 邮箱管理 CLI",
        prog="mail_manager.py",
    )
    subparsers = parser.add_subparsers(dest="module", help="功能模块")

    # --- init ---
    subparsers.add_parser("init", help="初始化数据目录")

    # --- config ---
    config_parser = subparsers.add_parser("config", help="配置管理")
    config_sub = config_parser.add_subparsers(dest="action", help="配置操作")

    config_setup = config_sub.add_parser("setup", help="配置邮箱账号")
    config_setup.add_argument("--email", required=True, help="邮箱地址")
    config_setup.add_argument("--auth-code", required=True, help="授权码")

    config_sub.add_parser("verify", help="验证连接")

    # --- inbox ---
    inbox_parser = subparsers.add_parser("inbox", help="收件箱")
    inbox_sub = inbox_parser.add_subparsers(dest="action", help="收件箱操作")

    # inbox list
    inbox_list = inbox_sub.add_parser("list", help="列出邮件")
    inbox_list.add_argument("--folder", default="INBOX", help="文件夹 (默认 INBOX)")
    inbox_list.add_argument("--limit", type=int, default=10, help="数量限制")
    inbox_list.add_argument("--offset", type=int, default=0, help="偏移量")
    inbox_list.add_argument("--unread", action="store_true", help="仅未读")

    # inbox read
    inbox_read = inbox_sub.add_parser("read", help="读取邮件")
    inbox_read.add_argument("--uid", required=True, help="邮件 UID")
    inbox_read.add_argument("--folder", default="INBOX", help="文件夹")

    # inbox search
    inbox_search = inbox_sub.add_parser("search", help="搜索邮件")
    inbox_search.add_argument("--from", dest="from_sender", help="发件人")
    inbox_search.add_argument("--to", help="收件人")
    inbox_search.add_argument("--subject", help="主题")
    inbox_search.add_argument("--since", help="起始日期 (YYYY-MM-DD)")
    inbox_search.add_argument("--until", help="结束日期 (YYYY-MM-DD)")
    inbox_search.add_argument("--folder", default="INBOX", help="文件夹")
    inbox_search.add_argument("--limit", type=int, default=20, help="数量限制")
    inbox_search.add_argument("--offset", type=int, default=0, help="偏移量")

    # inbox download
    inbox_download = inbox_sub.add_parser("download", help="下载附件")
    inbox_download.add_argument("--uid", required=True, help="邮件 UID")
    inbox_download.add_argument("--folder", default="INBOX", help="文件夹")
    inbox_download.add_argument("--output-dir", help="保存目录")
    inbox_download.add_argument("--attachment", help="指定附件名")

    # --- send ---
    send_parser = subparsers.add_parser("send", help="发送邮件")
    send_parser.add_argument("--to", required=True, help="收件人 (多个用逗号分隔)")
    send_parser.add_argument("--subject", help="主题")
    send_parser.add_argument("--body", help="正文")
    send_parser.add_argument("--html", help="HTML 正文")
    send_parser.add_argument("--cc", help="抄送")
    send_parser.add_argument("--bcc", help="密送")
    send_parser.add_argument("--attachments", help="附件路径 (多个用逗号分隔)")

    # --- reply ---
    reply_parser = subparsers.add_parser("reply", help="回复邮件")
    reply_parser.add_argument("--uid", required=True, help="原邮件 UID")
    reply_parser.add_argument("--body", required=True, help="回复内容")
    reply_parser.add_argument("--folder", default="INBOX", help="文件夹")
    reply_parser.add_argument("--all", action="store_true", help="回复全部")

    # --- forward ---
    forward_parser = subparsers.add_parser("forward", help="转发邮件")
    forward_parser.add_argument("--uid", required=True, help="原邮件 UID")
    forward_parser.add_argument("--to", required=True, help="转发目标 (多个用逗号分隔)")
    forward_parser.add_argument("--note", help="转发说明")
    forward_parser.add_argument("--folder", default="INBOX", help="文件夹")

    # --- manage ---
    manage_parser = subparsers.add_parser("manage", help="邮件管理")
    manage_sub = manage_parser.add_subparsers(dest="action", help="管理操作")

    manage_mark = manage_sub.add_parser("mark", help="标记邮件")
    manage_mark.add_argument("--uid", required=True, help="邮件 UID")
    manage_mark.add_argument("--flag", required=True,
                             choices=["read", "unread", "starred", "unstarred"],
                             help="标记类型")
    manage_mark.add_argument("--folder", default="INBOX", help="文件夹")

    manage_delete = manage_sub.add_parser("delete", help="删除邮件")
    manage_delete.add_argument("--uid", required=True, help="邮件 UID")
    manage_delete.add_argument("--folder", default="INBOX", help="文件夹")

    manage_move = manage_sub.add_parser("move", help="移动邮件")
    manage_move.add_argument("--uid", required=True, help="邮件 UID")
    manage_move.add_argument("--folder", required=True, help="目标文件夹")
    manage_move.add_argument("--source", default="INBOX", help="源文件夹")

    # --- stats ---
    stats_parser = subparsers.add_parser("stats", help="邮件统计")
    stats_sub = stats_parser.add_subparsers(dest="action", help="统计类型")

    stats_sub.add_parser("today", help="今日统计")

    stats_range = stats_sub.add_parser("range", help="日期范围统计")
    stats_range.add_argument("--since", default=None, help="起始日期 (YYYY-MM-DD)")
    stats_range.add_argument("--until", help="结束日期 (YYYY-MM-DD)")

    stats_sender = stats_sub.add_parser("by-sender", help="按发件人统计")
    stats_sender.add_argument("--limit", type=int, default=10, help="数量限制")
    stats_sender.add_argument("--days", type=int, default=30, help="统计天数")

    stats_sub.add_parser("folders", help="文件夹概览")

    # 解析参数
    args = parser.parse_args()

    if not args.module:
        parser.print_help()
        return

    # 路由
    if args.module == "init":
        cmd_init()
    elif args.module == "config":
        if args.action == "setup":
            cmd_config_setup(args)
        elif args.action == "verify":
            cmd_config_verify(args)
        else:
            config_parser.print_help()
    elif args.module == "inbox":
        if args.action == "list":
            cmd_inbox_list(args)
        elif args.action == "read":
            cmd_inbox_read(args)
        elif args.action == "search":
            cmd_inbox_search(args)
        elif args.action == "download":
            cmd_inbox_download(args)
        else:
            inbox_parser.print_help()
    elif args.module == "send":
        cmd_send(args)
    elif args.module == "reply":
        cmd_reply(args)
    elif args.module == "forward":
        cmd_forward(args)
    elif args.module == "manage":
        if args.action == "mark":
            cmd_manage_mark(args)
        elif args.action == "delete":
            cmd_manage_delete(args)
        elif args.action == "move":
            cmd_manage_move(args)
        else:
            manage_parser.print_help()
    elif args.module == "stats":
        if args.action == "today":
            cmd_stats_today(args)
        elif args.action == "range":
            cmd_stats_range(args)
        elif args.action == "by-sender":
            cmd_stats_by_sender(args)
        elif args.action == "folders":
            cmd_stats_folders(args)
        else:
            stats_parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
