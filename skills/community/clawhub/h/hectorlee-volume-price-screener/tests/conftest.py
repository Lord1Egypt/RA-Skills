#!/usr/bin/env python3
"""pytest 共享夹具：合成 K 线生成器 + 模块路径配置"""
import os
import sys

# 确保可以 import scripts 下的模块
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import pytest
from pattern_detect import Bar


def build_kline(n=60, anchor=45, surge_pct=7.0, vol_ratio=2.2,
                post_days=None, post_vol_ratio=0.4, post_amp=0.005,
                trend=0.005, base_vol=1000.0, base_price=10.0):
    """构造合成 K 线

    参数:
        n: 总 K 线数
        anchor: 放量拉升日索引
        surge_pct: 放量日涨幅(%)
        vol_ratio: 放量日量比（相对前20日均量，基础量为 base_vol）
        post_days: 放量后横盘天数（默认 n-anchor-1）
        post_vol_ratio: 横盘日量 / 放量日量
        post_amp: 横盘日单日最大波动幅度（相对锚点收盘）
        trend: 放量前每日基础涨幅（如 0.005 = +0.5%/日）
    """
    if post_days is None:
        post_days = n - anchor - 1
    bars = []
    price = base_price
    vol_ma_base = base_vol  # 前20日均量（基础段全为 base_vol）
    dates = [f"2026-01-{i+1:02d}" for i in range(n)]

    # 基础段: 索引 0 .. anchor-1（隔日阴阳交替，避免全阳触发E检测）
    for i in range(anchor):
        prev = price
        # odd days: yang, even days: yin (alternating to avoid pre_surge >= 5)
        if i % 3 == 0:
            price = prev * (1 + trend * 0.8)  # yang
        elif i % 3 == 1:
            price = prev * (1 - trend * 0.3)  # yin
        else:
            price = prev * (1 + trend * 0.5)  # yang
        bars.append(Bar(
            date=dates[i], open=prev, high=max(prev, price) * 1.002,
            low=min(prev, price) * 0.998, close=price, volume=base_vol,
        ))

    # 放量拉升日: anchor
    prev_close = bars[-1].close
    open_p = prev_close * 1.01
    close_p = prev_close * (1 + surge_pct / 100.0)
    high_p = max(open_p, close_p) * 1.003
    low_p = min(open_p, close_p) * 0.997
    anchor_vol = vol_ma_base * vol_ratio
    bars.append(Bar(
        date=dates[anchor], open=open_p, high=high_p, low=low_p,
        close=close_p, volume=anchor_vol,
    ))
    anchor_bar = bars[-1]

    # 横盘缩量段: anchor+1 .. 末尾（收盘锚定在锚点高低点区间内）
    for i in range(1, post_days + 1):
        # 在锚点 [low, high] 区间内小幅波动
        w = post_amp * 2 * (((i * 7) % 11) / 11.0 - 0.5)   # 确定性伪波动
        close_i = close_p * (1 + w)
        close_i = min(max(close_i, anchor_bar.low), anchor_bar.high)
        open_i = close_i * (1 - 0.001)
        vol_i = anchor_vol * post_vol_ratio
        bars.append(Bar(
            date=dates[anchor + i], open=open_i,
            high=close_i * 1.002, low=close_i * 0.998,
            close=close_i, volume=vol_i,
        ))

    return bars


@pytest.fixture
def standard_bars():
    """标准命中形态：放量+7%量比2.2，后14日缩量横盘"""
    return build_kline()


@pytest.fixture
def mainboard_code():
    return "000001"


@pytest.fixture
def gem_code():
    return "300001"
