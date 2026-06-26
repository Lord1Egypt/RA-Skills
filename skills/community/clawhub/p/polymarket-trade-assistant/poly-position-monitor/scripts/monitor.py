#!/usr/bin/env python3
"""
Main monitoring loop for Polymarket position tracking.

Orchestrates position fetching, price analysis, volume tracking, whale
detection, and order monitoring. Compares states across cycles and dispatches
alerts through configured handlers.

Usage:
    python monitor.py --config config.json
    python monitor.py --config config.json --once
    python monitor.py --config config.json --interval 30
"""

import argparse
import json
import os
import signal
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Import sibling modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alerters import build_handlers, emit, Colors
from fetch_positions import fetch_all_positions, get_monitored_markets
from fetch_price_history import fetch_price_history, compute_price_changes, check_thresholds
from fetch_market_activity import (
    fetch_market_trades, compute_volume_metrics,
    check_volume_anomaly, check_whale_activity,
)

try:
    from fetch_orders import fetch_all_open_orders, HAS_CLOB_CLIENT
except ImportError:
    HAS_CLOB_CLIENT = False
    fetch_all_open_orders = None


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def load_state(state_dir: str) -> dict | None:
    state_file = os.path.join(state_dir, "monitor-state.json")
    if os.path.exists(state_file):
        with open(state_file) as f:
            return json.load(f)
    return None


