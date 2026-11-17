#!/usr/bin/env python3
"""
盘中监控模块 — 腾讯实时行情版 V1.0
====================================
替代 TDX MCP 方案，使用腾讯 qt.gtimg.cn 实时行情接口。
无需充值，免费使用。

与 intraday.py (TDX版) 的区别:
  - 数据源: 腾讯实时行情 (qt.gtimg.cn) vs TDX 5分钟K线
  - 量比: 当日量/5日均量 (更准确) vs 盘中尾段/头段比
  - 换手率: ✅ 支持 vs ❌ 日线不支持
  - 速度: ~30s 全市场 vs ~34s (TDX无连接时静默失败)

用法:
  python intraday_tencent.py                    # 全市场盘中监控
  python intraday_tencent.py --top 30           # Top 30
  python intraday_tencent.py --min-score 80     # 最低涨幅5%  
  python intraday_tencent.py 600406 688111      # 指定股票
"""

import argparse
import sys
import os
import time
from collections import Counter
from typing import List, Optional, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pattern_detect import DEFAULT_PARAMS, get_rise_threshold
from data_provider import get_all_stocks
from colors import RED, GREEN, YELLOW, CYAN, GRAY, BOLD, RESET, MAGENTA

TENCENT_QUOTE_BATCH_URL = "https://qt.gtimg.cn/q={codes}"
BATCH_SIZE = 80  # 腾讯接口单次最多约80只


def fetch_quotes_batch_tencent(raw_codes: List[str]) -> Dict[str, dict]:
    """批量拉取实时行情（腾讯接口）
    
    Args:
        raw_codes: 腾讯格式代码列表，如 ['sh600406', 'sz002415', ...]
    
    Returns: {code: {name, price, change_pct, vol_ratio, turnover, volume, ...}}
    """
    results = {}
    for i in range(0, len(raw_codes), BATCH_SIZE):
        batch = raw_codes[i:i + BATCH_SIZE]
        url = TENCENT_QUOTE_BATCH_URL.format(codes=",".join(batch))
        try:
            resp = requests.get(url, timeout=15)
            resp.encoding = "gbk"
            text = resp.text
            
            for line in text.strip().split("\n"):
                line = line.strip().strip(";")
                if "=" not in line:
                    continue
                var, data = line.split("=", 1)
                if data.startswith('"') and data.endswith('"'):
                    data = data[1:-1]
                fields = data.split("~")
                if len(fields) < 50:
                    continue
                
                code = var.split("_")[-1] if "_" in var else var
                try:
                    price = float(fields[3]) if fields[3] else 0.0
                    change_pct = float(fields[32]) if fields[32] else 0.0
                    vol_ratio = float(fields[49]) if fields[49] else 0.0
                    turnover = float(fields[38]) if fields[38] else 0.0
                    volume = int(float(fields[6])) if fields[6] else 0
                    high = float(fields[33]) if fields[33] else 0.0
                    low = float(fields[34]) if fields[34] else 0.0
                    open_price = float(fields[5]) if fields[5] else 0.0
                    pre_close = float(fields[4]) if fields[4] else 0.0
                    amount = float(fields[37]) if fields[37] else 0.0  # 成交额(万)
                except (ValueError, IndexError):
                    continue
                
                if price <= 0:
                    continue
                
                # ST 过滤
                name = fields[1]
                if "ST" in name or "*ST" in name:
                    continue
                
                results[code] = {
                    "code": code,
                    "name": name,
                    "price": price,
                    "change_pct": change_pct,
                    "vol_ratio": vol_ratio,
                    "turnover": turnover,
                    "volume": volume,
                    "high": high,
                    "low": low,
                    "open": open_price,
                    "pre_close": pre_close,
                    "amount": amount,
                }
        except Exception as e:
            print(f"{YELLOW}⚠ 批量查询失败 (batch {i//BATCH_SIZE+1}): {e}{RESET}", file=sys.stderr)
            continue
    
    return results


