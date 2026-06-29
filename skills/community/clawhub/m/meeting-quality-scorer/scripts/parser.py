#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""parser.py — transcript format detection and utterance extraction."""
from __future__ import annotations
import re

MIN_CHARS = 100
LABELED_THRESHOLD = 0.30  # >=30% of non-empty lines must match

_PATTERNS = [
    re.compile(r'^\[?\d+:\d+(:\d+)?\]?\s*(SPEAKER_\d+|Speaker\s+\S+)\s*[:：]'),
    re.compile(r'^[A-Za-z一-鿿][A-Za-z0-9一-鿿\s]{0,15}[:：]\s+\S'),
    re.compile(r'^\[\d{2}:\d{2}:\d{2}\.\d+ --> \d{2}:\d{2}:\d{2}\.\d+\]\s+\S+\s*[:：]'),
]
_WHISPERX = re.compile(r'^\[(\d{2}:\d{2}:\d{2}\.\d+) --> \S+\]\s+(\S+?)\s*[:：]\s*(.*)')
_SPEAKER = re.compile(r'^(?:\[[\d:\.]+\s*-->\s*[\d:\.]+\]\s*)?([A-Za-z一-鿿][A-Za-z0-9一-鿿\s]{0,15})[:：]\s*(.*)')


def detect_format(text: str) -> str:
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return "plain"
    matched = sum(1 for l in lines if any(p.match(l) for p in _PATTERNS))
    return "labeled" if matched / len(lines) >= LABELED_THRESHOLD else "plain"


def parse(text: str) -> dict:
    if len(text.strip()) < MIN_CHARS:
        raise ValueError("transcript too short to score (< 100 chars)")
    fmt = detect_format(text)
    utterances, speakers = [], []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if fmt == "labeled":
            m = _WHISPERX.match(s)
            if m:
                ts, spk, txt = m.group(1), m.group(2), m.group(3).strip()
                if spk not in speakers:
                    speakers.append(spk)
                utterances.append({"speaker": spk, "text": txt, "timestamp": ts})
                continue
            m = _SPEAKER.match(s)
            if m:
                spk, txt = m.group(1).strip(), m.group(2).strip()
                if spk not in speakers:
                    speakers.append(spk)
                utterances.append({"speaker": spk, "text": txt, "timestamp": None})
                continue
        utterances.append({"speaker": None, "text": s, "timestamp": None})
    return {"format": fmt, "utterances": utterances, "speakers": speakers}
