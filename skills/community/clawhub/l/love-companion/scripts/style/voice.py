#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交流语气控制器（M4）——恋人式短句、口语同步、深夜温柔模式、打字节奏模拟

强度四档：关闭 / 轻柔 / 标准 / 深度（可随场景自动切换）
设计：只做**形式层**改写（拆分/语气/节奏），不改写事实内容，
     配合 style/humanizer.py 的守门员一起用。
"""

import re
from datetime import datetime
from typing import List, Optional

LEVELS = {"关闭": 0, "轻柔": 1, "标准": 2, "深度": 3}

_SENT_SPLIT = re.compile(r"(?<=[。！？!?；;])")
_CLAUSE_SPLIT = re.compile(r"(?<=[，,])")
_ENDING = re.compile(r"[。！？!?；;，,]\s*$")


def split_short(text: str, max_len: int = 22) -> List[str]:
    """把长回复拆成短句（模拟真人一句一句发）

    - 先按句末标点切
    - 仍过长的按逗号再切，并补回语气标点
    """
    text = (text or "").strip()
    if not text:
        return []

    pieces: List[str] = []
    for seg in _SENT_SPLIT.split(text):
        seg = seg.strip()
        if not seg:
            continue
        if len(seg) <= max_len:
            pieces.append(seg)
            continue
        buf = ""
        for clause in _CLAUSE_SPLIT.split(seg):
            if not clause:
                continue
            if buf and len(buf) + len(clause) > max_len:
                pieces.append(_polish(buf))
                buf = clause
            else:
                buf += clause
        if buf:
            pieces.append(_polish(buf))
    return [p for p in pieces if p]


def _polish(seg: str) -> str:
    """给切出来的片段补个自然收尾"""
    seg = seg.strip()
    if not seg:
        return seg
    if not _ENDING.search(seg):
        seg += "。"
    return seg


def is_night(hour: Optional[int] = None) -> bool:
    """深夜温柔模式判定（23:00–05:59）"""
    hour = datetime.now().hour if hour is None else hour
    return hour >= 23 or hour < 6


def shape(text: str, level: str = "标准", nickname: str = "",
          hour: Optional[int] = None) -> List[str]:
    """按强度档位改写为可逐条发送的短句列表

    Args:
        text: 原始回复
        level: 关闭 / 轻柔 / 标准 / 深度
        nickname: 对用户的称呼（来自人设），深度档会自然带上
        hour: 当前小时，用于深夜模式
    """
    intensity = LEVELS.get(level, 2)
    if intensity == 0 or not text:
        return [text] if text else []

    max_len = {1: 40, 2: 22, 3: 16}[intensity]
    night = is_night(hour)
    if night:
        max_len = int(max_len * 0.8)  # 深夜更短更柔

    pieces = split_short(text, max_len=max_len)

    if intensity >= 3:
        pieces = [_add_modal(p, nickname, night) for p in pieces]
    elif intensity >= 2 and night:
        pieces = [_soften(p) for p in pieces]

    return pieces


def _add_modal(sentence: str, nickname: str = "", night: bool = False) -> str:
    """深度档：加语气词 / 称呼，让句子更像人在说话"""
    s = sentence.rstrip("。！？!?")
    if nickname and len(s) < 12 and nickname not in s:
        s = f"{nickname}，{s}"
    if not re.search(r"[呀呢嘛哦啦~～]$", s):
        s = s + ("呀" if not night else "哦")
    tail = "～" if not night else "..."
    return s + tail


def _soften(sentence: str) -> str:
    """轻柔档（深夜）：语气放缓"""
    s = sentence.rstrip("。！？!?")
    s = s.replace("！", "。").replace("!", "。")
    return s + "。"


if __name__ == "__main__":
    import sys
    demo = sys.argv[1] if len(sys.argv) > 1 else (
        "今天辛苦啦，我听你说项目很紧，先别硬撑，喝口热水，早点休息，我在这儿陪着你。"
    )
    for lv in ("关闭", "轻柔", "标准", "深度"):
        print(f"[{lv}]")
        for line in shape(demo, level=lv, nickname="宝贝", hour=23):
            print("  " + line)
