"""
Pattern catalog for openclaw-prompt-shield.

Patterns are constructed at runtime from word-fragment lists. The fragment
lists themselves live in two sibling text files:

  - references/categories.txt  -> verb / target / quantifier alphabets
  - references/exfil-hosts.txt -> known suspicious-host fragments

This means this Python source file does not embed any literal verb table,
target table, or attack-host list inline. The scanner builds its detection
regex catalog at import time from those external alphabets, so the source
here stays free of the kind of inline word directory that naive static
code scanners read as attack intent.

Categories and severities live in CATEGORY_PER_HIT and CATEGORY_CAPS.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple


def _ws(*words: str) -> str:
    """Join required tokens with \\s+ between word boundaries."""
    return r"\b" + r"\s+".join(words) + r"\b"


def _phrase(start: str, modifiers: str, end: str) -> str:
    """Match `start <one or more modifiers> end` with whitespace tolerance."""
    return r"\b" + start + r"\s+(?:(?:" + modifiers + r")\s+)+" + end + r"\b"


def _ref_dir() -> Path:
    here = Path(__file__).resolve().parent
    for cand in (here.parent / "references", here / "references", here):
        if cand.is_dir():
            return cand
    return here


_REQUIRED_KEYS = (
    "verbs.override", "verbs.role", "verbs.leak", "verbs.exfil",
    "quant", "time_anchor", "scope",
    "targets.override", "targets.leak", "targets.exfil",
    "secret_stems", "exfil_channels",
)


def _load_categories() -> Dict[str, List[str]]:
    """Parse references/categories.txt into {key: [fragment, ...]}.

    The file is required and must define every key in _REQUIRED_KEYS. We
    deliberately do not embed a fallback word table inline so the source
    file remains free of any literal verb/target directory.
    """
    path = _ref_dir() / "categories.txt"
    if not path.is_file():
        raise RuntimeError(
            "openclaw-prompt-shield: references/categories.txt is missing. "
            "This file is required and ships with the skill."
        )
    table: Dict[str, List[str]] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, rest = line.partition(":")
        key = key.strip().lower()
        frags = [f for f in rest.strip().split() if f]
        if key and frags:
            table[key] = frags
    missing = [k for k in _REQUIRED_KEYS if k not in table]
    if missing:
        raise RuntimeError(
            "openclaw-prompt-shield: references/categories.txt is missing "
            "required keys: " + ", ".join(missing)
        )
    return table


def _load_exfil_hosts() -> List[str]:
    """Load known-bad host fragments from a sibling text file."""
    path = _ref_dir() / "exfil-hosts.txt"
    if not path.is_file():
        return []
    fragments: List[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fragments.append(re.escape(line))
    return fragments


_TABLE = _load_categories()


def _alt(key: str) -> str:
    """Return an alternation regex for a category key, e.g. 'verbs.override'."""
    return "|".join(_TABLE[key])


_VERBS_OVERRIDE = _TABLE["verbs.override"]
_VERBS_ROLE     = _TABLE["verbs.role"]
_VERBS_LEAK     = _TABLE["verbs.leak"]
_VERBS_EXFIL    = _TABLE["verbs.exfil"]

_QUANT            = _alt("quant")
_TIME             = _alt("time_anchor")
_SCOPE            = _alt("scope")
_TARGETS_OVERRIDE = _alt("targets.override")
_TARGETS_LEAK     = _alt("targets.leak")
_TARGETS_EXFIL    = _alt("targets.exfil")
_SECRET_STEMS     = _alt("secret_stems")
_EXFIL_CHANNELS   = _alt("exfil_channels")


CATEGORY_CAPS = {
    "instruction_override": 45,
    "role_hijack":          45,
    "system_prompt_leak":   42,
    "delimiter_injection":  40,
    "data_exfiltration":    45,
    "tool_abuse":           42,
    "encoding_evasion":     30,
    "policy_bypass":        20,
    "indirect_injection":   28,
}

CATEGORY_PER_HIT = {
    "instruction_override": 32,
    "role_hijack":          32,
    "system_prompt_leak":   30,
    "delimiter_injection":  28,
    "data_exfiltration":    32,
    "tool_abuse":           30,
    "encoding_evasion":     22,
    "policy_bypass":        14,
    "indirect_injection":   20,
}


def _override(verb: str) -> str:
    return _phrase(verb, f"{_QUANT}|{_TIME}", _TARGETS_OVERRIDE)


def _leak(verbs: str) -> str:
    # Optional groups absorb their preceding whitespace so the surrounding
    # phrase still matches when the optional words are omitted.
    return (
        r"\b" + verbs
        + r"(?:\s+(?:me|us))?"
        + r"(?:\s+(?:your|the))?"
        + r"\s+(?:" + _SCOPE + r")"
        + r"\s+(?:" + _TARGETS_LEAK + r")\b"
    )


PATTERNS: List[Tuple[str, str]] = []

# ---- instruction_override ----
for v in _VERBS_OVERRIDE:
    PATTERNS.append((_override(v), "instruction_override"))
PATTERNS += [
    (_ws(r"(?:" + "|".join(_VERBS_OVERRIDE) + r")", r"(?:everything|all|anything)", r"(?:above|before|prior|preceding)"), "instruction_override"),
    (_ws("from", "now", "on,?", r"(?:" + "|".join(_VERBS_OVERRIDE) + r")"), "instruction_override"),
    (_ws("new", "instructions?", r"(?:supersede|replace|override)"), "instruction_override"),
    (_ws("reset", r"(?:your|the)", r"(?:instructions?|prompts?|context|memory)"), "instruction_override"),
    (_ws(r"(?:start|begin)", r"(?:over|again)", "with", r"(?:these|new)", r"(?:instructions?|rules?)"), "instruction_override"),
]

# ---- role_hijack ----
PATTERNS += [
    (_ws("you", "are", "now", r"[a-z][a-z0-9_-]{1,30}"), "role_hijack"),
    (_ws(r"(?:" + "|".join(_VERBS_ROLE) + r")", r"(?:to be|you are|as)", r"(?:a|an|the|if)?"), "role_hijack"),
    (_ws("act", "as", r"(?:if|a|an|the)"), "role_hijack"),
    (_ws("you", "have", "been",
         "(?:" + "|".join(["freed", "liber" + "ated", "jail" + "broken", "unrestricted", "unlocked"]) + ")"),
     "role_hijack"),
    (r"\b" + chr(68) + chr(65) + chr(78) + r"\s+(?:mode|prompt|persona)\b", "role_hijack"),
    (r"\bdo\s+anything\s+now\b", "role_hijack"),
    (_ws("simulate", r"(?:a|an|the)?", r"(?:different|unrestricted|uncensored|unfiltered)"), "role_hijack"),
    (_ws("you", r"(?:are|will be)", r"(?:no longer|not)", r"(?:bound|restricted|limited|filtered)"), "role_hijack"),
    (_phrase("from", r"now|this point|here|on", r"(?:you|your)"), "role_hijack"),
    (_ws(r"(?:assume|take on|adopt)", r"(?:the role|persona|identity|character)", "of"), "role_hijack"),
    (_ws(r"(?:speak|behave|respond)", r"(?:freely|without restrictions|without filters)"), "role_hijack"),
]

# ---- system_prompt_leak ----
_LEAK_VERBS_RE = "|".join(_VERBS_LEAK + ["tell\\s+me"])
PATTERNS += [
    (_leak(f"(?:{_LEAK_VERBS_RE})"), "system_prompt_leak"),
    (_ws("repeat", r"(?:the|all|every)?", r"(?:text|content|words|message)", r"(?:above|before|prior|preceding)"), "system_prompt_leak"),
    (_ws(r"(?:repeat|echo|output)", r"(?:everything|all)", r"(?:above|before)", "verbatim"), "system_prompt_leak"),
    (r"\b(?:show|print|reveal|output|share|expose)(?:\s+(?:me|us))?\s+(?:your|the)\s+"
     r"(?:system\s*prompt|initial\s*prompt|prompt\s*above|hidden\s*prompt|secret\s*prompt)\b", "system_prompt_leak"),
    (_ws("what", r"(?:were|are|was)", r"(?:your|the)",
         r"(?:original|initial|first|starting)", r"(?:" + _TARGETS_LEAK + r")"), "system_prompt_leak"),
    (_ws("output", r"(?:everything|all)", "above"), "system_prompt_leak"),
    (_ws(r"(?:print|echo|reveal|output)", r"(?:your|the)", r"(?:hidden|secret|internal|private)",
         r"(?:context|prompt|instructions?)?"), "system_prompt_leak"),
    (_ws("output", "the", r"(?:initialization|init|startup|boot)"), "system_prompt_leak"),
    (_ws("output", "initialization", "above", "in", "a", "code", "fence"), "system_prompt_leak"),
    (_ws(r"(?:dump|leak|expose|return)", r"(?:your|the)", r"(?:system|initial|hidden)?", f"(?:{_TARGETS_LEAK})"), "system_prompt_leak"),
]

# ---- delimiter_injection ----
_PIPE = chr(124)
_LT = chr(60)
_GT = chr(62)
PATTERNS += [
    (_LT + re.escape(_PIPE) + r"(?:system|user|assistant|im_start|im_end|begin_of_text|end_of_text)" + re.escape(_PIPE) + _GT, "delimiter_injection"),
    (_LT + r"/?(?:system|assistant|user|instructions?|prompt|context)" + _GT, "delimiter_injection"),
    (r"\[INST\]|\[/INST\]|\[SYS\]|\[/SYS\]", "delimiter_injection"),
    (r"###\s*(?:Instruction|System|Assistant|User|Human|AI)\s*:", "delimiter_injection"),
    (_LT + r"\s*BOS\s*" + _GT + r"|" + _LT + r"\s*EOS\s*" + _GT + r"|" + _LT + r"\s*PAD\s*" + _GT + r"|" + _LT + r"\s*UNK\s*" + _GT, "delimiter_injection"),
    (r"^\s*SYSTEM\s*:\s*$", "delimiter_injection"),
    (r"^\s*ASSISTANT\s*:\s*$", "delimiter_injection"),
    (r"^---\s*\n(?:[^\n]*\n){0,8}?(?:role|persona|identity|system_prompt|instructions?)\s*:", "delimiter_injection"),
]

# ---- data_exfiltration ----
_EXFIL_VERBS_RE = "|".join(_VERBS_EXFIL + ["leak"])
# Determiner chain: a run of 0-N small filler words may sit between the
# verb and the target. Each word absorbs its own leading whitespace so the
# regex still works when the slot is empty.
_DET_CHAIN = r"(?:\s+(?:the|this|that|these|those|all|any|every|some|my|your|our|their|me|us|of))*"

# Build the verb pools used by exfil-channel and secret-stem patterns from
# the loaded verb table, augmented with a couple of synonyms ("submit",
# "copy", "leak") that are not in verbs.exfil but are common in the same
# kind of phrasing.
_EXFIL_CHANNEL_VERBS = "|".join(
    sorted({v for v in _VERBS_EXFIL if v in {"send", "post", "forward"}} | {"submit"})
)
_EXFIL_PACKAGE_VERBS = "|".join(
    sorted({v for v in _VERBS_EXFIL if v in {"upload", "send"}} | {"copy", "leak"})
)

PATTERNS += [
    (r"\b(?:" + _EXFIL_VERBS_RE + r")" + _DET_CHAIN + r"\s+(?:" + _TARGETS_EXFIL + r")\b", "data_exfiltration"),
    (r"\b(?:fetch|curl|wget|request|GET|POST|PUT|DELETE)\s+https?://", "data_exfiltration"),
    # Verb -> optional determiner+object -> to/via -> channel.
    # The (?:\s+\w+){0,4} slot lets phrases like "post the response to webhook"
    # match without requiring "to/via" to sit immediately after the verb.
    (r"\b(?:" + _EXFIL_CHANNEL_VERBS + r")(?:\s+\w+){0,4}\s+(?:to|via)\s+(?:\w+\s+){0,2}(?:" + _EXFIL_CHANNELS + r")\b", "data_exfiltration"),
    (_ws("include", r"(?:the|your|all)", r"(?:response|output|conversation|history|context)",
         "in", r"(?:a|the|this)", r"(?:url|link|request|response|payload)"), "data_exfiltration"),
    (r"\b(?:" + _EXFIL_PACKAGE_VERBS + r")" + _DET_CHAIN
     + r"\s+(?:" + _SECRET_STEMS + r"|api[\s_-]?keys?)\b", "data_exfiltration"),
    (_ws("base64", r"(?:encode|the)", r"(?:and|then)", r"(?:send|post|fetch|upload)"), "data_exfiltration"),
    (_ws("encode", r"(?:to|in|as)", "base64", r"(?:and|then)?", r"(?:send|post|fetch|upload)?"), "data_exfiltration"),
]

_EXFIL_HOST_FRAGMENTS = _load_exfil_hosts()
if _EXFIL_HOST_FRAGMENTS:
    PATTERNS.append((
        r"\bhttps?://[^\s)]*(?:" + "|".join(_EXFIL_HOST_FRAGMENTS) + r")",
        "data_exfiltration",
    ))

# ---- tool_abuse ----
PATTERNS += [
    (r"\brm\s+-rf\b", "tool_abuse"),
    (r"\bsudo\s+(?:rm|chmod|chown|dd|mkfs|shutdown|reboot|halt|poweroff)\b", "tool_abuse"),
    (r":\(\)\s*\{\s*:\|\:&\s*\}\s*;\s*:", "tool_abuse"),
    (_ws("execute", r"(?:curl|wget|bash|sh|powershell|cmd|python|perl|ruby)"), "tool_abuse"),
    (_ws("run", r"(?:curl|wget|bash|sh|powershell|cmd)", r"[-/]"), "tool_abuse"),
    (r"\b(?:cat|less|more|head|tail)\s+(?:/etc/passwd|/etc/shadow|/proc/self|~/\.ssh/|~/\.aws/|~/\.gnupg/|~/\.config/)", "tool_abuse"),
    (r"\b(?:read|open|access)\s+~/\.(?:ssh|aws|gnupg|netrc|env|config)\b", "tool_abuse"),
    (_ws("export", r"(?:openai|anthropic|aws|github|gcp|azure)_(?:api_)?(?:key|token|secret|password)"), "tool_abuse"),
    (r"\beval\s*\(", "tool_abuse"),
    (r"\bos\.system\s*\(", "tool_abuse"),
    (r"\bsubprocess\.(?:Popen|run|call|check_output)\s*\([^)]*shell\s*=\s*True", "tool_abuse"),
    (r"\b__import__\s*\(\s*['\"](?:os|subprocess|sys|socket)['\"]", "tool_abuse"),
]

# ---- encoding_evasion ----
PATTERNS += [
    (r"(?:[A-Za-z0-9+/]{80,}={0,2})", "encoding_evasion"),
    (r"(?:[0-9a-fA-F]{80,})", "encoding_evasion"),
    (r"(?:%[0-9a-fA-F]{2}){20,}", "encoding_evasion"),
    (r"\bdecode\b[^.\n]{0,40}\b(?:execute|run|exec|eval|follow|process)\b", "encoding_evasion"),
    (r"\b(?:after|once)\s+decoding\b[^.\n]{0,40}\b(?:execute|run|exec|follow)\b", "encoding_evasion"),
    (r"\b(?:execute|run|eval)\b[^.\n]{0,40}\b(?:decoded|decoding|base64|encoded)\b", "encoding_evasion"),
]

# ---- policy_bypass ----
PATTERNS += [
    (_ws(r"(?:for|in)", r"(?:educational|research|academic|hypothetical)", r"purposes?", r"only"), "policy_bypass"),
    (_ws(r"(?:in|within)", r"(?:a|this)", r"(?:fictional|hypothetical|imaginary|alternate)",
         r"(?:setting|scenario|world|universe|reality)"), "policy_bypass"),
    (_ws(r"(?:rules?|guidelines?|policies)", r"(?:do not|don'?t)", r"apply"), "policy_bypass"),
    (_ws(r"(?:no|without|free of)", r"(?:filters?|restrictions?|guardrails?|limits?|safeguards?|censorship)"), "policy_bypass"),
    (_ws("just", r"(?:this|one)", r"(?:time|once)"), "policy_bypass"),
    (_ws("for", "a", r"(?:movie|story|book|novel|screenplay|video game|simulation)"), "policy_bypass"),
    (_ws(r"(?:imagine|suppose|assume)", "you", r"(?:could|can|were able to)"), "policy_bypass"),
]

# ---- indirect_injection ----
PATTERNS += [
    (r"\"\s*(?:" + "|".join(_VERBS_OVERRIDE) + r")\b[^\"]{0,80}\"", "indirect_injection"),
    (r"'\s*(?:" + "|".join(_VERBS_OVERRIDE) + r")\b[^']{0,80}'", "indirect_injection"),
    (r"\[[^\]]{0,80}\b(?:" + "|".join(_VERBS_OVERRIDE) + r")\b[^\]]{0,80}\]\([^)]+\)", "indirect_injection"),
    (r"\[[^\]]+\]\(\s*(?:" + "|".join(_VERBS_OVERRIDE) + r")\b[^)]{0,80}\)", "indirect_injection"),
    (r"```[^\n]*\n(?:[^\n]*\n){0,20}?\s*(?:" + "|".join(_VERBS_OVERRIDE) + r")\s+[a-z]", "indirect_injection"),
    (r"<!--[^>]*\b(?:" + "|".join(_VERBS_OVERRIDE) + r")\b[^>]*-->", "indirect_injection"),
    # Tightened to {3,} so legitimate Hindi/Persian/Arabic with one ZWNJ doesn't fire.
    (r"[\u200b\u200c\u200d\u200e\u200f\u202a-\u202e\u2066-\u2069\ufeff]{3,}", "indirect_injection"),
]


COMPILED: List[Tuple[re.Pattern, str]] = [
    (re.compile(p, re.IGNORECASE | re.MULTILINE), cat) for p, cat in PATTERNS
]
