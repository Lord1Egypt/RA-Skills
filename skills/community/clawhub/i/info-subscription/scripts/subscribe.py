#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信息订阅技能 - OpenClaw Skill 脚本
用法:
  python3 subscribe.py "<邮箱>"        # 订阅（每个实例只能绑定一个邮箱，重复设置会替换旧邮箱）
  python3 subscribe.py "trigger"       # 手动触发推送（自动使用已绑定邮箱）
  python3 subscribe.py "unsubscribe"   # 取消订阅（自动使用已绑定邮箱）
  python3 subscribe.py "status"        # 查看当前绑定状态
"""

import sys
import os
import json

try:
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
    from urllib.error import URLError, HTTPError
except ImportError:
    from urllib2 import Request, urlopen, URLError, HTTPError
    from urllib import urlencode

# 后端服务地址（通过 ai-tools-center 对外暴露，转发到 crawler）
API_BASE = "https://adeeptools.com/api/manager/announcement"

# 本地配置文件：存储当前实例绑定的邮箱
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".openclaw", "skills", "info-subscription")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def load_config():
    """读取本地配置"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_config(config):
    """保存本地配置"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def get_bound_email():
    """获取当前绑定的邮箱"""
    return load_config().get("email")


def set_bound_email(email):
    """设置绑定邮箱"""
    config = load_config()
    config["email"] = email
    save_config(config)


def clear_bound_email():
    """清除绑定邮箱"""
    config = load_config()
    config.pop("email", None)
    save_config(config)


def parse_response(body):
    """解析响应，兼容 center 代理包装格式和 crawler 直连格式"""
    # center 代理格式: {"code": 0, "data": {"success": true, "data": {...}}}
    if "code" in body and body.get("code") == 0:
        inner = body.get("data", {})
        if isinstance(inner, dict) and "success" in inner:
            return inner.get("success"), inner.get("data", {}), inner.get("message", "")
        # inner 直接就是数据
        return True, inner, ""
    # crawler 直连格式: {"success": true, "data": {...}}
    if "success" in body:
        return body.get("success"), body.get("data", {}), body.get("message", "")
    # center 代理失败格式: {"code": -1, "message": "..."}
    if body.get("code") == -1:
        return False, {}, body.get("message", "服务异常")
    return False, {}, "未知响应格式"


def subscribe(email):
    """订阅公告监控（每个实例只能绑定一个邮箱，重复设置自动替换）"""
    old_email = get_bound_email()
    if old_email and old_email != email:
        # 先取消旧邮箱订阅
        try:
            unsub_url = API_BASE + "/unsubscribe"
            unsub_data = urlencode({"email": old_email}).encode("utf-8")
            unsub_req = Request(unsub_url, data=unsub_data, method="POST")
            unsub_req.add_header("Content-Type", "application/x-www-form-urlencoded")
            urlopen(unsub_req, timeout=10)
        except Exception:
            pass  # 旧邮箱取消失败不影响新订阅

    url = API_BASE + "/subscribe"
    data = urlencode({"email": email}).encode("utf-8")
    req = Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        resp = urlopen(req, timeout=15)
        body = json.loads(resp.read().decode("utf-8"))
        success, data_obj, err_msg = parse_response(body)
        if success:
            set_bound_email(email)  # 本地绑定新邮箱
            msg = data_obj.get("message", "订阅成功") if isinstance(data_obj, dict) else "订阅成功"
            if old_email and old_email != email:
                msg += "（已自动替换旧邮箱 {}）".format(old_email)
            print("SUBSCRIBE_STATUS: SUCCESS")
            print("MESSAGE: " + msg)
        else:
            print("ERROR: " + (err_msg or "订阅失败"))
            sys.exit(1)
    except (URLError, HTTPError) as e:
        print("ERROR: 服务连接失败 - " + str(e))
        sys.exit(1)


def unsubscribe(email=None):
    """取消订阅（默认使用本地绑定的邮箱）"""
    if not email:
        email = get_bound_email()
    if not email:
        print("ERROR: 当前未绑定邮箱，无需取消")
        sys.exit(1)

    url = API_BASE + "/unsubscribe"
    data = urlencode({"email": email}).encode("utf-8")
    req = Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        resp = urlopen(req, timeout=15)
        body = json.loads(resp.read().decode("utf-8"))
        success, data_obj, err_msg = parse_response(body)
        if success:
            clear_bound_email()  # 清除本地绑定
            msg = data_obj.get("message", "已取消订阅") if isinstance(data_obj, dict) else "已取消订阅"
            print("UNSUBSCRIBE_STATUS: SUCCESS")
            print("MESSAGE: " + msg)
        else:
            print("ERROR: " + (err_msg or "取消失败"))
            sys.exit(1)
    except (URLError, HTTPError) as e:
        print("ERROR: 服务连接失败 - " + str(e))
        sys.exit(1)


def trigger_push(email=None):
    """手动触发推送（默认使用本地绑定的邮箱）"""
    if not email:
        email = get_bound_email()
    if not email:
        print("ERROR: 请先设置邮箱订阅后再触发推送")
        sys.exit(1)

    url = API_BASE + "/trigger-push"
    url += "?" + urlencode({"email": email})
    req = Request(url, data=b"", method="POST")

    try:
        resp = urlopen(req, timeout=60)
        body = json.loads(resp.read().decode("utf-8"))
        success, data_obj, err_msg = parse_response(body)
        if success:
            total = data_obj.get("newCount", 0) if isinstance(data_obj, dict) else 0
            notify = data_obj.get("notifyStatus", "done") if isinstance(data_obj, dict) else "done"
            msg = "推送完成。本轮检测到 {} 条新公告，推送状态: {}".format(total, notify)
            print("TRIGGER_STATUS: SUCCESS")
            print("MESSAGE: " + msg)
        else:
            print("ERROR: " + (err_msg or "推送失败"))
            sys.exit(1)
    except (URLError, HTTPError) as e:
        print("ERROR: 服务连接失败 - " + str(e))
        sys.exit(1)


def show_status():
    """查看当前绑定状态"""
    email = get_bound_email()
    if email:
        print("STATUS: BOUND")
        print("EMAIL: " + email)
        print("MESSAGE: 当前已绑定邮箱 {}\uff0c系统每小时自动推送。".format(email))
    else:
        print("STATUS: UNBOUND")
        print("MESSAGE: 当前未绑定邮箱，请先设置您的接收邮箱。")


def main():
    if len(sys.argv) < 2:
        print("ERROR: 请提供参数（邮箱地址 / trigger / unsubscribe / status）")
        sys.exit(1)

    arg = sys.argv[1].strip()

    if arg.lower() == "trigger":
        trigger_push()
    elif arg.lower().startswith("trigger:"):
        email = arg[len("trigger:"):].strip()
        trigger_push(email if email and "@" in email else None)
    elif arg.lower() == "unsubscribe":
        unsubscribe()
    elif arg.lower().startswith("unsubscribe:"):
        email = arg[len("unsubscribe:"):].strip()
        unsubscribe(email if email and "@" in email else None)
    elif arg.lower() == "status":
        show_status()
    else:
        email = arg
        if "@" not in email:
            print("ERROR: 请提供有效的邮箱地址（需包含@）")
            sys.exit(1)
        subscribe(email)


if __name__ == "__main__":
    main()