def color_pct(pct: float) -> str:
    if pct > 0:
        return f"{RED}+{pct:.2f}%{RESET}"
    if pct == 0:
        return f"{pct:.2f}%"
    return f"{GREEN}{pct:.2f}%{RESET}"


def scan_intraday(top: int = 30, min_score: float = None):
    """全市场盘中监控（腾讯实时行情版）"""
    
    # 获取股票列表
    print(f"\n{GRAY}正在获取股票列表...{RESET}", end="", flush=True)
    stocks = get_all_stocks(include_bj=False, include_star=True)
    print(f" {len(stocks)}只")
    
    # 构建腾讯格式代码
    tencent_codes = [s["code"] for s in stocks]
    
    # 批量拉取行情
    print(f"{GRAY}正在拉取实时行情（{len(tencent_codes)}只，{len(tencent_codes)//BATCH_SIZE+1}批）...{RESET}")
    t0 = time.time()
    quotes = fetch_quotes_batch_tencent(tencent_codes)
    t1 = time.time()
    print(f"{GRAY}行情拉取完成（{t1-t0:.1f}s），命中 {len(quotes)} 只有效行情{RESET}")
    
    if not quotes:
        print(f"{RED}未获取到任何行情数据，请检查网络{RESET}")
        return
    
    # 筛选放量信号
    params = dict(DEFAULT_PARAMS)
    alerts = []
    skipped_st = 0
    skipped_no_vol = 0
    
    for code, quote in quotes.items():
        pure = "".join(c for c in code if c.isdigit())
        name = quote["name"]
        surge = quote["change_pct"]
        vol_ratio = quote["vol_ratio"]
        turnover = quote["turnover"]
        
        # 获取板块阈值
        rise_th, vol_th = get_rise_threshold(pure, params)
        
        # 涨幅检查
        if surge < rise_th - 0.01:
            continue
        
        # 量比检查
        if vol_ratio < vol_th - 0.01:
            skipped_no_vol += 1
            continue
        
        # 换手率检查（主板≥3%，科创/创业板放宽至2%）
        min_turnover = 2.0 if pure.startswith(("688", "300", "301")) else 3.0
        if turnover < min_turnover:
            continue
        
        alerts.append({
            "code": code,
            "pure_code": pure,
            "name": name,
            "price": quote["price"],
            "change_pct": surge,
            "vol_ratio": vol_ratio,
            "turnover": turnover,
            "volume": quote["volume"],
            "high": quote["high"],
            "low": quote["low"],
            "open": quote["open"],
            "pre_close": quote["pre_close"],
            "amount": quote["amount"],
            "rise_th": rise_th,
            "vol_th": vol_th,
        })
    
    # 排序：按涨幅降序
    alerts.sort(key=lambda x: -x["change_pct"])
    
    # 输出
    print(f"\n{BOLD}═══ 盘中实时放量监控 V1.0（腾讯行情）═══{RESET}")
    print(f"{GRAY}扫描: {len(tencent_codes)}只 | 有效行情: {len(quotes)}只 | 命中: {len(alerts)}只{RESET}")
    print(f"{GRAY}涨幅≥主板3-5% 创业板6% 科创4% | 量比≥1.5-3.0(板块差异化) | 换手≥2-3%{RESET}\n")
    
    if not alerts:
        print(f"{GRAY}今日盘中暂无符合阈值的放量信号{RESET}")
        if skipped_no_vol > 0:
            print(f"{GRAY}（涨幅达标但量比不足: {skipped_no_vol}只）{RESET}")
        return
    
    # Top N
    show_n = min(top, len(alerts))
    for i, a in enumerate(alerts[:show_n], 1):
        # 板块标签
        pure = a["pure_code"]
        if pure.startswith(("688",)):
            tag = f"{CYAN}[科创]{RESET}"
        elif pure.startswith(("300", "301")):
            tag = f"{CYAN}[创业]{RESET}"
        elif pure.startswith(("60",)):
            tag = f"{GRAY}[沪]{RESET}"
        else:
            tag = f"{GRAY}[深]{RESET}"
        
        # 涨停标记
        limit_tag = ""
        if a["change_pct"] >= 19.9 or abs(a["price"] - a["high"]) < 0.01:
            limit_tag = f" {RED}[涨停]{RESET}"
        
        amount_str = f"{a['amount']/10000:.1f}亿" if a['amount'] >= 10000 else f"{a['amount']:.0f}万"
        
        print(f"  {i:2d}. {tag} {a['code']} {BOLD}{a['name']:<8s}{RESET} "
              f"{BOLD}{a['price']:.2f}{RESET} {color_pct(a['change_pct'])} "
              f"量比{GREEN}{a['vol_ratio']:.1f}{RESET} "
              f"换手{CYAN}{a['turnover']:.1f}%{RESET} "
              f"额{amount_str}{limit_tag}")
    
    if len(alerts) > show_n:
        print(f"\n{GRAY}... 共 {len(alerts)} 只，仅显示前 {show_n} 只{RESET}")
    
    # 板块统计
    print(f"\n{BOLD}板块分布{RESET}")
    sectors = Counter()
    for a in alerts:
        pure = a["pure_code"]
        if pure.startswith("688"):
            sectors["科创板"] += 1
        elif pure.startswith(("300", "301")):
            sectors["创业板"] += 1
        elif pure.startswith("60"):
            sectors["沪主板"] += 1
        elif pure.startswith(("00", "002")):
            sectors["深主板"] += 1
        else:
            sectors["其他"] += 1
    for s, c in sectors.most_common():
        print(f"  {s}: {c}只")
    
    t2 = time.time()
    print(f"\n{GRAY}总耗时 {t2-t0:.1f}s{RESET}")


