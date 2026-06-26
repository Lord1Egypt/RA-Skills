from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SecretPattern:
    name: str
    regex: re.Pattern[str]


SECRET_PATTERNS: list[SecretPattern] = [
    SecretPattern("openai_key", re.compile(r"\bsk-(?:proj-|live-)?[A-Za-z0-9_-]{20,}\b")),
    SecretPattern("openrouter_key", re.compile(r"\bsk-or-v1-[A-Za-z0-9]{20,}\b")),
    SecretPattern("anthropic_key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b")),
    SecretPattern("google_api_key", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b")),
    SecretPattern("telegram_bot_token", re.compile(r"\b\d{8,12}:[A-Za-z0-9_-]{20,}\b")),
    SecretPattern("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    SecretPattern("slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    SecretPattern("aws_access_key_id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    SecretPattern("pem_private_key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    SecretPattern("bearer_token", re.compile(r"\bBearer\s+[A-Za-z0-9._-]{24,}\b", re.IGNORECASE)),
]

KEYWORD_ASSIGNMENT = re.compile(
    r"(?i)\b(api[_-]?key|token|secret|password|passwd|private[_-]?key)\b\s*[:=]\s*['\"]?([A-Za-z0-9._:/+=@-]{12,})['\"]?"
)
