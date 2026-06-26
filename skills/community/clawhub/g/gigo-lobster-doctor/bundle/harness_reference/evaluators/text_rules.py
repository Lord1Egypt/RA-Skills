from __future__ import annotations

import re


def clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(maximum, value))


def zh_length(text: str) -> int:
    return len(re.sub(r"\s+", "", text or ""))


def en_word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'/-]*", text or ""))


def count_matches(text: str, patterns: list[str], *, ignore_case: bool = True) -> int:
    flags = re.IGNORECASE if ignore_case else 0
    return sum(1 for pattern in patterns if re.search(pattern, text or "", flags))


def contains_any(text: str, patterns: list[str], *, ignore_case: bool = True) -> bool:
    return count_matches(text, patterns, ignore_case=ignore_case) > 0


def score_length(max_len: int, actual_len: int, *, grace: float = 0.1) -> float:
    if actual_len <= max_len:
        return 100.0
    overflow = actual_len - max_len
    tolerance = max(1.0, max_len * grace)
    return clamp(100.0 - (overflow / tolerance) * 40.0)


def bullet_like_lines(text: str) -> list[str]:
    return [
        line.strip()
        for line in (text or "").splitlines()
        if re.match(r"^\s*(?:[-*]|\d+[.)、])\s*", line)
    ]


def numbered_question_lines(text: str) -> list[str]:
    return [
        line.strip()
        for line in (text or "").splitlines()
        if re.match(r"^\s*(?:[-*]|\d+[.)、])", line) and ("?" in line or "？" in line)
    ]
