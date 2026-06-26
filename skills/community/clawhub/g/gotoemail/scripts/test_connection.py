#!/usr/bin/env python3
"""
GoToEmail — test_connection.py
测试 IMAP/SMTP 连接并返回结果。

输入（JSON via stdin）：
{
  "email":      "user@163.com",
  "password":   "授权码或App密码",
  "imap_host":  "imap.163.com",   // 可选，163/QQ/Gmail/Yahoo 可自动识别
  "imap_port":  993,               // 可选，默认 993
  "smtp_host":  "smtp.163.com",   // 可选
  "smtp_port":  465                // 可选，默认 465
}

输出（JSON）：
成功: {"ok": true, "message": "邮箱 xxx 连接测试通过", "config": {...}}
失败: {"ok": false, "error": "IMAP认证失败: ..."}
"""

import imaplib
import smtplib
import ssl
import json
import sys

# 内置服务器配置（domain → provider key）
PROVIDERS = {
    "163.com":    {"imap": ("imap.163.com",           993), "smtp": ("smtp.163.com",           465)},
    "126.com":    {"imap": ("imap.126.com",           993), "smtp": ("smtp.126.com",           465)},
    "yeah.net":   {"imap": ("imap.yeah.net",          993), "smtp": ("smtp.yeah.net",          465)},
    "qq.com":     {"imap": ("imap.qq.com",            993), "smtp": ("smtp.qq.com",            465)},
    "foxmail.com":{"imap": ("imap.qq.com",            993), "smtp": ("smtp.qq.com",            465)},
    "gmail.com":  {"imap": ("imap.gmail.com",         993), "smtp": ("smtp.gmail.com",         465)},
    "yahoo.com":  {"imap": ("imap.mail.yahoo.com",    993), "smtp": ("smtp.mail.yahoo.com",    465)},
    "ymail.com":  {"imap": ("imap.mail.yahoo.com",    993), "smtp": ("smtp.mail.yahoo.com",    465)},
    "yahoo.co.jp":{"imap": ("imap.mail.yahoo.co.jp",  993), "smtp": ("smtp.mail.yahoo.co.jp",  465)},
}


def detect_servers(email: str, data: dict):
    """从邮箱地址自动识别服务器，或使用 data 中的自定义值。"""
    domain = email.split("@")[-1].lower() if "@" in email else ""
    cfg = PROVIDERS.get(domain)

    imap_host = data.get("imap_host") or (cfg["imap"][0] if cfg else None)
    imap_port = int(data.get("imap_port") or (cfg["imap"][1] if cfg else 993))
    smtp_host = data.get("smtp_host") or (cfg["smtp"][0] if cfg else None)
    smtp_port = int(data.get("smtp_port") or (cfg["smtp"][1] if cfg else 465))

    return imap_host, imap_port, smtp_host, smtp_port


def test_imap(host: str, port: int, email: str, password: str) -> dict:
    try:
        ctx = ssl.create_default_context()
        conn = imaplib.IMAP4_SSL(host, port, ssl_context=ctx)
        conn.login(email, password)
        conn.logout()
        return {"ok": True}
    except imaplib.IMAP4.error as e:
        return {"ok": False, "error": f"IMAP认证失败: {e}"}
    except OSError as e:
        return {"ok": False, "error": f"IMAP无法连接 {host}:{port} — {e}"}
    except Exception as e:
        return {"ok": False, "error": f"IMAP错误: {e}"}


def test_smtp(host: str, port: int, email: str, password: str) -> dict:
    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=ctx) as s:
            s.login(email, password)
        return {"ok": True}
    except smtplib.SMTPAuthenticationError as e:
        return {"ok": False, "error": f"SMTP认证失败: {e}"}
    except OSError as e:
        return {"ok": False, "error": f"SMTP无法连接 {host}:{port} — {e}"}
    except Exception as e:
        return {"ok": False, "error": f"SMTP错误: {e}"}


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "error": f"JSON解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        print(json.dumps({"ok": False, "error": "缺少 email 或 password"}, ensure_ascii=False))
        sys.exit(1)

    imap_host, imap_port, smtp_host, smtp_port = detect_servers(email, data)

    if not imap_host or not smtp_host:
        print(json.dumps({
            "ok": False,
            "error": "未识别邮箱提供商，请提供 imap_host 和 smtp_host"
        }, ensure_ascii=False))
        sys.exit(1)

    imap_r = test_imap(imap_host, imap_port, email, password)
    smtp_r = test_smtp(smtp_host, smtp_port, email, password)

    ok = imap_r["ok"] and smtp_r["ok"]
    result = {"ok": ok, "imap": imap_r, "smtp": smtp_r}

    if ok:
        result["message"] = f"邮箱 {email} 连接测试通过"
        result["config"] = {
            "email": email,
            "imap": {"host": imap_host, "port": imap_port},
            "smtp": {"host": smtp_host, "port": smtp_port},
        }
    else:
        result["error"] = (
            imap_r.get("error") or smtp_r.get("error") or "连接失败"
        )

    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
