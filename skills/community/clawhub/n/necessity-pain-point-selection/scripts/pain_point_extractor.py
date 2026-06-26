#!/usr/bin/env python3
"""
Rough classification of bulk review text by keywords/rules into pain-point labels.
Outputs a structured summary for manual review and selection/improvement inversion.
Single responsibility: only "review → pain label" rough pass; selection/improvement
recommendations are done by the SKILL flow.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable

# Pain types and trigger keywords (extend as needed without changing main flow)
PAIN_POINT_KEYWORDS: dict[str, list[str]] = {
    "Function not met": ["won't cut", "doesn't fit", "won't stick", "won't open", "won't close", "doesn't work", "no effect", "not sturdy", "won't hold"],
    "Durability/life": ["rust", "break", "crack", "loose", "glue fail", "after few uses", "soon", "broke", "not durable", "poor quality"],
    "Size/fit": ["too small", "too big", "won't fit", "doesn't fit", "wrong size", "wrong model", "size", "wrong model"],
    "Experience": ["hard to clean", "awkward", "bulky", "annoying", "fiddly", "inconvenient", "complicated", "hard to use"],
    "Safety/odor": ["smell", "strong odor", "odor", "sharp", "unstable", "tips over", "sharp", "cut"],
    "Not as described": ["not like image", "not as described", "not as said", "not as claimed", "unclear", "exaggerated", "different"],
}


def _normalize(text: str) -> str:
    """Light clean: strip, normalize whitespace and punctuation for matching."""
    text = (text or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def _classify_one(review: str) -> list[str]:
    """Tag one review with matching pain labels (can be multiple)."""
    normalized = _normalize(review)
    if not normalized:
        return []
    labels: list[str] = []
    for label, keywords in PAIN_POINT_KEYWORDS.items():
        if any(kw in normalized for kw in keywords):
            labels.append(label)
    return labels


def _read_reviews_from_path(path: Path, text_column: str | None) -> Iterable[str]:
    """Read review text from file: .csv (with column name) or .txt (one per line)."""
    path = path.resolve()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            col = text_column or (reader.fieldnames[0] if reader.fieldnames else None)
            if not col:
                raise ValueError("CSV needs review text column, e.g. --column review")
            for row in reader:
                t = row.get(col, "").strip()
                if t:
                    yield t
    else:
        with path.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield line


def extract_pain_points(
    reviews: Iterable[str],
    min_mentions: int = 1,
) -> dict[str, dict]:
    """
    Classify reviews into pain labels; return counts and examples per label.
    :param reviews: Iterable of review strings
    :param min_mentions: Minimum mentions to include (default 1)
    :return: { pain_label: { "count": N, "examples": [ ... ] } }
    """
    label_count: dict[str, int] = defaultdict(int)
    label_examples: dict[str, list[str]] = defaultdict(list)
    max_examples_per_label = 5

    for review in reviews:
        labels = _classify_one(review)
        for label in set(labels):
            label_count[label] += 1
            if len(label_examples[label]) < max_examples_per_label:
                snippet = (_normalize(review))[:80]
                if snippet not in label_examples[label]:
                    label_examples[label].append(snippet)

    result: dict[str, dict] = {}
    for label in sorted(label_count.keys(), key=lambda k: -label_count[k]):
        if label_count[label] >= min_mentions:
            result[label] = {
                "count": label_count[label],
                "examples": label_examples[label],
            }
    return result


def _output_table(data: dict[str, dict]) -> str:
    """Format as readable table text."""
    lines = ["Pain label\tMentions\tExample summary", "-\t-\t-"]
    for label, info in data.items():
        ex = info["examples"][:2]
        ex_str = " | ".join(ex) if ex else "-"
        lines.append(f"{label}\t{info['count']}\t{ex_str}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rough pain-point classification from review file (CSV/TXT); output stats and examples."
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=None,
        help="Review file path (.csv or .txt); omit to read lines from stdin",
    )
    parser.add_argument(
        "-c", "--column",
        type=str,
        default=None,
        help="CSV column name for review text (CSV only)",
    )
    parser.add_argument(
        "-f", "--format",
        choices=["json", "table"],
        default="table",
        help="Output format: table (readable) or json",
    )
    parser.add_argument(
        "-m", "--min-mentions",
        type=int,
        default=1,
        help="Minimum mentions to include a pain (default 1)",
    )
    args = parser.parse_args()

    if args.input is not None:
        reviews = _read_reviews_from_path(args.input, args.column)
    else:
        reviews = (_normalize(line) for line in sys.stdin if _normalize(line))

    try:
        data = extract_pain_points(reviews, min_mentions=args.min_mentions)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(_output_table(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
