#!/usr/bin/env python3
"""
outer_ratio_monitor.py — A股外内比实时监控脚本
用法：
  python3 outer_ratio_monitor.py              # 全量扫描
  python3 outer_ratio_monitor.py --status     # 仅状态（无告警）
  python3 outer_ratio_monitor.py --stock 600036  # 单只
  python3 outer_ratio_monitor.py --alert-only # 仅告警
  python3 outer_ratio_monitor.py --history    # 历史趋势
"""

import urllib.request
import json
import os
import sys
import argparse
from datetime import date, datetime
from pathlib import Path

# ========== 配置（修改这里） ==========
WATCHED_STOCKS = [
    ("600036", "招商银行"),
    ("601318", "中国平安"),
    ("002891", "中宠股份"),
    ("000625", "长安汽车"),
    ("600780", "通宝能源"),
    ("000426", "兴业银锡"),
]

ALERT_THRESHOLDS = {
    "outer_ratio_strong": 1.25,   # 主力建仓信号
    "outer_ratio_danger": 0.50,   # 主力出逃信号
    "surge_up_pct": 9.0,          # 大涨异动
    "surge_down_pct": -5.0,       # 大跌异动
    "volume_surge_ratio": 2.0,    # 量能异常倍数
}

FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "")
SNAPSHOT_FILE = os.path.expanduser("~/.openclaw/memory/stocks/intraday_snapshots.json")
HISTORY_FILE = os.path.expanduser("~/.openclaw/memory/stocks/outer_ratio_history.json")

C_GREEN = "\033[92m"
C_RED   = "\033[91m"
C_YELLOW = "\033[93m"
C_RESET  = "\033[0m"


def get_realtime_data(code: str) -> dict:
    """获取单只股票实时行情"""
    market = "sh" if code.startswith(("6", "9")) else "sz"
    url = f"https://qt.gtimg.cn/q={market}{code}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            raw = resp.read().decode("gbk")
        parts = raw.split('"')
        if len(parts) < 2:
            return None
        data = parts[1].split("~")
        price = float(data[3]) if data[3] else 0
        prev_close = float(data[4]) if data[4] else price
        change_pct = ((price - prev_close) / prev_close * 100) if prev_close else 0
        outer = int(data[7]) if data[7] else 0
        inner = int(data[8]) if data[8] else 0
        volume = int(data[6]) if data[6] else 0
        outer_ratio = round(outer / (outer + inner), 4) if (outer + inner) > 0 else 0

        return {
            "code": code,
            "name": data[1] if len(data) > 1 else code,
            "price": price,
            "prev_close": prev_close,
            "change_pct": round(change_pct, 2),
            "outer": outer,
            "inner": inner,
            "outer_ratio": outer_ratio,
            "volume": volume,
            "time": datetime.now().strftime("%H:%M"),
        }
    except Exception as e:
        print(f"  [错误] {code}: {e}")
        return None


def detect_alerts(data: dict, prev_snap: dict = None) -> list:
    """检测异动信号"""
    alerts = []
    if data["change_pct"] >= ALERT_THRESHOLDS["surge_up_pct"]:
        alerts.append(f"🚀 {'涨停' if data['change_pct'] >= 9.9 else '大涨'}+{data['change_pct']}%")
    elif data["change_pct"] <= ALERT_THRESHOLDS["surge_down_pct"]:
        alerts.append(f"🔴 大跌 {data['change_pct']}%")
    if data["outer_ratio"] >= ALERT_THRESHOLDS["outer_ratio_strong"]:
        alerts.append(f"🟢 主力建仓 外内比{data['outer_ratio']:.2f}")
    elif data["outer_ratio"] <= ALERT_THRESHOLDS["outer_ratio_danger"]:
        alerts.append(f"🔴 主力出逃 外内比{data['outer_ratio']:.2f}")
    if prev_snap:
        prev_vol = prev_snap.get("volume", 0)
        if prev_vol > 0:
            vol_ratio = data["volume"] / prev_vol
            if vol_ratio >= ALERT_THRESHOLDS["volume_surge_ratio"]:
                alerts.append(f"📈 量能放大 {vol_ratio:.1f}x")
    return alerts


