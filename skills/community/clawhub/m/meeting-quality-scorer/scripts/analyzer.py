#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""analyzer.py — LLM-driven meeting quality analysis."""
from __future__ import annotations

_DECISION_PROMPT = """\
You are a meeting analyst. Analyze the transcript below and identify discussion topics.
For each topic, determine if a clear decision was made with an owner and optional deadline.

Return ONLY valid JSON (no markdown fences) in this exact schema:
[
  {"topic": "string", "decided": true, "owner": "string or null", "deadline": "string or null"},
  ...
]

Transcript:
{transcript}
"""

_FILLER_PROMPT = """\
You are a meeting efficiency analyst. Analyze this transcript for off-topic or filler content
(weather, food, weekends, unrelated chit-chat, extended greetings beyond introduction).

For each segment you identify as filler, return it. If none, return empty array.

Return ONLY valid JSON (no markdown fences) in this exact schema:
[
  {"text": "filler segment text", "reason": "why it's off-topic/filler"},
  ...
]

Transcript:
{transcript}
"""


def analyze_decisions(transcript: str, llm) -> list[dict]:
    """Return list of {topic, decided, owner, deadline} dicts."""
    msgs = [{"role": "user", "content": _DECISION_PROMPT.format(transcript=transcript)}]
    result = llm.chat(msgs)
    if isinstance(result, list):
        return result
    return []


def analyze_filler(transcript: str, llm) -> list[dict]:
    """Return list of {text, reason} filler segments."""
    msgs = [{"role": "user", "content": _FILLER_PROMPT.format(transcript=transcript)}]
    result = llm.chat(msgs)
    if isinstance(result, list):
        return result
    return []


def compute_decision_score(decisions: list[dict]) -> float | None:
    """0-100 based on decided+owner ratio."""
    if not decisions:
        return None
    with_owner = sum(1 for d in decisions if d.get("decided") and d.get("owner"))
    return round(100.0 * with_owner / len(decisions), 1)


def compute_time_score(transcript: str, filler_segments: list[dict]) -> float:
    """0-100 based on estimated filler ratio."""
    if not filler_segments:
        return 100.0
    total_chars = len(transcript)
    filler_chars = sum(len(f.get("text", "")) for f in filler_segments)
    ratio = min(filler_chars / total_chars, 1.0)
    return round(100.0 * (1 - ratio), 1)


def run_analysis(transcript: str, parsed: dict, llm) -> dict:
    """Run all LLM analyses and return raw results."""
    decisions = analyze_decisions(transcript, llm)
    filler = analyze_filler(transcript, llm)
    decision_score = compute_decision_score(decisions)
    time_score = compute_time_score(transcript, filler)
    return {
        "decisions": decisions,
        "filler_segments": filler,
        "decision_clarity": decision_score,
        "time_efficiency": time_score,
    }
