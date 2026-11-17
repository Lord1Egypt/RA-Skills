#!/usr/bin/env python3
"""
信号历史追踪模块 V3.5
=====================
读取 data/signals_YYYYMMDD.json 历史文件，
统计每只股票在过去 N 个交易日的命中次数（"关注池曝光度"）。

用法:
    from signal_history import get_recurrence

    freq = get_recurrence()          # {code: count, ...} 最近50日
    count = freq.get("600406", 0)    # 某只股票的曝光次数
"""

import json
import os
import glob
from pathlib import Path
from typing import Dict, Optional


# 信号文件存放目录（相对于脚本目录）
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# 默认回溯窗口（交易日，约2.5个月）
DEFAULT_LOOKBACK = 50


def _parse_date(filename: str) -> Optional[str]:
    """从文件名提取日期：signals_20260803.json → 20260803"""
    import re
    m = re.search(r"signals_(\d{8})\.json", filename)
    return m.group(1) if m else None


def get_recurrence(lookback_days: int = DEFAULT_LOOKBACK) -> Dict[str, int]:
    """读取最近 N 个交易日的信号文件，返回每只股票的历史命中次数

    防污染设计：
      - 按日期去重：同一日期（文件名中的 YYYYMMDD）只计一次
      - 盘中模式（intraday.py）不写入 signals JSON，天然隔离
      - 即使同一天多次运行 screener 且保存到同日期文件，也只计 1 次

    Args:
        lookback_days: 回溯窗口（交易日数，默认50）

    Returns:
        {code: count} 格式，如 {"600406": 3, "000001": 1}
    """
    pattern = str(DATA_DIR / "signals_*.json")
    files = sorted(glob.glob(pattern), reverse=True)[:lookback_days]

    if not files:
        return {}

    # 两层去重：日期去重 + 同日同股只计一次
    recurrence: Dict[str, int] = {}
    for fpath in files:
        file_date = _parse_date(os.path.basename(fpath))
        if not file_date:
            continue

        try:
            with open(fpath, "r", encoding="utf-8") as f:
                records = json.load(f)
        except (json.JSONDecodeError, IOError):
            continue

        if not isinstance(records, list):
            continue

        # 当天已出现的股票（防止同日多次扫描重复计数）
        seen_today: set = set()
        for rec in records:
            if not isinstance(rec, dict):
                continue
            code = rec.get("code", "")
            if not code or code in seen_today:
                continue
            seen_today.add(code)
            recurrence[code] = recurrence.get(code, 0) + 1

    return recurrence


def get_stock_history(code: str, lookback_days: int = DEFAULT_LOOKBACK) -> dict:
    """查询单只股票的历史命中明细

    Returns:
        {"count": 3, "dates": ["20260801", "20260728", ...], "avg_score": 72.5}
    """
    pattern = str(DATA_DIR / "signals_*.json")
    files = sorted(glob.glob(pattern), reverse=True)[:lookback_days]

    count = 0
    dates = []
    scores = []

    for fpath in files:
        date_str = _parse_date(os.path.basename(fpath))
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                records = json.load(f)
        except (json.JSONDecodeError, IOError):
            continue

        if not isinstance(records, list):
            continue

        for rec in records:
            if rec.get("code") == code:
                count += 1
                if date_str:
                    dates.append(date_str)
                sc = rec.get("score", 0)
                if sc:
                    scores.append(sc)
                break  # 同一天只计一次

    return {
        "count": count,
        "dates": dates,
        "avg_score": sum(scores) / len(scores) if scores else 0,
    }


def get_top_recurring(top_n: int = 10,
                       lookback_days: int = DEFAULT_LOOKBACK) -> list:
    """返回近期最频繁出现在关注池的股票

    Returns:
        [(code, count), ...] 按出现次数降序
    """
    freq = get_recurrence(lookback_days)
    sorted_items = sorted(freq.items(), key=lambda x: -x[1])
    return sorted_items[:top_n]


if __name__ == "__main__":
    # 自测
    freq = get_recurrence(50)
    if freq:
        print(f"历史信号文件: {len(freq)} 只股票有记录")
        for code, count in sorted(freq.items(), key=lambda x: -x[1])[:10]:
            print(f"  {code}: {count}次")
    else:
        print("暂无历史信号文件（data/signals_*.json 为空）")
        print("首次收盘扫描后自动生成，后续每日累积")
