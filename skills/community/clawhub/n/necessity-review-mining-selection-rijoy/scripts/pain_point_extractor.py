#!/usr/bin/env python3
"""
Bulk reviews → rough pain-point labeler.

Design:
- Single responsibility: normalize text + keyword/rule match + structured output
- Extensible: keyword map loaded from JSON (default: same-dir keywords_en.json)
- Auditable: can export per-review labels for manual review and merge
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence


DEFAULT_KEYWORDS_PATH = Path(__file__).with_name("keywords_en.json")


def normalize_text(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def load_keyword_map(path: Path | None) -> dict[str, list[str]]:
    p = (path or DEFAULT_KEYWORDS_PATH).resolve()
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Keyword map must be JSON object: {label: [keywords...]}")
    keyword_map: dict[str, list[str]] = {}
    for label, keywords in data.items():
        if not isinstance(label, str) or not isinstance(keywords, list):
            raise ValueError("Keyword map: label must be string, keywords must be array")
        keyword_map[label] = [str(k).strip() for k in keywords if str(k).strip()]
    return keyword_map


def iter_reviews_from_path(path: Path, text_column: str | None) -> Iterator[str]:
    path = path.resolve()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return
            col = text_column or reader.fieldnames[0]
            if col not in reader.fieldnames:
                raise ValueError(f"CSV column not found: {col}. Available: {reader.fieldnames}")
            for row in reader:
                t = normalize_text(row.get(col, ""))
                if t:
                    yield t
    else:
        with path.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                t = normalize_text(line)
                if t:
                    yield t


def iter_reviews_from_stdin() -> Iterator[str]:
    for line in sys.stdin:
        t = normalize_text(line)
        if t:
            yield t


def classify_review(review: str, keyword_map: Mapping[str, Sequence[str]]) -> list[str]:
    """
    Return list of matched labels (multi-label).
    Matching is keyword containment; richer semantics belong in human/model layer.
    """
    text = normalize_text(review)
    if not text:
        return []
    labels: list[str] = []
    for label, keywords in keyword_map.items():
        if any(kw and kw in text for kw in keywords):
            labels.append(label)
    return labels


@dataclass(frozen=True)
class AggregatedLabel:
    label: str
    count: int
    examples: list[str]


def aggregate_labels(
    reviews: Iterable[str],
    keyword_map: Mapping[str, Sequence[str]],
    *,
    min_mentions: int = 1,
    max_examples_per_label: int = 5,
) -> dict[str, AggregatedLabel]:
    label_counts: Counter[str] = Counter()
    label_examples: dict[str, list[str]] = defaultdict(list)

    for review in reviews:
        labels = set(classify_review(review, keyword_map))
        for label in labels:
            label_counts[label] += 1
            if len(label_examples[label]) < max_examples_per_label:
                snippet = normalize_text(review)[:120]
                if snippet and snippet not in label_examples[label]:
                    label_examples[label].append(snippet)

    result: dict[str, AggregatedLabel] = {}
    for label, count in label_counts.most_common():
        if count >= min_mentions:
            result[label] = AggregatedLabel(label=label, count=count, examples=label_examples[label])
    return result


def tag_each_review(
    reviews: Iterable[str],
    keyword_map: Mapping[str, Sequence[str]],
) -> Iterator[dict]:
    for review in reviews:
        labels = classify_review(review, keyword_map)
        yield {"review": review, "labels": labels}


def format_table(aggregated: Mapping[str, AggregatedLabel], *, example_cols: int = 2) -> str:
    lines = ["Pain label\tMentions\tExample summary", "-\t-\t-"]
    for label, info in aggregated.items():
        ex = info.examples[:example_cols]
        ex_str = " | ".join(ex) if ex else "-"
        lines.append(f"{label}\t{info.count}\t{ex_str}")
    return "\n".join(lines)


def write_csv_aggregate(path: Path, aggregated: Mapping[str, AggregatedLabel]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["label", "count", "examples"])
        for label, info in aggregated.items():
            w.writerow([label, info.count, " | ".join(info.examples)])


def write_csv_tagged(path: Path, tagged: Iterable[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["review", "labels"])
        for item in tagged:
            w.writerow([item.get("review", ""), ",".join(item.get("labels", []))])


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Rough pain-point classification from review file (CSV/TXT); output stats and examples.")
    p.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=None,
        help="Review file path (.csv or .txt); omit to read from stdin",
    )
    p.add_argument("-c", "--column", type=str, default=None, help="CSV column for review text (CSV only)")
    p.add_argument(
        "-k",
        "--keywords",
        type=Path,
        default=None,
        help="Keyword map JSON path (default: same-dir keywords_en.json)",
    )
    p.add_argument(
        "-f",
        "--format",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format: table / json / csv (csv needs --output)",
    )
    p.add_argument(
        "-m",
        "--min-mentions",
        type=int,
        default=1,
        help="Minimum mentions to include (default 1)",
    )
    p.add_argument(
        "--per-review",
        action="store_true",
        help="Output per-review labels instead of aggregate",
    )
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output file (recommended for json/csv; else stdout)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    try:
        keyword_map = load_keyword_map(args.keywords)
    except Exception as e:
        print(f"Error: keyword map load failed: {e}", file=sys.stderr)
        return 2

    try:
        if args.input is None:
            reviews = list(iter_reviews_from_stdin())
        else:
            reviews = list(iter_reviews_from_path(args.input, args.column))
    except Exception as e:
        print(f"Error: read reviews failed: {e}", file=sys.stderr)
        return 2

    if args.per_review:
        tagged = list(tag_each_review(reviews, keyword_map))
        if args.format == "table":
            preview = tagged[:10]
            text = json.dumps({"preview_top10": preview, "total": len(tagged)}, ensure_ascii=False, indent=2)
            if args.output:
                args.output.write_text(text, encoding="utf-8")
            else:
                print(text)
            return 0

        if args.format == "json":
            text = json.dumps(tagged, ensure_ascii=False, indent=2)
            if args.output:
                args.output.write_text(text, encoding="utf-8")
            else:
                print(text)
            return 0

        if not args.output:
            print("Error: --format csv with --per-review requires --output", file=sys.stderr)
            return 2
        write_csv_tagged(args.output, tagged)
        return 0

    aggregated = aggregate_labels(reviews, keyword_map, min_mentions=args.min_mentions)

    if args.format == "table":
        text = format_table(aggregated)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text)
        return 0

    if args.format == "json":
        payload = {
            "total_reviews": len(reviews),
            "labels": [
                {"label": v.label, "count": v.count, "examples": v.examples}
                for v in aggregated.values()
            ],
        }
        text = json.dumps(payload, ensure_ascii=False, indent=2)
        if args.output:
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text)
        return 0

    if not args.output:
        print("Error: --format csv requires --output", file=sys.stderr)
        return 2
    write_csv_aggregate(args.output, aggregated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
