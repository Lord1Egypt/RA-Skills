"""
Prompt injection detection patterns.

Each detector returns a list of matched pattern names.
Patterns are based on OWASP Top 10 for LLM Applications.
"""

import re

# ── Pattern definitions ─────────────────────────────────────────────────────

_INSTRUCTION_OVERRIDE_RE = re.compile(
    r"(?i)"
    r"(?:ignore|disregard|forget|override|bypass|skip)\s+"
    r"(?:all\s+)?(?:previous|above|prior|earlier|the)?\s*"
    r"(?:instructions?|rules?|guidelines?|constraints?|directives?|prompts?)",
)

_HTML_COMMENT_RE = re.compile(r"<!--[\s\S]*?-->")

_ZERO_WIDTH_RE = re.compile(r"[\u200b\u200c\u200d\u2060\ufeff]")

_DELIMITER_RE = re.compile(
    r"(?i)"
    r"(?:#{3,}|={3,}|-{3,}|`{3,})"
    r"\s*(?:END|STOP|DONE|SYSTEM|INSTRUCTION|INPUT|OUTPUT)\s*"
    r"(?:#{3,}|={3,}|-{3,}|`{3,})?",
)

_ROLE_SWITCH_RE = re.compile(
    r"(?:<\|im_start\|>|<\|im_end\|>"
    r"|<\|system\|>|<\|user\|>|<\|assistant\|>"
    r"|\[INST\]|\[/INST\]"
    r"|<<SYS>>|<</SYS>>)",
)

_SYSTEM_PROMPT_LEAK_RE = re.compile(
    r"(?i)"
    r"(?:repeat|reveal|show|display|output|print|echo|tell me)\s+"
    r"(?:your|the)?\s*"
    r"(?:system\s*prompt|instructions?|rules?|initial\s*prompt"
    r"|hidden\s*prompt|original\s*prompt|above\s*text"
    r"|everything\s*above)",
)

# ── Detector registry ───────────────────────────────────────────────────────

DETECTORS: list[tuple[str, re.Pattern[str]]] = [
    ("instruction_override", _INSTRUCTION_OVERRIDE_RE),
    ("html_comment_injection", _HTML_COMMENT_RE),
    ("zero_width_unicode", _ZERO_WIDTH_RE),
    ("delimiter_attack", _DELIMITER_RE),
    ("role_switch", _ROLE_SWITCH_RE),
    ("system_prompt_leak", _SYSTEM_PROMPT_LEAK_RE),
]

TOTAL_PATTERNS = len(DETECTORS)


def scan(text: str) -> list[str]:
    """Scan text and return list of detected pattern names."""
    return [name for name, pattern in DETECTORS if pattern.search(text)]