def load_snapshots() -> dict:
    if os.path.exists(SNAPSHOT_FILE):
        with open(SNAPSHOT_FILE) as f:
            return json.load(f)
    return {}


def save_snapshots(snapshots: dict):
    os.makedirs(os.path.dirname(SNAPSHOT_FILE), exist_ok=True)
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(snapshots, f, ensure_ascii=False, indent=2)


def load_history() -> dict:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return {}


def save_history(history: dict):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def record_to_history(data: dict):
    """将当前外内比记录到历史数据库"""
    today = date.today().strftime("%Y-%m-%d")
    history = load_history()
    code = data["code"]
    if code not in history:
        history[code] = {"name": data["name"], "dates": {}}
    history[code]["dates"][today] = data["outer_ratio"]
    save_history(history)


def scan_all(status_only: bool = False, alert_only: bool = False):
    """扫描所有自选股"""
    today = date.today().strftime("%Y-%m-%d")
    snapshots = load_snapshots()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    time_key = datetime.now().strftime("%H:%M")

    print(f"\n{'='*60}")
    print(f"📊 盘中实时监控  {now_str}")
    print(f"{'='*60}")

    alert_count = 0
    all_data = []

    for code, name in WATCHED_STOCKS:
        d = get_realtime_data(code)
        if not d:
            continue
        all_data.append(d)
        prev_snap = snapshots.get(code)
        alerts = detect_alerts(d, prev_snap)

        if status_only:
            ratio_color = (C_GREEN if d["outer_ratio"] >= 1.25 else
                           C_RED if d["outer_ratio"] <= 0.50 else C_YELLOW)
            print(f"  {d['name']}({code}): {d['price']}  {d['change_pct']:+.2f}%  "
                  f"外内比 {ratio_color}{d['outer_ratio']:.4f}{C_RESET}")
            print(f"    外盘{d['outer']:,}手 / 内盘{d['inner']:,}手")
        else:
            print(f"\n{d['name']}({code}) {d['time']}")
            print(f"  价格: {d['price']}  {d['change_pct']:+.2f}%")
            print(f"  外内比: {d['outer_ratio']:.4f} (外{d['outer']:,}手 / 内{d['inner']:,}手)")
            for alert in alerts:
                print(f"  {alert}")
                alert_count += 1

        record_to_history(d)

        # 更新快照
        snapshots[code] = {"volume": d["volume"], "outer_ratio": d["outer_ratio"]}

    save_snapshots(snapshots)

    if not status_only:
        print(f"\n{'='*60}")
        print(f"✅ 扫描完成：{len(all_data)}只 | 异动{alert_count}只 | {now_str}")

    return all_data


def scan_single(code: str):
    """扫描单只股票"""
    d = get_realtime_data(code)
    if not d:
        print(f"获取失败: {code}")
        return
    alerts = detect_alerts(d)
    print(f"\n{d['name']}({code}) {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  价格: {d['price']}  {d['change_pct']:+.2f}%")
    print(f"  外内比: {d['outer_ratio']:.4f} (外{d['outer']:,}手 / 内{d['inner']:,}手)")
    for alert in alerts:
        print(f"  {alert}")


def show_history():
    """显示外内比历史趋势"""
    history = load_history()
    today = date.today().strftime("%Y-%m-%d")
    print(f"\n📈 外内比历史趋势（截至 {today}）")
    print("="*60)
    for code, info in history.items():
        name = info["name"]
        dates = info["dates"]
        if not dates:
            continue
        sorted_dates = sorted(dates.items(), reverse=True)[:7]
        trend = " ".join([f"{dt[:5]}:{r:.2f}" for dt, r in sorted_dates])
        print(f"  {name}({code}): {trend}")


def main():
    parser = argparse.ArgumentParser(description="A股外内比实时监控")
    parser.add_argument("--status", action="store_true", help="仅状态输出（无告警）")
    parser.add_argument("--alert-only", action="store_true", help="仅输出告警")
    parser.add_argument("--stock", type=str, help="单只股票代码")
    parser.add_argument("--history", action="store_true", help="显示历史趋势")
    args = parser.parse_args()

    if args.history:
        show_history()
    elif args.stock:
        scan_single(args.stock)
    else:
        scan_all(status_only=args.status, alert_only=args.alert_only)


if __name__ == "__main__":
    main()
