#!/usr/bin/env python3
"""
email_reader.py - POP3 邮件只读工具
支持 163、QQ、Gmail、Outlook 等任意 POP3 邮箱

配置方式（按优先级）：
1. 命令行参数 --user / --pass_ / --server / --port
2. 环境变量 EMAIL_USER / EMAIL_PASS / POP3_SERVER / POP3_PORT
3. 脚本同目录的 .email_config 文件（INI 格式）

用法示例：
  python3 email_reader.py count
  python3 email_reader.py subjects --n 10
  python3 email_reader.py list --n 5
  python3 email_reader.py read --index 42
  python3 email_reader.py search --keyword 验证码 --range 100

输出均为 JSON，方便 agent 解析。
"""

import argparse
import configparser
import email
import json
import os
import poplib
import re
import sys
from email.header import decode_header
from email.utils import parsedate_to_datetime
from pathlib import Path

# ─── 配置加载 ────────────────────────────────────────────────────────────────

def load_config(args):
    """从 CLI / 环境变量 / .email_config 三层加载配置，返回 dict"""
    cfg = {
        "user": None,
        "pass_": None,
        "server": None,
        "port": 995,
    }

    # 层 3：.email_config 文件
    config_file = Path(__file__).parent / ".email_config"
    if config_file.exists():
        parser = configparser.ConfigParser()
        parser.read(config_file)
        if "email" in parser:
            s = parser["email"]
            cfg["user"]   = s.get("user",   cfg["user"])
            cfg["pass_"]  = s.get("pass_",  cfg["pass_"])
            cfg["server"] = s.get("server", cfg["server"])
            cfg["port"]   = int(s.get("port", cfg["port"]))

    # 层 2：环境变量
    cfg["user"]   = os.environ.get("EMAIL_USER",   cfg["user"])
    cfg["pass_"]  = os.environ.get("EMAIL_PASS",   cfg["pass_"])
    cfg["server"] = os.environ.get("POP3_SERVER",  cfg["server"])
    cfg["port"]   = int(os.environ.get("POP3_PORT", cfg["port"]))

    # 层 1：命令行参数（最高优先级）
    if args.user:   cfg["user"]   = args.user
    if args.pass_:  cfg["pass_"]  = args.pass_
    if args.server: cfg["server"] = args.server
    if args.port:   cfg["port"]   = args.port

    # 校验
    missing = [k for k in ("user", "pass_", "server") if not cfg[k]]
    if missing:
        print(json.dumps({
            "error": f"缺少必要配置项：{missing}。"
                     "请通过环境变量、.email_config 文件或命令行参数提供。"
        }, ensure_ascii=False))
        sys.exit(1)

    return cfg

# ─── POP3 连接 ───────────────────────────────────────────────────────────────

def connect(cfg):
    server = poplib.POP3_SSL(cfg["server"], cfg["port"])
    server.user(cfg["user"])
    server.pass_(cfg["pass_"])
    return server

def disconnect(server):
    try:
        server.quit()
    except Exception:
        pass

# ─── 解析工具 ─────────────────────────────────────────────────────────────────

def decode_str(s):
    if s is None:
        return ""
    decoded_parts = decode_header(s)
    result = ""
    for part, enc in decoded_parts:
        if isinstance(part, bytes):
            result += part.decode(enc if enc else "utf-8", errors="ignore")
        else:
            result += part
    return result

def get_email_body(msg):
    text_body = ""
    html_body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            charset = part.get_content_charset() or "utf-8"
            if ct == "text/plain":
                text_body = part.get_payload(decode=True).decode(charset, errors="ignore")
            elif ct == "text/html":
                html_body = part.get_payload(decode=True).decode(charset, errors="ignore")
    else:
        charset = msg.get_content_charset() or "utf-8"
        payload = msg.get_payload(decode=True)
        if payload:
            ct = msg.get_content_type()
            if ct == "text/plain":
                text_body = payload.decode(charset, errors="ignore")
            elif ct == "text/html":
                html_body = payload.decode(charset, errors="ignore")

    if text_body:
        return text_body.strip()
    elif html_body:
        clean = re.sub(r"<[^>]+>", "", html_body)
        return clean.strip()
    return "（无正文内容）"

