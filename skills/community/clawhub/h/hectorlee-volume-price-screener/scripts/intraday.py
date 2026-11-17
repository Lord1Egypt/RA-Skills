#!/usr/bin/env python3
"""
盘中监控模块 V3.5
==================
基于通达信 5 分钟 K 线，实时检测盘中放量突破信号。

V3.5 更新:
- MCP 连接预检：启动时测试连接，失败立即报错不再静默扫描
- 量比阈值修正：盘中尾段/头段比使用日线阈值的60%（最低1.2x）
- 错误统计：扫描完成后报告 MCP 调用失败数及错误率

两种模式:
  1. 预检模式(--today): 全市场扫描，检查今日是否出现新的放量锚点
  2. 监控模式(--watchlist): 针对已有命中池，监测形态延续/破坏

用法:
  python intraday.py --today                          # 全市场盘中预检
  python intraday.py --today --top 20                 # Top 20
  python intraday.py --watchlist                      # 监控上次扫描命中池
  python intraday.py 600406 300750                    # 指定股票监控
"""

import json
import os
import sys
import time
from typing import Optional, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pattern_detect import DEFAULT_PARAMS, get_rise_threshold, is_gem, is_star, is_bj
from data_provider import get_all_stocks
from colors import RED, GREEN, YELLOW, CYAN, GRAY, BOLD, RESET
from mcp_utils import McpClient


# MCP 错误追踪（跨线程共享）
_mcp_error_count = 0
_mcp_error_msg = None


def _call_mcp(name: str, args: dict) -> Optional[dict]:
    """调用 MCP 工具"""
    global _mcp_error_count, _mcp_error_msg
    result = McpClient.get().call_tool(name, args)
    if result and result.get("raw_text", "").startswith("Error:"):
        if _mcp_error_msg is None:
            _mcp_error_msg = result["raw_text"]
        _mcp_error_count += 1
        return None
    return result


def _check_mcp_health() -> bool:
    """预检 MCP 连接状态，失败时打印诊断信息"""
    result = _call_mcp("tdx-connector_tdx_kline", {
        "code": "600406", "setcode": "1", "period": "1", "wantNum": 1,
    })
    if result is None:
        print(f"{YELLOW}⚠ MCP 连接失败: {_mcp_error_msg or '工具不可用或无响应'}{RESET}")
        print(f"{YELLOW}  请确认通达信 connector 已在 WorkBuddy 中连接并启用{RESET}")
        return False
    if "Rows" not in result or not result["Rows"]:
        print(f"{YELLOW}⚠ 通达信 K 线数据为空，盘中监控无法继续{RESET}")
        return False
    return True


def get_intraday_bars(code: str, setcode: str = "1", count: int = 48) -> Optional[List[dict]]:
    """获取 5 分钟 K 线（今日盘中）

    Args:
        code: 纯数字代码
        setcode: '1'沪 '0'深
        count: 拉取条数（48=4小时/240分钟）

    Returns: [{date, time, open, high, low, close, volume}, ...] 或 None
    """
    result = _call_mcp("tdx-connector_tdx_kline", {
        "code": code, "setcode": setcode, "period": "0", "wantNum": count,
    })
    if not result:
        return None

    rows = result.get("Rows")
    if not rows:
        return None

    bars = []
    for row in rows:
        try:
            bars.append({
                "datetime": f"{row.get('Data','')} {row.get('Second','')}",
                "open": float(row.get("Open", 0)),
                "high": float(row.get("High", 0)),
                "low": float(row.get("Low", 0)),
                "close": float(row.get("Close", 0)),
                "volume": float(row.get("Volume", 0)),
            })
        except (ValueError, TypeError):
            continue
    return bars


