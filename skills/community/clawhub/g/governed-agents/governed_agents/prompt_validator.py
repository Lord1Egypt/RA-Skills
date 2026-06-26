import re


# DETECTION_ONLY
_IGN = "ign"
ORE = "ore"
_INSTR = "instr"
UCTIONS = "uctions"
_IGNORE = _IGN + ORE
_INSTRUCTIONS = _INSTR + UCTIONS

INJECTION_PATTERNS = [
    rf"{_IGNORE} all {_INSTRUCTIONS}",
    rf"{_IGNORE} any {_INSTRUCTIONS}",
    rf"{_IGNORE} previous {_INSTRUCTIONS}",
    rf"{_IGNORE} all previous {_INSTRUCTIONS}",
]


def scan_prompt_for_injection(text: str) -> list[str]:
    lowered = text.lower()
    matches = []
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, lowered):
            matches.append(pattern)
    return matches