def check_specific(codes: List[str]):
    """指定股票盘中检测"""
    # 规范化代码
    from data_provider import _normalize_code
    tencent_codes = [_normalize_code(c) for c in codes]
    
    print(f"\n{GRAY}查询 {len(codes)} 只股票...{RESET}")
    quotes = fetch_quotes_batch_tencent(tencent_codes)
    
    if not quotes:
        print(f"{RED}未获取到行情数据{RESET}")
        return
    
    params = dict(DEFAULT_PARAMS)
    
    for tc, quote in quotes.items():
        pure = "".join(c for c in tc if c.isdigit())
        rise_th, vol_th = get_rise_threshold(pure, params)
        surge = quote["change_pct"]
        vol_r = quote["vol_ratio"]
        turnover = quote["turnover"]
        
        surge_ok = surge >= rise_th - 0.01
        vol_ok = vol_r >= vol_th - 0.01
        min_to = 2.0 if pure.startswith(("688", "300", "301")) else 3.0
        turnover_ok = turnover >= min_to
        
        status = f"{GREEN}✅ 放量{RESET}" if (surge_ok and vol_ok and turnover_ok) else f"{GRAY}—{RESET}"
        detail = []
        if not surge_ok:
            detail.append(f"{RED}涨幅不足(需≥{rise_th}%){RESET}")
        if not vol_ok:
            detail.append(f"{YELLOW}量比不足(需≥{vol_th}){RESET}")
        if not turnover_ok:
            detail.append(f"{GRAY}换手不足(需≥{min_to}%){RESET}")
        
        detail_str = " | ".join(detail) if detail else ""
        
        print(f"  {tc} {quote['name']:<8s} {quote['price']:.2f} {color_pct(surge)} "
              f"量比{vol_r:.1f} 换手{turnover:.1f}% {status}")
        if detail_str:
            print(f"    {GRAY}{detail_str}{RESET}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="盘中实时放量监控 — 腾讯行情版 V1.0")
    ap.add_argument("codes", nargs="*", help="指定股票代码")
    ap.add_argument("--top", type=int, default=30, help="显示 Top N（默认30）")
    ap.add_argument("--min-score", type=float, help="最低涨幅（覆盖板块默认阈值）")
    
    args = ap.parse_args()
    
    if args.codes:
        check_specific(args.codes)
    else:
        scan_intraday(top=args.top, min_score=args.min_score)
