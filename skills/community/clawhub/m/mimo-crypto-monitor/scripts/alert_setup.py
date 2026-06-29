#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加密货币告警设置脚本
支持价格突破/跌破/涨跌幅告警
"""

import json
import os
import sys
import time
from datetime import datetime

ALERTS_FILE = os.path.expanduser("~/.openclaw/workspace/crypto-alerts.json")

def load_alerts():
    if os.path.exists(ALERTS_FILE):
        with open(ALERTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_alerts(alerts):
    os.makedirs(os.path.dirname(ALERTS_FILE), exist_ok=True)
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=2, ensure_ascii=False)

def add_alert(coin, condition, target, interval=300):
    alerts = load_alerts()
    alert = {
        "id": int(time.time() * 1000),
        "coin": coin.upper(),
        "condition": condition,
        "target": target,
        "interval": interval,
        "created_at": datetime.now().isoformat(),
        "triggered": False
    }
    alerts.append(alert)
    save_alerts(alerts)
    cond_text = {"above": f"突破 {target}", "below": f"跌破 {target}", "change": f"涨跌幅超过 {target}"}
    print(f"✅ 告警已设置")
    print(f"🪙 币种：{coin.upper()}")
    print(f"📏 条件：{cond_text.get(condition, condition)}")
    print(f"⏰ 检查频率：每{interval//60}分钟")

def list_alerts():
    alerts = load_alerts()
    if not alerts:
        print("📭 暂无告警")
        return
    for a in alerts:
        status = "🔴 已触发" if a["triggered"] else "🟢 监控中"
        print(f"  {status} | {a['coin']} | {a['condition']} {a['target']} | 频率{a['interval']//60}min")

def remove_alert(alert_id):
    alerts = load_alerts()
    alerts = [a for a in alerts if a["id"] != alert_id]
    save_alerts(alerts)
    print(f"🗑 告警 {alert_id} 已删除")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--coin", required=True)
    parser.add_argument("--condition", required=True, choices=["above", "below", "change"])
    parser.add_argument("--target", required=True)
    parser.add_argument("--interval", type=int, default=300)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--remove", type=int)
    args = parser.parse_args()

    if args.list:
        list_alerts()
    elif args.remove:
        remove_alert(args.remove)
    else:
        add_alert(args.coin, args.condition, args.target, args.interval)
