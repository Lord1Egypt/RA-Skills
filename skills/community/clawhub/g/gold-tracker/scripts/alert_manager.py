#!/usr/bin/env python3
"""提醒引擎：多基准检测、动态阈值、状态机、冷却、每日上限、自动解决。

核心修复（对照 P0-2 / P0-6 / P0-7 / P0-8）：
  - 多基准：昨日收盘（prev_close）、单次抓取（last_fetch）、可选 EMA、连续 N 次同向趋势
  - 动态阈值：基于近 lookback 天日收益率波动率（stddev）× 乘数，夹在 [min,max]
  - 趋势行情可触发；每日每方向限一次防刷屏
  - 状态机：pending → sent → acknowledged → resolved/dismissed
  - 通知发送由 notify.py 负责；失败保留 pending 待下周期重试

用法:
    python3 scripts/alert_manager.py detect
    python3 scripts/alert_manager.py list
    python3 scripts/alert_manager.py pending
    python3 scripts/alert_manager.py status <id> <status> [resolved_price]
    python3 scripts/alert_manager.py auto_resolve
    python3 scripts/alert_manager.py cleanup
    python3 scripts/alert_manager.py threshold
"""

import hashlib
import json
import statistics
import sys

from common import paths, config, atomic, history, heartbeat, timeutil

VALID_STATUSES = ("pending", "sent", "acknowledged", "resolved", "dismissed")


def alerts_dir():
    d = paths.resolve("alerts")
    d.mkdir(parents=True, exist_ok=True)
    return d


def today_file(tz):
    return alerts_dir() / (timeutil.today_str(tz) + ".json")


def read_file(f):
    if not f.exists():
        return []
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def write_file(f, alerts):
    atomic.atomic_write_json(f, alerts)


def iter_alerts():
    """遍历所有提醒文件，返回 [(file, alert_dict)]。"""
    out = []
    for f in sorted(alerts_dir().iterdir()):
        if f.suffix != ".json":
            continue
        for a in read_file(f):
            if isinstance(a, dict):
                out.append((f, a))
    return out


def _update_alert(alert_id, mutator):
    for f, a in iter_alerts():
        if a.get("alert_id") != alert_id:
            continue
        data = read_file(f)
        for item in data:
            if item.get("alert_id") == alert_id:
                mutator(item)
                item["updated_at"] = timeutil.now_iso()
                write_file(f, data)
                return True
    return False


def mark_sent(alert_id, sent_via):
    return _update_alert(alert_id, lambda a: a.update(
        status="sent", sent_via=list(sent_via), sent_at=timeutil.now_iso()))


def mark_failed(alert_id, error):
    return _update_alert(alert_id, lambda a: a.update(
        last_error=error))  # 状态保持 pending，待下周期重试


def set_status(alert_id, status, resolved_price=None):
    def _apply(a):
        a["status"] = status
        if status == "resolved":
            a["resolved_at"] = timeutil.now_iso()
            if resolved_price is not None:
                a["resolved_price"] = resolved_price
    return _update_alert(alert_id, _apply)


def list_pending():
    return [a for _, a in iter_alerts() if a.get("status") == "pending"]


def get_active_alerts():
    return [a for _, a in iter_alerts() if a.get("status") in ("pending", "sent")]


def compute_threshold(cfg, closes):
    b = cfg["alerts"]
    lo = float(b.get("min_threshold_pct", 0.5))
    hi = float(b.get("max_threshold_pct", 3.0))
    base = float(b.get("threshold_pct", 1.0))
    mult = float(b.get("volatility_multiplier", 1.5))
    lookback = int(b.get("lookback_days", 7))

    window = closes[-lookback:]
    rets = []
    for i in range(1, len(window)):
        prev = window[i - 1]["price"]
        cur = window[i]["price"]
        if prev:
            rets.append((cur - prev) / prev * 100)
    if len(rets) >= 2:
        vol = statistics.stdev(rets)
        thr = mult * vol
        return round(max(lo, min(hi, thr)), 2)
    return round(max(lo, min(hi, base)), 2)


