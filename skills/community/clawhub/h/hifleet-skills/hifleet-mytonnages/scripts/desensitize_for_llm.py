#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
供 hifleet-mytonnages Skill 使用：在把邮件主题+正文交给大模型解析前做脱敏。
stdin → stdout；或 -f 读文件写到 stdout。不修改 vessel_sales_purchase 主工程。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_SENS_LINE = "[隐私信息已移除]"


def desensitize_for_llm(text: str) -> str:
    if not text:
        return text

    out_lines: list[str] = []
    for line in text.splitlines():
        l = line.strip()
        drop = False
        if re.match(
            r"(?i)^(From|Sender|Reply-To|Return-Path|Delivered-To|X-Original-From|To|Cc|Bcc)\s*:",
            l,
        ):
            drop = True
        elif re.match(
            r"^(发件人|收件人|抄送|密送|发送时间)\s*[:：]",
            l,
        ):
            drop = True
        elif re.match(r"(?i)^Sent from .+$", l):
            drop = True
        elif re.match(r"^发自\s*\S", l):
            drop = True
        elif re.match(r"^On .+ wrote:\s*$", l):
            drop = True
        elif re.match(r"^在 .+(写入|写道)[:：]\s*$", l):
            drop = True
        out_lines.append(_SENS_LINE if drop else line)
    s = "\n".join(out_lines)

    s = re.sub(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "***@***.***",
        s,
    )
    s = re.sub(r"(?i)mailto:\s*[^\s\]>)]+", "***@***.***", s)

    s = re.sub(r"(?<!\d)1[3-9]\d{9}(?!\d)", "***手机***", s)
    s = re.sub(
        r"(?<!\d)(?:\+?\d{1,3}[-\s])?\d{3,4}[-\s]\d{7,8}(?!\d)|(?<!\d)\d{3,4}[-\s]\d{3,4}[-\s]\d{3,4}(?!\d)",
        "***电话***",
        s,
    )

    s = re.sub(
        r"(?i)(微信|WeChat|WhatsApp)\s*[:：\s]+\s*[\w.@+-]{2,50}",
        "***即时通讯***",
        s,
    )
    s = re.sub(r"(?i)QQ\s*[:：\s]+\s*\d{5,12}\b", "***即时通讯***", s)

    return s


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="邮件文本脱敏后供大模型解析")
    p.add_argument("-f", "--file", help="输入文件（默认读 stdin）")
    args = p.parse_args(argv)
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()
    sys.stdout.write(desensitize_for_llm(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
