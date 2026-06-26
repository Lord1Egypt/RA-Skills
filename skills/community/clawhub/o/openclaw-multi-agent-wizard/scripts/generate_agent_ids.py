#!/usr/bin/env python3
"""Generate safe OpenClaw agent IDs from display names.

Usage:
  python scripts/generate_agent_ids.py "产品助理" "研发助理"
  python scripts/generate_agent_ids.py --existing main,product-assistant "产品助理"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Iterable


PINYIN_FALLBACKS = {
    "产": "chan",
    "品": "pin",
    "助": "zhu",
    "理": "li",
    "研": "yan",
    "发": "fa",
    "运": "yun",
    "营": "ying",
    "生": "sheng",
    "活": "huo",
    "工": "gong",
    "作": "zuo",
}


def slugify(text: str) -> str:
    ascii_parts: list[str] = []
    for char in text.strip().lower():
        if re.match(r"[a-z0-9]", char):
            ascii_parts.append(char)
            continue
        if char in {" ", "-", "_", "/", "."}:
            ascii_parts.append("-")
            continue
        if char in PINYIN_FALLBACKS:
            ascii_parts.append(PINYIN_FALLBACKS[char])
            ascii_parts.append("-")
            continue

    slug = re.sub(r"-{2,}", "-", "".join(ascii_parts)).strip("-")
    return slug or "agent"


def make_unique(base: str, existing: set[str]) -> str:
    candidate = base
    counter = 2
    while candidate in existing:
        candidate = f"{base}-{counter}"
        counter += 1
    existing.add(candidate)
    return candidate


def build_payload(names: Iterable[str], existing: set[str]) -> dict[str, object]:
    items = []
    for name in names:
        base = slugify(name)
        safe_id = make_unique(base, existing)
        items.append(
            {
                "display_name": name,
                "suggested_id": safe_id,
            }
        )
    return {"agents": items}


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser()
    parser.add_argument("names", nargs="+", help="agent display names")
    parser.add_argument(
        "--existing",
        default="",
        help="comma-separated existing agent ids that should not be reused",
    )
    args = parser.parse_args()

    existing = {item.strip() for item in args.existing.split(",") if item.strip()}
    payload = build_payload(args.names, existing)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
