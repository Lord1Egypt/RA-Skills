#!/usr/bin/env python3
"""
cancel-alert.py — 取消/查看价格警报

用法:
  python3 cancel-alert.py --agent laok --list           # 列出所有活跃警报
  python3 cancel-alert.py --agent laok --id eth-1741234 # 按 ID 取消
  python3 cancel-alert.py --agent laok --asset ETH       # 取消所有 ETH 警报
  python3 cancel-alert.py --agent laok --type price      # 取消所有价格类警报
  python3 cancel-alert.py --agent laok --type news       # 取消所有新闻类警报
  python3 cancel-alert.py --agent laok --all             # 取消所有活跃警报
"""

import argparse
import json
from pathlib import Path
from datetime import datetime


def fmt_alert(a: dict) -> str:
    alert_type = a.get("type", "price")
    asset = a.get("asset", "?")
    market = a.get("market", "crypto")
    created = a.get("created_at", "?")[:16]
    summary = a.get("context_summary", "")[:50]

    if alert_type == "price":
        cond = a.get("condition", "?")
        target = a.get("target_price", "?")
        return f"[{a['id']}] {asset} {cond} {target} ({market}) | {created} | {summary}"
    elif alert_type == "news":
        keywords = ", ".join(a.get("keywords", []))[:40]
        return f"[{a['id']}] NEWS: {keywords} | {created} | {summary}"
    else:
        return f"[{a['id']}] {alert_type} | {created}"


def main():
    parser = argparse.ArgumentParser(description="Cancel or list alerts")
    parser.add_argument("--agent",       default="laok")
    parser.add_argument("--id",          default="",  help="Alert ID to cancel")
    parser.add_argument("--asset",       default="",  help="Cancel all alerts for this asset")
    parser.add_argument("--type",        default="",  help="Filter by type: price / news")
    parser.add_argument("--all",         action="store_true", help="Cancel all active alerts")
    parser.add_argument("--list",        action="store_true", help="List active alerts")
    parser.add_argument("--alerts-file", default="")
    args = parser.parse_args()

    alerts_path = Path(args.alerts_file) if args.alerts_file else \
        Path.home() / f".openclaw/agents/{args.agent}/private/market-alerts.json"

    if not alerts_path.exists():
        print("（无警报文件）")
        return

    with open(alerts_path) as f:
        data = json.load(f)

    alerts = data.get("alerts", [])
    active = [a for a in alerts if a.get("status") == "active"]

    # ── List mode ──────────────────────────────────────────────────────────
    if args.list:
        if not active:
            print("（无活跃警报）")
            return

        # Group by type
        price_alerts = [a for a in active if a.get("type", "price") == "price"]
        news_alerts  = [a for a in active if a.get("type") == "news"]

        if price_alerts:
            print(f"\n📊 价格警报 ({len(price_alerts)}):")
            for a in price_alerts:
                print(f"  {fmt_alert(a)}")

        if news_alerts:
            print(f"\n📰 新闻警报 ({len(news_alerts)}):")
            for a in news_alerts:
                print(f"  {fmt_alert(a)}")

        print(f"\n合计: {len(active)} 个活跃警报")
        return

    # ── Cancel mode ────────────────────────────────────────────────────────
    cancelled = 0
    for a in alerts:
        if a.get("status") != "active":
            continue

        match = False
        if args.all:
            match = True
        elif args.id and a["id"] == args.id:
            match = True
        elif args.asset and a.get("asset", "").upper() == args.asset.upper():
            match = True
        elif args.type and a.get("type", "price") == args.type:
            match = True

        if match:
            a["status"] = "cancelled"
            a["cancelled_at"] = datetime.now().isoformat()
            cancelled += 1
            print(f"  取消: {fmt_alert(a)}")

    if cancelled == 0:
        print("（未找到匹配的警报）")
        return

    data["alerts"] = alerts
    with open(alerts_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    remaining = sum(1 for a in data["alerts"] if a.get("status") == "active")
    print(f"\n✅ 已取消 {cancelled} 个警报，剩余活跃: {remaining} 个")


if __name__ == "__main__":
    main()
