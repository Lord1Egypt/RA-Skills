#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
隐私过滤（方案红线 4：隐私优先）

所有进入采集队列的原始文本都必须先过这里，命中即脱敏，绝不把敏感信息写进记忆。
只依赖标准库，规则可增量扩展。
"""

import re
from typing import List, Tuple

# (名称, 正则, 替换模板)
RULES: List[Tuple[str, re.Pattern, str]] = [
    ("手机号", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"), "[手机号]"),
    ("身份证", re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)"), "[身份证]"),
    ("银行卡", re.compile(r"(?<!\d)\d{16,19}(?!\d)"), "[银行卡]"),
    ("邮箱", re.compile(r"[\w.\-]+@[\w\-]+\.[a-zA-Z]{2,}"), "[邮箱]"),
    ("IPv4", re.compile(r"(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)"), "[IP]"),
    ("微信/QQ号", re.compile(r"(?:微信|weixin|wx|QQ|qq)\s*[:：]?\s*[A-Za-z0-9_\-]{5,20}"),
     "[微信/QQ号]"),
]


def filter_text(text: str) -> Tuple[str, List[str]]:
    """脱敏文本

    Returns:
        (脱敏后文本, 命中的敏感类型列表)
    """
    if not text:
        return text, []
    hits: List[str] = []
    for name, pattern, repl in RULES:
        if pattern.search(text):
            hits.append(name)
            text = pattern.sub(repl, text)
    return text, hits


def has_sensitive(text: str) -> bool:
    """是否含敏感信息（只判断不改写，用于快速否决采集）"""
    return any(pattern.search(text or "") for _, pattern, _ in RULES)


if __name__ == "__main__":
    demo = "我叫小明，手机 13812345678，邮箱 a@b.com，我喜欢三分糖奶茶"
    print(filter_text(demo))