def save_state(state_dir: str, state: dict) -> None:
    os.makedirs(state_dir, exist_ok=True)
    state_file = os.path.join(state_dir, "monitor-state.json")
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    snapshot = os.path.join(state_dir, f"snapshot-{ts}.json")
    with open(snapshot, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def load_config(config_path: str) -> dict:
    path = os.path.expanduser(config_path)
    with open(path) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Core monitoring cycle
# ---------------------------------------------------------------------------

def run_cycle(config: dict, handlers: list, prev_state: dict | None) -> dict:
    """Execute one full monitoring cycle. Returns new state."""
    now = datetime.now(timezone.utc)
    now_str = now.isoformat()
    now_ts = int(now.timestamp())

    thresholds = config.get("thresholds", {})
    price_thresholds = thresholds.get("price_change", {})
    volume_spike = thresholds.get("volume_spike_ratio", 2.0)
    volume_drop = thresholds.get("volume_drop_ratio", 0.3)
    position_change_pct = thresholds.get("position_change_pct", 0.20)
    min_inflow_usd = thresholds.get("min_inflow_usd", 1000)

    user_addresses = config.get("user_addresses", [])
    watched_addresses = config.get("watched_addresses", [])
    clob_auth = config.get("clob_auth", {})

    prev_ts = None
    if prev_state:
        prev_ts = prev_state.get("timestamp_unix")

    # -----------------------------------------------------------------------
    # 1. Fetch positions
    # -----------------------------------------------------------------------
    emit(handlers, "INFO", "system", "", "获取持仓数据...")
    try:
        positions_by_addr = fetch_all_positions(user_addresses)
    except Exception as e:
        emit(handlers, "WARNING", "system", "", f"获取持仓失败: {e}")
        positions_by_addr = {}

    markets = get_monitored_markets(positions_by_addr)
    condition_ids = list(markets.keys())

    if not condition_ids:
        emit(handlers, "INFO", "system", "", "无活跃持仓，跳过本轮监控")
        return _build_state(now_str, now_ts, positions_by_addr, {}, {}, {}, {})

    emit(handlers, "INFO", "system", "",
         f"监控 {len(condition_ids)} 个市场, "
         f"{sum(len(ps) for ps in positions_by_addr.values())} 个仓位")

    # -----------------------------------------------------------------------
    # 2. Fetch open orders (if auth available)
    # -----------------------------------------------------------------------
    orders = []
    if (HAS_CLOB_CLIENT and fetch_all_open_orders and
            clob_auth.get("api_key") and clob_auth.get("secret")):
        try:
            orders = fetch_all_open_orders(
                api_key=clob_auth["api_key"],
                secret=clob_auth["secret"],
                passphrase=clob_auth.get("passphrase", ""),
                markets=condition_ids,
            )
            emit(handlers, "INFO", "system", "", f"获取到 {len(orders)} 个挂单")
        except Exception as e:
            emit(handlers, "WARNING", "system", "", f"获取挂单失败: {e}")

    # -----------------------------------------------------------------------
    # 3. Price analysis per market
    # -----------------------------------------------------------------------
    price_data_map = {}
    for cid, minfo in markets.items():
        asset_id = minfo.get("asset_id", "")
        if not asset_id:
            continue
        title = minfo.get("title", cid[:12])
        try:
            history = fetch_price_history(asset_id)
            pdata = compute_price_changes(history)
            price_data_map[cid] = pdata

            if price_thresholds:
                breaches = check_thresholds(pdata, price_thresholds)
                for b in breaches:
                    window = b["window"]
                    change = b["change_pct"]
                    thresh = b["threshold"]
                    alert_level = _price_alert_level(window)
                    emit(handlers, alert_level, "price", title,
                         f"{window} 价格变化 {change:+.2%} (阈值 {thresh:.0%}), "
                         f"价格: {b['price_then']:.4f} → {b['price_now']:.4f}",
                         {"change_pct": change, "threshold": thresh,
                          "current_price": b["price_now"],
                          "window": window})
        except Exception as e:
            emit(handlers, "WARNING", "system", title, f"价格数据获取失败: {e}")
        time.sleep(0.2)

    # -----------------------------------------------------------------------
    # 4. Volume analysis
    # -----------------------------------------------------------------------
    volume_data_map = {}
    for cid, minfo in markets.items():
        title = minfo.get("title", cid[:12])
        try:
            trades = fetch_market_trades(cid, limit=200, since_ts=prev_ts)
            metrics = compute_volume_metrics(trades)
            volume_data_map[cid] = metrics

            prev_vol = _get_prev_volume(prev_state, cid)
            if prev_vol is not None and prev_vol > 0:
                anomaly = check_volume_anomaly(
                    metrics["interval_volume_usd"], prev_vol,
                    spike_ratio=volume_spike, drop_ratio=volume_drop,
                )
                if anomaly:
                    atype = anomaly["type"]
                    label = "暴涨" if atype == "spike" else "骤降"
                    level = "ALERT" if atype == "spike" else "WARNING"
                    emit(handlers, level, "volume", title,
                         f"成交量{label}: ${metrics['interval_volume_usd']:.0f} "
                         f"(均值 ${prev_vol:.0f}, 倍率 {anomaly['ratio']:.1f}x)",
                         {"volume_current": metrics["interval_volume_usd"],
                          "volume_avg": prev_vol,
                          "ratio": anomaly["ratio"],
                          "anomaly_type": atype})

            if metrics["largest_trade_usd"] >= min_inflow_usd:
                lt = metrics["largest_trade"]
                emit(handlers, "WARNING", "volume", title,
                     f"大额交易: {lt['side']} ${lt['usd']:.0f} "
                     f"({lt['size']:.0f} 份 @ {lt['price']:.4f})",
                     {"largest_trade": lt})
        except Exception as e:
            emit(handlers, "WARNING", "system", title, f"成交量数据获取失败: {e}")
        time.sleep(0.2)

    # -----------------------------------------------------------------------
    # 5. Position change detection
    # -----------------------------------------------------------------------
    if prev_state:
        _detect_position_changes(
            prev_state.get("positions", {}),
            positions_by_addr,
            position_change_pct,
            min_inflow_usd,
            handlers,
        )

    # -----------------------------------------------------------------------
    # 6. Order change detection
    # -----------------------------------------------------------------------
    if prev_state and orders:
        _detect_order_changes(prev_state.get("orders", []), orders, handlers)

    # -----------------------------------------------------------------------
    # 7. Whale activity
    # -----------------------------------------------------------------------
    if watched_addresses and condition_ids:
        lookback = prev_ts or (now_ts - 300)
        try:
            whale_trades = check_whale_activity(
                watched_addresses, condition_ids, since_ts=lookback,
            )
            for wt in whale_trades:
                title_str = wt.get("title", wt["condition_id"][:12])
                emit(handlers, "ALERT", "whale", title_str,
                     f"[{wt['label']}] {wt['side']} {wt['size']:.0f} 份 "
                     f"@ {wt['price']:.4f} (${wt['usd']:.0f})",
                     {"address": wt["address"], "label": wt["label"],
                      "side": wt["side"], "size": wt["size"],
                      "price": wt["price"]})
        except Exception as e:
            emit(handlers, "WARNING", "system", "", f"监控地址检测失败: {e}")

    # -----------------------------------------------------------------------
    # Build and return state
    # -----------------------------------------------------------------------
    serializable_positions = {}
    for addr, ps in positions_by_addr.items():
        serializable_positions[addr] = [
            {k: v for k, v in p.items() if k != "raw"} for p in ps
        ]

    return _build_state(
        now_str, now_ts, serializable_positions,
        orders, price_data_map, volume_data_map, markets,
    )


# ---------------------------------------------------------------------------
# Detection helpers
# ---------------------------------------------------------------------------

def _price_alert_level(window: str) -> str:
    """Map time window to alert severity."""
    if window in ("240m",):
        return "CRITICAL"
    if window in ("60m",):
        return "ALERT"
    return "WARNING"


def _get_prev_volume(prev_state: dict | None, cid: str) -> float | None:
    if not prev_state:
        return None
    vol_map = prev_state.get("volume_data", {})
    prev = vol_map.get(cid)
    if prev:
        return prev.get("interval_volume_usd")
    return None


def _detect_position_changes(prev_positions: dict, curr_positions: dict,
                             change_pct: float, min_usd: float,
                             handlers: list) -> None:
    """Compare positions between cycles and emit alerts."""
    prev_flat = {}
    for addr, ps in prev_positions.items():
        for p in ps:
            key = (addr, p.get("market_id", ""), p.get("outcome", ""))
            prev_flat[key] = p

    curr_flat = {}
    for addr, ps in curr_positions.items():
        for p in ps:
            key = (addr, p.get("market_id", ""), p.get("outcome", ""))
            curr_flat[key] = p

    for key, cp in curr_flat.items():
        title = cp.get("title", key[1][:12])
        if key not in prev_flat:
            val = cp.get("current_value", 0)
            if val >= min_usd:
                emit(handlers, "ALERT", "position", title,
                     f"新仓位: {cp.get('outcome', '')} "
                     f"{cp.get('size', 0):.0f} 份, 价值 ${val:.0f}",
                     {"outcome": cp.get("outcome"), "size": cp.get("size"),
                      "value": val, "type": "new"})
            continue

        pp = prev_flat[key]
        prev_size = pp.get("size", 0)
        curr_size = cp.get("size", 0)
        if prev_size > 0:
            size_change = (curr_size / prev_size) - 1.0
            if abs(size_change) >= change_pct:
                direction = "增加" if size_change > 0 else "减少"
                emit(handlers, "WARNING", "position", title,
                     f"仓位{direction} {abs(size_change):.1%}: "
                     f"{prev_size:.0f} → {curr_size:.0f} 份",
                     {"prev_size": prev_size, "curr_size": curr_size,
                      "change_pct": size_change, "type": "change"})

    for key, pp in prev_flat.items():
        if key not in curr_flat:
            title = pp.get("title", key[1][:12])
            emit(handlers, "WARNING", "position", title,
                 f"仓位关闭: {pp.get('outcome', '')} "
                 f"{pp.get('size', 0):.0f} 份",
                 {"outcome": pp.get("outcome"), "size": pp.get("size"),
                  "type": "closed"})


def _detect_order_changes(prev_orders: list, curr_orders: list,
                          handlers: list) -> None:
    """Compare orders between cycles."""
    prev_ids = {o.get("order_id"): o for o in prev_orders if o.get("order_id")}
    curr_ids = {o.get("order_id"): o for o in curr_orders if o.get("order_id")}

    for oid, co in curr_ids.items():
        if oid not in prev_ids:
            emit(handlers, "INFO", "order", co.get("market", "")[:20],
                 f"新挂单: {co['side']} {co['size']:.0f} 份 @ {co['price']:.4f}",
                 {"order_id": oid, "side": co["side"],
                  "size": co["size"], "price": co["price"],
                  "type": "new"})
            continue

        po = prev_ids[oid]
        prev_matched = po.get("size_matched", 0)
        curr_matched = co.get("size_matched", 0)
        if curr_matched > prev_matched:
            filled = curr_matched - prev_matched
            emit(handlers, "INFO", "order", co.get("market", "")[:20],
                 f"挂单部分成交: +{filled:.0f} 份 (共 {curr_matched:.0f}/{co['size']:.0f})",
                 {"order_id": oid, "filled": filled, "type": "partial_fill"})

    for oid, po in prev_ids.items():
        if oid not in curr_ids:
            if po.get("size_matched", 0) >= po.get("size", 1) * 0.99:
                emit(handlers, "INFO", "order", po.get("market", "")[:20],
                     f"挂单完全成交: {po['side']} {po['size']:.0f} 份 @ {po['price']:.4f}",
                     {"order_id": oid, "type": "filled"})
            else:
                emit(handlers, "INFO", "order", po.get("market", "")[:20],
                     f"挂单消失/撤销: {po['side']} {po['size']:.0f} 份 @ {po['price']:.4f}",
                     {"order_id": oid, "type": "cancelled"})


# ---------------------------------------------------------------------------
# State builder
# ---------------------------------------------------------------------------

def _build_state(timestamp: str, timestamp_unix: int,
                 positions: dict, orders: list,
                 price_data: dict, volume_data: dict,
                 markets: dict) -> dict:
    # Ensure price_data is serializable (strip non-JSON types)
    clean_price = {}
    for cid, pd in price_data.items():
        clean_price[cid] = {
            "current_price": pd.get("current_price"),
            "current_time": pd.get("current_time"),
        }

    return {
        "timestamp": timestamp,
        "timestamp_unix": timestamp_unix,
        "positions": positions,
        "orders": orders,
        "price_data": clean_price,
        "volume_data": {
            cid: {
                "interval_volume_usd": vd.get("interval_volume_usd", 0),
                "total_volume_usd": vd.get("total_volume_usd", 0),
                "total_trades": vd.get("total_trades", 0),
            }
            for cid, vd in volume_data.items()
        },
        "markets": {
            cid: {k: v for k, v in m.items()}
            for cid, m in markets.items()
        },
    }


# ---------------------------------------------------------------------------
# Header & main loop
# ---------------------------------------------------------------------------

def print_header(config: dict, interval: int):
    now = datetime.now(timezone.utc)
    addrs = config.get("user_addresses", [])
    watched = config.get("watched_addresses", [])
    notif = config.get("notifications", {})

    channels = ["Console", "File"]
    if notif.get("telegram", {}).get("enabled"):
        channels.append("Telegram")
    if notif.get("email", {}).get("enabled"):
        channels.append("Email")

    print(f"\n{Colors.BOLD}{'=' * 62}{Colors.RESET}")
    print(f"{Colors.BOLD}[{now.strftime('%Y-%m-%d %H:%M UTC')}] "
          f"Polymarket Position Monitor Started{Colors.RESET}")
    print(f"钱包地址: {len(addrs)} 个")
    print(f"监控地址: {len(watched)} 个")
    print(f"通知渠道: {', '.join(channels)}")
    print(f"监控间隔: {interval} 秒")
    thresholds = config.get("thresholds", {}).get("price_change", {})
    if thresholds:
        parts = [f"{k}: {v:.0%}" for k, v in thresholds.items()]
        print(f"价格阈值: {', '.join(parts)}")
    print(f"{Colors.BOLD}{'-' * 62}{Colors.RESET}")


_running = True


def _signal_handler(signum, frame):
    global _running
    _running = False
    print(f"\n{Colors.YELLOW}[INFO] 正在优雅关闭...{Colors.RESET}")


def main():
    parser = argparse.ArgumentParser(description="Polymarket position monitor")
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--interval", type=int, default=None,
                        help="Override interval in seconds")
    parser.add_argument("--once", action="store_true",
                        help="Run a single cycle and exit")
    args = parser.parse_args()

    config = load_config(args.config)
    interval = args.interval or config.get("monitor", {}).get("interval_seconds", 60)
    state_dir = os.path.expanduser(
        config.get("monitor", {}).get("state_dir", "~/polymarket-monitoring")
    )

    handlers = build_handlers(config)

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    if args.once:
        print_header(config, 0)
        prev_state = load_state(state_dir)
        new_state = run_cycle(config, handlers, prev_state)
        save_state(state_dir, new_state)
        print(f"{Colors.BOLD}{'-' * 62}{Colors.RESET}")
        print(f"{Colors.GREEN}状态已保存到 {state_dir}/monitor-state.json{Colors.RESET}")
        return

    print_header(config, interval)

    global _running
    while _running:
        prev_state = load_state(state_dir)

        print(f"\n{Colors.CYAN}[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] "
              f"开始第 {'1' if not prev_state else 'N'} 轮监控...{Colors.RESET}")

        new_state = run_cycle(config, handlers, prev_state)
        save_state(state_dir, new_state)

        if not _running:
            break

        next_check = datetime.now(timezone.utc) + timedelta(seconds=interval)
        print(f"{Colors.DIM}  下一轮: {interval}s 后 "
              f"({next_check.strftime('%H:%M:%S UTC')}){Colors.RESET}")

        for _ in range(interval):
            if not _running:
                break
            time.sleep(1)

    print(f"\n{Colors.BOLD}{'=' * 62}{Colors.RESET}")
    print(f"{Colors.GREEN}监控已停止。状态保存在 {state_dir}/{Colors.RESET}")


if __name__ == "__main__":
    main()
