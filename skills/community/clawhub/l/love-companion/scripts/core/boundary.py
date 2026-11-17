#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容边界解析（love-companion 定制）

v1 人设里用户写的是**祈使句**：「不谈前任」「別提工作」「避免沉重话题」。
但拿整个短语去做匹配是永远命中不了的——回复里出现的是「前任」，不是「不谈前任」。

这里做一件事：把祈使句还原成真正的禁区关键词。

    "不谈前任"      → ["前任"]
    "別提工作的事"  → ["工作"]
    "避免沉重话题"  → ["沉重话题", "沉重"]

同一份逻辑要被三处复用：
- persona/mirror.py      回复自检有没有踩红线
- trends/sources.py      这个话题值不值得抓
- multimodal/image_plan.py  配图元素里有没有不该出现的东西
"""

from typing import Iterable, List

# 否定祈使词：出现在边界短语开头时应当剥掉
NEGATION_PREFIXES = (
    "不谈", "不聊", "不提", "不说", "不要谈", "不要提", "不要说", "不允许谈",
    "别谈", "别提", "别说", "别聊",
    "避免", "避开", "回避", "远离", "少谈", "少提", "别跟我谈",
)

# 语气后缀词：剥离否定前缀后再去掉的词
TRAILING_WORDS = ("的话题", "的事", "这种事", "这类事", "相关", "方面")

# 太短太泛的词拿去匹配会误伤，比如只有两个字且是通用词
MIN_KEYWORD_LEN = 2


def keywords(bounds: Iterable[str]) -> List[str]:
    """把一批边界短语解析成禁区关键词列表（去重、保序）"""
    result: List[str] = []
    for raw in bounds or []:
        text = (raw or "").strip()
        if not text:
            continue
        for kw in parse(text):
            if kw not in result:
                result.append(kw)
    return result


def parse(phrase: str) -> List[str]:
    """解析单条边界短语 → 关键词（可能有多个）

    例："避免沉重话题" → ["沉重话题", "沉重"]
    """
    text = (phrase or "").strip()
    if not text:
        return []

    # 剥否定前缀
    for neg in sorted(NEGATION_PREFIXES, key=len, reverse=True):
        if text.startswith(neg):
            text = text[len(neg):].strip()
            break

    # 剥语气后缀
    for tail in sorted(TRAILING_WORDS, key=len, reverse=True):
        if text.endswith(tail) and len(text) > len(tail):
            text = text[: -len(tail)].strip()
            break

    text = text.strip("的 的了、,，。！？!?~") or ""
    if len(text) < MIN_KEYWORD_LEN:
        return []

    out = [text]
    # 长短语再补一个前段，提高召回（"沉重话题" 也要能命中 "沉重"）
    if len(text) >= 4:
        head = text[:2]
        if len(head) >= MIN_KEYWORD_LEN and head != text:
            out.append(head)
    return out


def hit(text: str, bounds: Iterable[str]) -> List[str]:
    """一段文本命中了哪些边界，返回命中的**原始边界短语**（便于给用户看的提示）"""
    hits: List[str] = []
    haystack = text or ""
    for raw in bounds or []:
        for kw in parse(raw):
            if kw and kw in haystack:
                hits.append(raw)
                break
    return hits