def get_attachments(msg):
    attachments = []
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            filename = decode_str(part.get_filename())
            attachments.append({
                "filename": filename,
                "content_type": part.get_content_type(),
                "size": len(part.get_payload(decode=True) or b""),
            })
    return attachments

def parse_email(raw_lines):
    msg = email.message_from_bytes(b"\r\n".join(raw_lines))
    try:
        date = parsedate_to_datetime(msg.get("Date")).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        date = msg.get("Date", "未知时间")
    return {
        "subject":     decode_str(msg.get("Subject")),
        "from":        decode_str(msg.get("From")),
        "to":          decode_str(msg.get("To")),
        "date":        date,
        "body":        get_email_body(msg),
        "attachments": get_attachments(msg),
    }

def parse_header_only(raw_lines):
    msg = email.message_from_bytes(b"\r\n".join(raw_lines))
    try:
        date = parsedate_to_datetime(msg.get("Date")).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        date = msg.get("Date", "未知时间")
    return {
        "subject": decode_str(msg.get("Subject")),
        "from":    decode_str(msg.get("From")),
        "date":    date,
    }

# ─── 功能函数 ─────────────────────────────────────────────────────────────────

def cmd_count(cfg, _args):
    server = connect(cfg)
    count = len(server.list()[1])
    disconnect(server)
    return {"total": count}

def cmd_subjects(cfg, args):
    n = args.n
    server = connect(cfg)
    total = len(server.list()[1])
    results = []
    for i in range(total, max(total - n, 0), -1):
        _, lines, _ = server.top(i, 0)
        item = parse_header_only(lines)
        item["index"] = i
        results.append(item)
    disconnect(server)
    return {"total": total, "emails": results}

def cmd_list(cfg, args):
    n = args.n
    server = connect(cfg)
    total = len(server.list()[1])
    results = []
    for i in range(total, max(total - n, 0), -1):
        _, lines, _ = server.retr(i)
        item = parse_email(lines)
        item["index"] = i
        results.append(item)
    disconnect(server)
    return {"total": total, "emails": results}

def cmd_read(cfg, args):
    server = connect(cfg)
    _, lines, _ = server.retr(args.index)
    item = parse_email(lines)
    item["index"] = args.index
    disconnect(server)
    return item

def cmd_search(cfg, args):
    keyword = args.keyword
    search_range = args.range
    server = connect(cfg)
    total = len(server.list()[1])
    results = []
    for i in range(total, max(total - search_range, 0), -1):
        _, lines, _ = server.top(i, 0)
        item = parse_header_only(lines)
        if keyword.lower() in item["subject"].lower():
            item["index"] = i
            results.append(item)
    disconnect(server)
    return {"keyword": keyword, "found": len(results), "emails": results}

# ─── CLI 入口 ─────────────────────────────────────────────────────────────────

def build_parser():
    p = argparse.ArgumentParser(
        description="POP3 邮件只读工具（JSON 输出）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # 全局凭证参数
    p.add_argument("--user",   help="邮箱账号（覆盖环境变量/配置文件）")
    p.add_argument("--pass_",  help="邮箱密码/授权码（覆盖环境变量/配置文件）")
    p.add_argument("--server", help="POP3 服务器地址（覆盖环境变量/配置文件）")
    p.add_argument("--port",   type=int, help="POP3 端口，默认 995")

    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("count", help="获取邮件总数")

    s = sub.add_parser("subjects", help="获取最近 n 封邮件标题列表（仅头部，速度快）")
    s.add_argument("--n", type=int, default=10, help="获取数量，默认 10")

    l = sub.add_parser("list", help="获取最近 n 封邮件完整内容（含正文）")
    l.add_argument("--n", type=int, default=5, help="获取数量，默认 5")

    r = sub.add_parser("read", help="按序号读取指定邮件完整内容")
    r.add_argument("--index", type=int, required=True, help="邮件序号（1=最旧，total=最新）")

    se = sub.add_parser("search", help="在最近 n 封中搜索主题含关键词的邮件")
    se.add_argument("--keyword", required=True, help="搜索关键词")
    se.add_argument("--range",   type=int, default=50, help="搜索范围（最近 n 封），默认 50")

    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    cfg = load_config(args)

    dispatch = {
        "count":    cmd_count,
        "subjects": cmd_subjects,
        "list":     cmd_list,
        "read":     cmd_read,
        "search":   cmd_search,
    }

    result = dispatch[args.cmd](cfg, args)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
