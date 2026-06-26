#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alert Webhook Receiver
Receives alerts from Alertmanager and forwards to Feishu/Lark.
Configure via environment variables (see below).
"""

import os
import re
import sys
from flask import Flask, request
import requests

app = Flask(__name__)

# ==============   Env Config   =================
# FEISHU_WEBHOOK_URL  # Feishu bot webhook URL
# WEBHOOK_PORT        # Listen port (default: 5000)
# PUSH_INTERVAL       # Agent push interval (for value formatting, default: 60)

FEISHU_WEBHOOK_URL = os.environ.get("FEISHU_WEBHOOK_URL", "")
WEBHOOK_PORT = int(os.environ.get("WEBHOOK_PORT", "5000"))
PUSH_INTERVAL = int(os.environ.get("PUSH_INTERVAL", "60"))


# ==============   Helpers   =================
def extract_ip(hostname):
    """Extract IP address from hostname string."""
    try:
        m = re.search(r'(\d+\.\d+\.\d+\.\d+)', hostname)
        return m.group(1) if m else "unknown"
    except Exception:
        return "unknown"


def format_value(alertname, value):
    """Format alert value for display."""
    try:
        if alertname in ["JVMProcessDown", "MySQLDown"]:
            return str(value)

        v = float(value)

        # Percentage alerts
        if alertname in ["JVMHeapUsageHigh", "JVMOldGenHigh",
                          "JVMHeapUsageHighWarmup", "MySQLBufferPoolHigh"]:
            return f"{v * 100:.2f}%"

        # GC time alerts
        if "Gc" in alertname:
            percent = v / PUSH_INTERVAL * 100
            return f"{v:.2f}s ({percent:.1f}% of cycle)"

        # MySQL memory
        if alertname == "MySQLMemoryHigh":
            return f"{v / 1024**3:.2f} GB"

        return str(v)
    except Exception:
        return str(value)


# ================= Webhook Handler   =================
@app.route('/webhook', methods=['POST'])
def webhook():
    if not FEISHU_WEBHOOK_URL:
        return "FEISHU_WEBHOOK_URL not configured", 500

    data = request.json or {}
    level = request.args.get("level", "info")

    title = "告警通知"
    if level == "critical":
        title = "严重告警"
    elif level == "warning":
        title = "警告告警"

    text = ""
    for a in data.get("alerts", []):
        labels = a.get("labels", {})
        annotations = a.get("annotations", {})

        alertname = labels.get("alertname", "unknown")
        hostname = labels.get("hostname", "unknown")
        game_dir = labels.get("game_dir", "")
        value = annotations.get("value", "0")
        value_fmt = format_value(alertname, value)
        summary = annotations.get("summary", "")
        desc = annotations.get("description", "")
        ip = extract_ip(hostname)

        text += f"""### {summary}
- 主机: {hostname}
- IP: {ip}
{"- 服务: " + game_dir if game_dir else ""}
- 当前值: {value_fmt}
- 描述: {desc}

"""

    msg = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"tag": "plain_text", "content": title}},
            "elements": [{"tag": "div", "text": {"tag": "lark_md", "content": text}}]
        }
    }

    requests.post(FEISHU_WEBHOOK_URL, json=msg)
    return "ok"


if __name__ == "__main__":
    if not FEISHU_WEBHOOK_URL:
        print("ERROR: FEISHU_WEBHOOK_URL environment variable is not set", file=sys.stderr)
        sys.exit(1)
    # Bind to 127.0.0.1 — Alertmanager calls via localhost only
    app.run(host="127.0.0.1", port=WEBHOOK_PORT)