def _ema(values, window):
    if not values:
        return None
    k = 2.0 / (window + 1)
    ema = values[0]
    for v in values[1:]:
        ema = v * k + ema * (1 - k)
    return ema


def build_benchmarks(cfg, state, closes, current, tz):
    bm = cfg["alerts"]["benchmarks"]
    out = []
    today = timeutil.today_str(tz)

    if bm.get("prev_close", True):
        prev_close = state.get("prev_close")
        if prev_close is None:
            prior = [c for c in closes if c["date"] < today]
            if prior:
                prev_close = prior[-1]["price"]
        if prev_close:
            out.append(("prev_close", prev_close, (current - prev_close) / prev_close * 100))

    if bm.get("last_fetch", True):
        last = state.get("last_price")
        if last:
            out.append(("last_fetch", last, (current - last) / last * 100))

    if bm.get("ema"):
        win = int(bm.get("ema_window", 20))
        ema = _ema([c["price"] for c in closes], win)
        if ema:
            out.append(("ema", ema, (current - ema) / ema * 100))
    return out


def detect_trend(cfg, closes):
    bm = cfg["alerts"]["benchmarks"]
    if not bm.get("trend", True):
        return None
    n = int(bm.get("trend_consecutive_n", 3))
    prices = [c["price"] for c in closes]
    if len(prices) < n + 1:
        return None
    diffs = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    tail = diffs[-n:]
    if all(d > 0 for d in tail):
        base = prices[-(n + 1)]
        change = (prices[-1] - base) / base * 100 if base else 0.0
        return ("trend_up", round(change, 2), n)
    if all(d < 0 for d in tail):
        base = prices[-(n + 1)]
        change = (prices[-1] - base) / base * 100 if base else 0.0
        return ("trend_down", round(change, 2), n)
    return None


def _on_cooldown(today_alerts, alert_type, benchmark, cooldown_minutes, now):
    for a in today_alerts:
        if a.get("type") != alert_type or a.get("benchmark") != benchmark:
            continue
        try:
            from datetime import datetime
            created = datetime.fromisoformat(a.get("created_at", ""))
            if (now - created).total_seconds() < cooldown_minutes * 60:
                return True
        except Exception:
            pass
    return False


def detect(current_price, state, cfg, tz):
    from datetime import datetime

    closes = history.daily_closes(history.load_series())
    threshold = compute_threshold(cfg, closes)

    today_alerts = read_file(today_file(tz))
    now = datetime.now(timeutil.get_tz(tz))
    cooldown_min = int(cfg["alerts"].get("cooldown_minutes", 30))
    max_day = int(cfg["alerts"].get("max_alerts_per_day", 10))
    max_dir = int(cfg["alerts"].get("max_alerts_per_direction_per_day", 1))

    # 每日上限（不计 resolved/dismissed）
    active_today = [a for a in today_alerts
                    if a.get("status") not in ("resolved", "dismissed")]
    if len(active_today) >= max_day:
        return [], threshold

    candidates = []

    # 趋势（每日每方向限一次）
    trend = detect_trend(cfg, closes)
    if trend:
        ttype, change, n = trend
        existing_dir = [a for a in today_alerts
                        if a.get("type") == ttype]
        if len(existing_dir) < max_dir:
            direction = "连续上涨" if ttype == "trend_up" else "连续下跌"
            candidates.append({
                "type": ttype,
                "benchmark": "trend",
                "change_pct": change,
                "price": current_price,
                "direction": direction,
                "note": "连续 {} 次同向".format(n),
            })

    # 基准检测
    for name, base_price, change in build_benchmarks(cfg, state, closes, current_price, tz):
        abs_change = abs(change)
        if abs_change < threshold * 0.5:
            continue
        if change >= threshold:
            atype, direction = "price_breakout_high", "上涨"
        elif change <= -threshold:
            atype, direction = "price_breakout_low", "下跌"
        elif abs_change >= threshold * 0.7:
            atype = "price_reversal_up" if change > 0 else "price_reversal_down"
            direction = "反转上涨" if change > 0 else "反转下跌"
        else:
            continue
        candidates.append({
            "type": atype,
            "benchmark": name,
            "change_pct": round(change, 2),
            "price": current_price,
            "direction": direction,
            "base_price": base_price,
            "note": "",
        })

    alerts = []
    for c in candidates:
        if _on_cooldown(today_alerts, c["type"], c["benchmark"], cooldown_min, now):
            continue
        if len(active_today) + len(alerts) >= max_day:
            break
        if c["type"] in ("trend_up", "trend_down"):
            if len([a for a in today_alerts if a.get("type") == c["type"]]) + \
               len([a for a in alerts if a["type"] == c["type"]]) >= max_dir:
                continue

        msg = build_message(c, threshold)
        alert_id = "{}-{}".format(
            datetime.now(timeutil.get_tz(tz)).strftime("%Y%m%d-%H%M%S"),
            c["benchmark"])
        alerts.append({
            "alert_id": alert_id,
            "type": c["type"],
            "price": c["price"],
            "change_pct": c["change_pct"],
            "threshold_pct": threshold,
            "benchmark": c["benchmark"],
            "message": msg,
            "details": {k: v for k, v in c.items() if k not in ("type", "benchmark", "price", "change_pct")},
            "status": "pending",
            "created_at": datetime.now(timeutil.get_tz(tz)).isoformat(),
            "updated_at": datetime.now(timeutil.get_tz(tz)).isoformat(),
            "resolved_at": None,
            "resolved_price": None,
        })

    return alerts, threshold


