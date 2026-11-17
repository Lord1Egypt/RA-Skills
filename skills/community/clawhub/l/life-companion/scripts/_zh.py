#!/usr/bin/env python3
"""
_zh.py — fold traditional Chinese characters to simplified, one character at a time.

Why this exists: every pattern in selfcheck.py (the honesty gate) and safety_scan.py
(the crisis backstop) is written in simplified characters. Hong Kong, Taiwan and much of
the diaspora write traditional ones, so the same fatalistic sentence was blocked in one
script and waved through in the other, and a traditional-script crisis message raised no
flag at all. Folding the text before matching covers every pattern at once, including
the ones nobody has written yet.

The table is OpenCC's TSCharacters (Apache-2.0, data/zh/). Only the first candidate of
each entry is used, and only entries that map one character to one character, so folded
text keeps its exact length and every match offset lines up with the original. That is
how the gate can quote back the words that were actually written.

Loud on purpose: if the table is missing this raises instead of passing text through,
because a silent pass-through would quietly reopen the hole it exists to close.
"""
import os

TABLE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "data", "zh", "TSCharacters.txt")
_TRANSLATION = None


def _table():
    global _TRANSLATION
    if _TRANSLATION is None:
        if not os.path.exists(TABLE_PATH):
            raise FileNotFoundError(
                f"{TABLE_PATH} is missing, so traditional Chinese cannot be folded and the "
                "honesty gate and crisis scan would miss traditional-script text. The file "
                "ships with the skill in data/zh/; reinstall rather than skipping this.")
        table = {}
        with open(TABLE_PATH, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line or line.startswith("#"):
                    continue
                src, _, targets = line.partition("\t")
                first = targets.split(" ")[0]
                if len(src) == 1 and len(first) == 1 and src != first:
                    table[ord(src)] = ord(first)
        _TRANSLATION = table
    return _TRANSLATION


def to_simplified(text):
    """Traditional → simplified, character for character. The output is exactly as long
    as the input."""
    if not text:
        return ""
    return text.translate(_table())