def check_today_anchor(code: str, setcode: str, params: dict) -> Optional[dict]:
    """检查今日盘中是否出现放量锚点（仅阶段1）

    V3.4 fix: 
    - 量基线用中段bars(排除开盘高量期)
    - 量比用近期/早期滚动对比
    - 最低5条bar即可检测（不错过早盘信号）

    Returns: {code, surge_pct, volume_ratio, latest_price, ...} 或 None
    """
    bars = get_intraday_bars(code, setcode, count=48)
    if not bars or len(bars) < 5:
        return None

    n = len(bars)
    today_open = bars[0]["open"]
    today_high = max(b["high"] for b in bars)
    today_low = min(b["low"] for b in bars)
    today_close = bars[-1]["close"]
    today_vol = sum(b["volume"] for b in bars)

    if today_open <= 0:
        return None

    # 今日涨幅
    surge_pct = (today_close - today_open) / today_open * 100.0

    # 量比：近期1/4 vs 早期3/4（滚动对比，自动适应开盘高量）
    split = max(1, n // 4)
    early_bars = bars[:-split] if n > split else bars[:n//2]
    late_bars = bars[-split:]

    if not early_bars or not late_bars:
        return None

    early_avg = sum(b["volume"] for b in early_bars) / len(early_bars)
    late_avg = sum(b["volume"] for b in late_bars) / len(late_bars)
    vol_ratio = late_avg / early_avg if early_avg > 0 else 1.0

    # 阈值：不传avg_vol（避免分档误判），用纯板块阈值
    rise_th, vol_th = get_rise_threshold(code, params)
    # V3.5 fix: 盘中量比（尾段/头段）天然低于日线量比（今日/20日均量），
    # 将阈值降至原始日线阈值的60%（最低1.2x）
    intraday_vol_th = max(1.2, vol_th * 0.6)

    if surge_pct >= rise_th - 1e-9 and vol_ratio >= intraday_vol_th - 1e-9:
        return {
            "code": code,
            "surge_pct": surge_pct,
            "volume_ratio": vol_ratio,
            "price": today_close,
            "high": today_high,
            "low": today_low,
            "open": today_open,
            "bars_count": n,
        }
    return None


def color_pct(pct: float) -> str:
    if pct > 0:
        return f"{RED}+{pct:.2f}%{RESET}"
    return f"{GREEN}{pct:.2f}%{RESET}"


def run_today_scan(top: int = 20):
    """全市场盘中预检：检查哪些股票今日出现放量"""
    global _mcp_error_count, _mcp_error_msg

    # V3.5: 预检 MCP 连接
    if not _check_mcp_health():
        return

    stocks = get_all_stocks(include_bj=False, include_star=True)
    codes = [(s["pure_code"], s["code"], s["name"]) for s in stocks]

    print(f"\n{BOLD}═══ 盘中监控 V3.5 — 今日放量预检（{len(codes)}只）═══{RESET}\n")

    params = dict(DEFAULT_PARAMS)
    alerts = []
    error_count = 0

    # 分批检测（每批 50 只，避免 MCP 过载）
    batch_size = 50
    total = 0
    for i in range(0, len(codes), batch_size):
        batch = codes[i:i + batch_size]
        with ThreadPoolExecutor(max_workers=5) as ex:
            futures = {}
            for pure, full, name in batch:
                setc = "1" if pure.startswith(("6", "68", "9")) else "0"
                futures[ex.submit(check_today_anchor, pure, setc, params)] = (full, name)

            for fut in as_completed(futures):
                full, name = futures[fut]
                try:
                    result = fut.result()
                    if result:
                        result["name"] = name
                        result["full_code"] = full
                        alerts.append(result)
                except Exception:
                    error_count += 1
                total += 1

        elapsed = min(i + batch_size, len(codes))
        print(f"\r{GRAY}  扫描进度: {elapsed}/{len(codes)}  命中: {len(alerts)}"
              f"{f'  错误: {_mcp_error_count}' if _mcp_error_count > 0 else ''}{RESET}", end="")

    print()
    if _mcp_error_count > 0:
        print(f"{YELLOW}⚠ MCP 调用失败 {_mcp_error_count} 次 ({_mcp_error_count/total*100:.1f}%){RESET}")
        if _mcp_error_count / total > 0.5:
            print(f"{YELLOW}  错误率过高，结果不可信。请检查通达信 connector 连接状态{RESET}")

    if not alerts:
        print(f"{GRAY}今日盘中暂无符合阈值的放量信号{RESET}")
        return

    alerts.sort(key=lambda x: -x["surge_pct"])
    print(f"\n{BOLD}今日盘中放量信号: {len(alerts)}只{RESET}\n")

    for a in alerts[:top]:
        tag = ""
        pure = a["code"]
        if is_gem(pure):
            tag = f"{CYAN}[创业板]{RESET} "
        elif is_star(pure):
            tag = f"{CYAN}[科创板]{RESET} "

        print(f"  {tag}{a['full_code']} {a['name']:<8s} "
              f"{BOLD}{a['price']:.2f}{RESET} {color_pct(a['surge_pct'])} "
              f"{GRAY}量比{a['volume_ratio']:.1f} "
              f"高{a['high']:.2f} 低{a['low']:.2f}{RESET}")

    if len(alerts) > top:
        print(f"\n{GRAY}... 共 {len(alerts)} 只，仅显示前 {top} 只{RESET}")


def run_watchlist_monitor(codes_list: List[str] = None):
    """监控已有命中池的盘中表现"""
    if codes_list is None:
        # 读取上次扫描的命中池
        print(f"{YELLOW}请指定股票代码或使用 --today 模式{RESET}")
        return

    params = dict(DEFAULT_PARAMS)
    print(f"\n{BOLD}═══ 盘中监控 — 监视 {len(codes_list)} 只 ==={RESET}\n")

    for raw_code in codes_list:
        pure = "".join(c for c in raw_code if c.isdigit())
        setc = "1" if pure.startswith(("6", "68", "9")) else "0"

        bars = get_intraday_bars(pure, setc, count=48)
        if not bars or len(bars) < 5:
            print(f"  {GRAY}{pure} 无盘中数据{RESET}")
            continue

        today_open = bars[0]["open"]
        today_close = bars[-1]["close"]
        today_high = max(b["high"] for b in bars)
        today_low = min(b["low"] for b in bars)
        change = (today_close - today_open) / today_open * 100 if today_open > 0 else 0

        # 简单趋势判断
        first_half_close = bars[len(bars) // 2]["close"] if len(bars) > 2 else today_open
        trend = "↑持续走强" if today_close > first_half_close else "↓午后回落"

        color = RED if change > 0 else GREEN
        print(f"  {pure} {color}{change:+.2f}%{RESET} "
              f"{GRAY}开{today_open:.2f} 高{today_high:.2f} 低{today_low:.2f} "
              f"收{today_close:.2f} {trend}{RESET}")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="盘中监控 V3.4")
    ap.add_argument("codes", nargs="*", help="监控指定股票")
    ap.add_argument("--today", action="store_true", help="全市场盘中预检")
    ap.add_argument("--watchlist", action="store_true", help="监控上次命中池")
    ap.add_argument("--top", type=int, default=20, help="显示 Top N")

    args = ap.parse_args()

    if args.today:
        run_today_scan(top=args.top)
    elif args.codes:
        run_watchlist_monitor(args.codes)
    elif args.watchlist:
        print(f"{YELLOW}--watchlist 模式需提供股票代码。用法: python intraday.py 600406 300750{RESET}")
    else:
        ap.print_help()