_BENCHMARK_LABELS = {
    "prev_close": "昨日收盘",
    "last_fetch": "上次抓取",
    "ema": "EMA 均线",
    "trend": "趋势",
}


def benchmark_label(name):
    """把检测基准的技术名映射为面向客户的中文标签。"""
    return _BENCHMARK_LABELS.get(name, name) or "未知基准"


_TYPE_LABELS = {
    "price_breakout_high": "上涨突破",
    "price_breakout_low": "下跌突破",
    "price_reversal_up": "反转上涨",
    "price_reversal_down": "反转下跌",
    "trend_up": "连续上涨",
    "trend_down": "连续下跌",
}


def type_label(t):
    return _TYPE_LABELS.get(t, t) or "未知类型"


_STATUS_LABELS = {
    "pending": "待发送",
    "sent": "已发送",
    "acknowledged": "已确认",
    "resolved": "已解决",
    "dismissed": "已忽略",
}


def status_label(s):
    return _STATUS_LABELS.get(s, s) or "未知状态"


def build_message(c, threshold):
    emoji = {"上涨": "📈", "下跌": "📉", "反转上涨": "↗️", "反转下跌": "↘️",
             "连续上涨": "📈", "连续下跌": "📉"}.get(c["direction"], "📊")
    note = "（{}）".format(c.get("note")) if c.get("note") else ""
    return "{emoji} 金价{direction}提醒{note}：当前 ${price:.2f}，较{benchmark}变动 {chg:+.2f}%（正常波动 ±{thr}%）".format(
        emoji=emoji, direction=c["direction"], note=note,
        price=c["price"], benchmark=benchmark_label(c["benchmark"]),
        chg=c["change_pct"], thr=threshold)


def create_alerts(current_price):
    cfg = config.load()
    tz = config.dig(cfg, "general.timezone", "Asia/Shanghai")
    state = _load_state()
    alerts, threshold = detect(current_price, state, cfg, tz)
    if alerts:
        tf = today_file(tz)
        existing = read_file(tf)
        existing.extend(alerts)
        write_file(tf, existing)
    heartbeat.record("alert_detect")
    return alerts, threshold


def _load_state():
    f = paths.resolve("state.json")
    if f.exists():
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception:
            pass
    return {}


def auto_resolve(minutes):
    now = timeutil.now()
    changed = False
    for f, _ in iter_alerts():
        data = read_file(f)
        modified = False
        for a in data:
            if a.get("status") in ("pending", "sent"):
                try:
                    from datetime import datetime
                    created = datetime.fromisoformat(a.get("created_at", ""))
                    if (now - created).total_seconds() > minutes * 60:
                        a["status"] = "resolved"
                        a["updated_at"] = now.isoformat()
                        a["resolved_at"] = now.isoformat()
                        modified = True
                except Exception:
                    pass
        if modified:
            write_file(f, data)
            changed = True
    return changed


