#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

KEYS = [
    "brand_or_account_type",
    "offer",
    "target_audience",
    "platform",
    "content_goal",
    "tone",
    "source_material"
]

PLATFORM_PATTERNS = {
    "x": r"(?:^|[^a-z])x(?:$|[^a-z])|twitter",
    "linkedin": r"linkedin",
    "instagram": r"instagram",
    "tiktok": r"tiktok",
    "xiaohongshu": r"xiaohongshu|小红书",
    "wechat": r"(?:wechat)(?! official accounts)",
    "wechat official accounts": r"wechat official accounts|微信公众号"
}


def infer_platform(text: str):
    lower = text.lower()
    found = [name for name, pattern in PLATFORM_PATTERNS.items() if re.search(pattern, lower)]
    return found or None


def infer_goal(text: str):
    lower = text.lower()
    mapping = {
        "lead generation": ["lead", "demo", "inquiry", "consult", "signup"],
        "reach": ["reach", "awareness", "exposure"],
        "engagement": ["comment", "reply", "discussion", "engagement"],
        "saveability": ["save", "bookmark", "collect"],
        "conversion": ["buy", "purchase", "convert", "order"]
    }
    for goal, cues in mapping.items():
        if any(c in lower for c in cues):
            return goal
    return None


def build_brief(text: str):
    clean = re.sub(r"\s+", " ", text).strip()
    brief = {
        "brand_or_account_type": None,
        "offer": None,
        "target_audience": None,
        "platform": infer_platform(clean),
        "content_goal": infer_goal(clean),
        "tone": None,
        "source_material": clean,
        "notes": []
    }
    brief["notes"].append("Fill missing fields manually if the source text does not specify them.")
    return brief


def main():
    parser = argparse.ArgumentParser(description="Convert messy free text into a reusable content brief JSON.")
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    text = Path(args.input_file).read_text(encoding="utf-8")
    brief = build_brief(text)
    if args.pretty:
        print(json.dumps(brief, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(brief, ensure_ascii=False))


if __name__ == "__main__":
    main()
