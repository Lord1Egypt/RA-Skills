#!/usr/bin/env python3
"""
逻辑覆盖层 V1.4.0 — 四层判断框架固化
=====================================
纯量价模型告诉你"哪里疼"，本模块判断"要不要截肢"。

四层检验（在决策引擎输出之上做最终裁决）：
1. 逻辑证伪检验 —— 基本面逻辑是否被破坏（fundamentals.json 配置）
2. 量价破坏分级 —— 区分"趋势型卖出"(M10/M11，易受外生冲击误杀)与"形态型卖出"(M8/M9，出货特征)
3. 资金承接检验 —— K线识别低位承接日（长下影+放量回收）
4. 事件日历检验 —— 重大事件窗口内，外生冲击类卖出可逆性高

三条核心规则：
- 规则A 逻辑完好豁免：SELL(仅趋势型信号) + 逻辑intact + (承接日|底部反弹|事件窗口) → WATCH
- 规则B 结构性走弱升级：20日无任何修复阳线 + 逻辑非intact → REDUCE/WATCH 升级 SELL
- 规则C 逻辑破坏加速：logic='broken' → 任何非SELL决策至少降为REDUCE

配置文件（与 data/ 同目录）：
- fundamentals.json: {"code": {"logic": "intact|weak|broken", "note": "...", "support": [支撑位], "valid_until": "YYYY-MM-DD"}}
- events.json: [{"date": "YYYY-MM-DD", "name": "FOMC决议", "window": 3}]
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Optional

_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

# 趋势型卖出信号：外生冲击（宏观/板块情绪）容易误杀，逻辑完好时需人工/配置豁免
SOFT_SELL = {'M10峰值回撤', 'M11趋势破位'}
# 形态型卖出信号：出货特征明显，逻辑完好也不轻易豁免
HARD_SELL = {'M8高开诱多', 'M9缩量连阴'}


def load_fundamentals(filepath: str = None) -> dict:
    """加载基本面逻辑配置。过期条目自动忽略。"""
    path = filepath or os.path.join(_DATA_DIR, 'fundamentals.json')
    try:
        with open(path, 'r') as f:
            raw = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    out = {}
    today = datetime.now().strftime('%Y-%m-%d')
    for code, cfg in raw.items():
        if not isinstance(cfg, dict):
            continue
        vu = cfg.get('valid_until')
        if vu and today > vu:
            continue  # 配置过期，视为 unknown，不参与覆盖
        out[code] = cfg
    return out


def load_events(filepath: str = None) -> list:
    """加载事件日历。过期事件自动忽略。"""
    path = filepath or os.path.join(_DATA_DIR, 'events.json')
    try:
        with open(path, 'r') as f:
            raw = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    today = datetime.now().date()
    out = []
    for ev in raw:
        try:
            d = datetime.strptime(ev['date'], '%Y-%m-%d').date()
        except (KeyError, ValueError):
            continue
        window = int(ev.get('window', 2))
        if timedelta(days=-1) <= (d - today) <= timedelta(days=window):
            out.append(ev)
    return out


def detect_absorption_day(kline: List[dict]) -> dict:
    """
    资金承接检验：最新K线为低位承接日。
    条件：下影线 >= 收盘价2% + 收盘位于当日振幅上半部 + 量能 >= 前日1.2x
    （对应实盘"盘中下探关键位被买回"的主力承接结构）
    """
    if len(kline) < 3:
        return {'absorption': False, 'note': ''}
    last = kline[-1]
    prev = kline[-2]
    o, c, h, l = last['open'], last['close'], last['high'], last['low']
    rng = h - l
    if rng <= 0:
        return {'absorption': False, 'note': ''}
    lower_shadow = min(o, c) - l
    lower_pct = lower_shadow / c * 100
    close_pos = (c - l) / rng  # 收盘在振幅中的位置
    vol_ratio = last['volume'] / prev['volume'] if prev['volume'] > 0 else 1
    ok = lower_pct >= 2.0 and close_pos >= 0.55 and vol_ratio >= 1.2
    note = f'承接日(下影{lower_pct:.1f}%/收盘位{close_pos:.0%}/量比{vol_ratio:.1f}x)' if ok else ''
    return {'absorption': ok, 'note': note}


def detect_structural_weakness(kline: List[dict]) -> dict:
    """
    结构性走弱检验：近20日无任何单日涨幅>=2%的阳线（全程无修复日）
    —— 对应"恒玄模式"：每个SELL都有恐慌日背景的票可豁免，
    连一次修复都没有的票是结构性病灶，不可豁免。
    """
    n = len(kline)
    if n < 20:
        return {'structural_weak': False, 'note': ''}
    window = kline[-20:]
    has_repair = False
    for i in range(1, len(window)):
        k, kp = window[i], window[i - 1]
        chg = (k['close'] - kp['close']) / kp['close'] * 100
        if k['close'] > k['open'] and chg >= 2.0:
            has_repair = True
            break
    weak = not has_repair
    return {'structural_weak': weak, 'note': '20日无修复阳线(结构性走弱)' if weak else ''}


def get_fundamental(code: str, fundamentals: dict) -> dict:
    cfg = fundamentals.get(code, {})
    return {'logic': cfg.get('logic', 'unknown'), 'note': cfg.get('note', ''),
            'support': cfg.get('support', [])}


def apply_logic_overlay(decision: str, quality_note: str, code: str,
                        kline: List[dict], detect_result: dict,
                        fundamental: dict, events: list) -> tuple:
    """
    在决策引擎输出之上执行四层裁决。返回 (decision, quality_note, overlay_notes)
    """
    overlay_notes = []
    logic = fundamental.get('logic', 'unknown')
    logic_note = fundamental.get('note', '')

    # --- 量价破坏分级 ---
    sell_signals = (detect_result or {}).get('sell_signals', []) or []
    sell_names = {s.get('name', '') for s in sell_signals}
    only_soft = bool(sell_names) and sell_names.issubset(SOFT_SELL)
    has_hard = bool(sell_names & HARD_SELL)

    # --- 资金承接 ---
    ab = detect_absorption_day(kline)
    if ab['absorption']:
        overlay_notes.append(f'承接信号: {ab["note"]}')

    # --- 结构性走弱 ---
    sw = detect_structural_weakness(kline)
    if sw['structural_weak']:
        overlay_notes.append(sw['note'])

    # --- 事件窗口 ---
    in_event = bool(events)
    if in_event:
        ev_names = '、'.join(e['name'] for e in events)
        overlay_notes.append(f'事件窗口({ev_names}): 外生冲击类卖出可逆性高')

    # === 规则A：逻辑完好豁免（趋势型SELL → WATCH） ===
    if decision == 'sell' and only_soft and logic == 'intact' and (ab['absorption'] or in_event):
        support_txt = '/'.join(str(x) for x in fundamental.get('support', []))
        decision = 'watch'
        quality_note = f'WATCH 逻辑完好豁免(M11/M10趋势型破位+{ "承接" if ab["absorption"] else "事件窗口" })'
        overlay_notes.append(f'基本面intact: {logic_note}' if logic_note else '基本面intact')
        if support_txt:
            overlay_notes.append(f'纪律位: {support_txt} 破位则豁免失效')
        overlay_notes.append('模型SELL降级WATCH：杀估值不杀逻辑')

    # === 规则B：结构性走弱升级 ===
    if sw['structural_weak'] and logic in ('weak', 'broken', 'unknown') and decision in ('reduce', 'watch'):
        decision = 'sell'
        quality_note = 'SELL 结构性走弱(20日无修复+逻辑非intact)'
        overlay_notes.append('不可豁免：无修复日的票没有"恐慌日背景"，是病灶')

    # === 规则C：逻辑破坏加速 ===
    if logic == 'broken' and decision in ('hold', 'hold_buy', 'watch'):
        decision = 'reduce' if decision in ('hold', 'hold_buy') else 'reduce'
        quality_note += ' → 逻辑破坏降级REDUCE'
        overlay_notes.append(f'基本面broken: {logic_note}')

    # === 规则D：逻辑偏弱标注（不改决策，只降置信） ===
    if logic == 'weak' and decision in ('hold', 'hold_buy'):
        overlay_notes.append(f'逻辑偏弱: {logic_note}（建议反弹减1/3）')

    return decision, quality_note, overlay_notes


def format_overlay_summary(overlay_notes: list) -> str:
    if not overlay_notes:
        return ''
    return '  ⚗ ' + ' | '.join(overlay_notes)