def cleanup(retention_days):
    import datetime as _dt
    now = timeutil.now()
    removed = 0
    for f in sorted(alerts_dir().iterdir()):
        if f.suffix != ".json":
            continue
        try:
            file_date = _dt.datetime.strptime(f.stem, "%Y-%m-%d").replace(tzinfo=now.tzinfo)
            if (now - file_date).days > retention_days:
                f.unlink()
                removed += 1
        except Exception:
            pass
    return removed


def format_alerts(alerts):
    if not alerts:
        return "暂无活跃提醒"
    lines = ["## 活跃提醒"]
    icon = {"pending": "⏳", "sent": "📤", "acknowledged": "✅",
            "resolved": "🔒", "dismissed": "❌"}
    for a in alerts:
        lines.append("")
        lines.append("### {} {}".format(icon.get(a.get("status"), "⚪"), a.get("message", "")))
        lines.append("- ID: {}".format(a.get("alert_id")))
        lines.append("- 类型: {} / 基准: {} (正常波动 ±{}%)".format(
            type_label(a.get("type")), benchmark_label(a.get("benchmark")), a.get("threshold_pct")))
        lines.append("- 状态: {} / 创建: {}".format(status_label(a.get("status")), a.get("created_at")))
        if a.get("sent_via"):
            lines.append("- 已送达: {}".format(", ".join(a["sent_via"])))
        if a.get("resolved_at"):
            lines.append("- 已解决: {} (价格 ${})".format(a.get("resolved_at"), a.get("resolved_price")))
    return "\n".join(lines)


def main():
    paths.ensure_env()
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    action = sys.argv[1]
    cfg = config.load()
    tz = config.dig(cfg, "general.timezone", "Asia/Shanghai")

    if action == "detect":
        state = _load_state()
        current = state.get("current_price")
        if not current:
            print("[错误] state.json 中无 current_price，请先运行 fetch.py")
            sys.exit(1)
        alerts, threshold = create_alerts(current)
        print("[信息] 本次正常波动范围: ±{}%".format(threshold))
        if alerts:
            print("[成功] 创建 {} 条提醒:".format(len(alerts)))
            for a in alerts:
                print("  - {}".format(a["message"]))
        else:
            print("[信息] 无新提醒触发")

    elif action == "list":
        print(format_alerts(get_active_alerts()))

    elif action == "pending":
        p = list_pending()
        print(format_alerts(p) if p else "暂无待发送提醒")

    elif action == "status":
        if len(sys.argv) < 4:
            print("用法: alert_manager.py status <alert_id> <pending|sent|acknowledged|resolved|dismissed> [resolved_price]")
            sys.exit(1)
        alert_id, status = sys.argv[2], sys.argv[3]
        if status not in VALID_STATUSES:
            print("无效状态: {}".format(status))
            sys.exit(1)
        resolved_price = float(sys.argv[4]) if len(sys.argv) > 4 else None
        if set_status(alert_id, status, resolved_price):
            print("[成功] 提醒 {} 状态更新为 {}".format(alert_id, status))
        else:
            print("[错误] 未找到提醒 {}".format(alert_id))
            sys.exit(1)

    elif action == "auto_resolve":
        minutes = int(cfg["alerts"].get("auto_resolve_minutes", 1440))
        print("[成功] 已自动解决" if auto_resolve(minutes) else "[信息] 无超时提醒")
        heartbeat.record("alert_auto_resolve")

    elif action == "cleanup":
        removed = cleanup(int(cfg["alerts"].get("retention_days", 30)))
        print("[完成] 清理 {} 个过期提醒文件".format(removed))
        heartbeat.record("alert_cleanup")

    elif action == "threshold":
        closes = history.daily_closes(history.load_series())
        print("当前正常波动范围: ±{}%".format(compute_threshold(cfg, closes)))

    else:
        print("未知操作: {}".format(action))
        sys.exit(1)


if __name__ == "__main__":
    main()
