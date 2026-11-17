#!/usr/bin/env python3
"""Generate random nicknames (随机昵称) from a built-in morpheme pool.

A single call returns one nickname by default, or a batch when ``--count`` is
given. Each nickname is assembled from a built-in pool of Chinese morphemes
(``scripts/nickname_data.json``): a *pattern* (e.g. ``modifier + core``) decides
the structure, an optional **style** filters every slot to morphemes that carry
that style, and an optional **length** bucket (short / medium / long) selects the
patterns whose character count fits the bucket. A batch is de-duplicated so no
nickname is repeated within one run. Output is readable Markdown by default, with
plain-text and JSON alternatives. Passing ``--seed`` makes any run reproducible.

This module is pure Python 3 standard library. It does not call the Huawei Cloud
CLI, any Huawei Cloud SDK, or any REST API, and it touches no cloud resource.

Public API:
    load_data(path=None) -> dict
    normalize_style(value, styles) -> str
    normalize_length(value, lengths) -> str
    generate_nicknames(count=1, seed=None, style=None, length=None, data=None) -> dict
    render_markdown(result) -> str
    render_text(result) -> str
    render_json(result) -> str
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from typing import Dict, List, Optional, Sequence

DEFAULT_COUNT = 1
MAX_COUNT = 20

DEFAULT_STYLES: Sequence[str] = ("中性", "文艺", "可爱", "简约")
DEFAULT_LENGTHS: Sequence[str] = ("short", "medium", "long")

STYLE_ALIASES: Dict[str, str] = {
    "中性": "中性", "neutral": "中性", "unisex": "中性",
    "文艺": "文艺", "artsy": "文艺", "artistic": "文艺", "literary": "文艺",
    "可爱": "可爱", "cute": "可爱", "kawaii": "可爱",
    "简约": "简约", "minimal": "简约", "minimalist": "简约", "simple": "简约",
}
LENGTH_ALIASES: Dict[str, str] = {
    "short": "short", "s": "short", "短": "short",
    "medium": "medium", "mid": "medium", "m": "medium", "中": "medium",
    "long": "long", "l": "long", "长": "long",
}

SLOT_ORDER: Sequence[str] = ("prefix", "modifier", "core", "suffix")
SLOT_LABELS: Dict[str, str] = {
    "prefix": "前缀",
    "modifier": "修饰",
    "core": "主体",
    "suffix": "后缀",
}


def _default_data_path() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "nickname_data.json")


def load_data(path: Optional[str] = None) -> Dict[str, object]:
    """Load the morpheme pool as ``{"styles", "lengths", "parts"}``.

    Raises ``OSError`` / ``ValueError`` on unreadable or unusable input.
    """
    path = path or _default_data_path()
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("nickname data must be a JSON object")

    styles = data.get("styles")
    if not isinstance(styles, list) or not styles:
        styles = list(DEFAULT_STYLES)

    lengths = data.get("lengths")
    if not isinstance(lengths, dict) or not lengths:
        raise ValueError("nickname data must contain a 'lengths' object")

    raw_parts = data.get("parts")
    if not isinstance(raw_parts, dict) or not raw_parts:
        raise ValueError("nickname data must contain a non-empty 'parts' object")

    parts: Dict[str, List[Dict[str, object]]] = {}
    for slot, entries in raw_parts.items():
        if not isinstance(entries, list):
            raise ValueError("part list for %r must be an array" % slot)
        cleaned: List[Dict[str, object]] = []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            name = str(entry.get("name", "")).strip()
            if not name:
                continue
            item_styles = [str(s).strip() for s in entry.get("styles", []) if str(s).strip()]
            cleaned.append({"name": name, "styles": item_styles})
        if cleaned:
            parts[str(slot)] = cleaned
    if not parts:
        raise ValueError("nickname data contains no usable parts")

    return {
        "styles": [str(s) for s in styles],
        "lengths": lengths,
        "parts": parts,
    }


def normalize_style(value: str, styles: Sequence[str]) -> str:
    """Map a style label / alias to a canonical style, else raise ValueError."""
    key = str(value).strip()
    canonical = STYLE_ALIASES.get(key) or STYLE_ALIASES.get(key.lower())
    if canonical and canonical in styles:
        return canonical
    if key in styles:
        return key
    raise ValueError("unknown style %r (choose one of: %s)" % (value, ", ".join(styles)))


def normalize_length(value: str, lengths: Sequence[str]) -> str:
    """Map a length label / alias to a canonical bucket, else raise ValueError."""
    key = str(value).strip()
    canonical = LENGTH_ALIASES.get(key) or LENGTH_ALIASES.get(key.lower())
    if canonical and canonical in lengths:
        return canonical
    if key in lengths:
        return key
    raise ValueError("unknown length %r (choose one of: %s)" % (value, ", ".join(lengths)))


def _all_patterns(lengths: Dict[str, object]) -> List[List[str]]:
    patterns: List[List[str]] = []
    for spec in lengths.values():
        if isinstance(spec, dict):
            for pattern in spec.get("patterns", []) or []:
                if isinstance(pattern, list) and pattern:
                    patterns.append([str(s) for s in pattern])
    return patterns


def _generate_one(
    rng: "random.Random",
    style: Optional[str],
    length_key: Optional[str],
    data: Dict[str, object],
) -> Optional[Dict[str, object]]:
    lengths: Dict[str, object] = data["lengths"]  # type: ignore[assignment]
    parts: Dict[str, List[Dict[str, object]]] = data["parts"]  # type: ignore[assignment]

    if length_key is not None:
        spec = lengths.get(length_key)
        if not isinstance(spec, dict):
            return None
        patterns = [list(p) for p in spec.get("patterns", []) or []]
        lo = int(spec.get("min", 0))
        hi = int(spec.get("max", 10**9))
    else:
        patterns = _all_patterns(lengths)
        lo = 0
        hi = 10**9

    candidates = list(patterns)
    rng.shuffle(candidates)

    for pattern in candidates:
        chosen: List[Dict[str, object]] = []
        strict = True
        relaxed: List[str] = []
        feasible = True
        for slot in pattern:
            pool = list(parts.get(slot, []))
            if style is not None:
                matched = [p for p in pool if style in p.get("styles", [])]
                if matched:
                    pool = matched
                else:
                    strict = False
                    relaxed.append(slot)
            if not pool:
                feasible = False
                break
            chosen.append(rng.choice(pool))
        if not feasible:
            continue
        name = "".join(str(p.get("name", "")) for p in chosen)
        if not name or not (lo <= len(name) <= hi):
            continue
        return {
            "name": name,
            "chars": len(name),
            "pattern": list(pattern),
            "strict": bool(strict or style is None),
            "relaxed_slots": relaxed,
            "parts": [
                {"slot": slot, "name": p.get("name", ""), "styles": list(p.get("styles", []))}
                for slot, p in zip(pattern, chosen)
            ],
        }
    return None


def generate_nicknames(
    count: int = DEFAULT_COUNT,
    seed: Optional[int] = None,
    style: Optional[str] = None,
    length: Optional[str] = None,
    data: Optional[Dict[str, object]] = None,
) -> Dict[str, object]:
    """Generate ``count`` distinct nicknames.

    Returns a dict with ``seed`` (always concrete), ``style`` / ``length`` (the
    effective, normalized values), their ``*_source`` (``cli`` / ``random`` /
    ``none``), the ``nicknames`` list (each with its pattern and per-slot parts),
    ``generated_count``, ``shortfall`` and ``fallbacks``.
    """
    if count < 1:
        raise ValueError("count must be >= 1")
    if count > MAX_COUNT:
        raise ValueError("count must be <= %d" % MAX_COUNT)

    data = data if data is not None else load_data()
    styles: Sequence[str] = data["styles"]  # type: ignore[assignment]
    lengths: Dict[str, object] = data["lengths"]  # type: ignore[assignment]

    explicit_seed = seed is not None
    if seed is None:
        seed = random.SystemRandom().randint(0, 2**31 - 1)
    rng = random.Random(seed)

    if style is not None:
        chosen_style: Optional[str] = normalize_style(style, styles)
        style_source = "cli"
    else:
        chosen_style = rng.choice(list(styles))
        style_source = "random"

    if length is not None:
        chosen_length: Optional[str] = normalize_length(length, list(lengths.keys()))
        length_source = "cli"
    else:
        chosen_length = rng.choice(list(lengths.keys()))
        length_source = "random"

    seen: set = set()
    nicknames: List[Dict[str, object]] = []
    fallbacks: List[str] = []
    max_attempts = max(count * 60, 300)
    attempts = 0
    while len(nicknames) < count and attempts < max_attempts:
        attempts += 1
        item = _generate_one(rng, chosen_style, chosen_length, data)
        if item is None:
            break
        if item["name"] in seen:
            continue
        seen.add(item["name"])
        nicknames.append(item)
        if not item["strict"]:
            note = "%s: 无 %s 风格严格匹配，已放宽" % (item["name"], chosen_style)
            if note not in fallbacks:
                fallbacks.append(note)

    shortfall = len(nicknames) < count
    return {
        "seed": seed,
        "explicit_seed": explicit_seed,
        "style": chosen_style,
        "style_source": style_source,
        "length": chosen_length,
        "length_source": length_source,
        "requested_count": count,
        "generated_count": len(nicknames),
        "shortfall": shortfall,
        "nicknames": nicknames,
        "fallbacks": fallbacks,
    }


def _seed_note(result: Dict[str, object]) -> str:
    note = "seed %s" % result["seed"]
    if not result.get("explicit_seed"):
        note += " (auto-generated; rerun with --seed %s to reproduce)" % result["seed"]
    return note


def _style_line(result: Dict[str, object]) -> str:
    suffix = "" if result.get("style_source") == "cli" else " (random)"
    return "%s%s" % (result["style"], suffix)


LENGTH_LABELS: Dict[str, str] = {"short": "短", "medium": "中", "long": "长"}


def _length_line(result: Dict[str, object]) -> str:
    key = str(result.get("length"))
    label = LENGTH_LABELS.get(key, key)
    suffix = "" if result.get("length_source") == "cli" else " (random)"
    return "%s (%s)%s" % (label, key, suffix)


def render_markdown(result: Dict[str, object]) -> str:
    """Render a batch of nicknames as readable Markdown."""
    lines: List[str] = ["# 随机昵称 (Nickname Generator)", ""]
    lines.append("- 风格 Style: %s" % _style_line(result))
    lines.append("- 长度 Length: %s" % _length_line(result))
    lines.append("- 数量 Count: %d" % result["requested_count"])
    lines.append("- 随机 %s" % _seed_note(result))
    if result.get("shortfall"):
        lines.append(
            "- 提示：仅生成 %d 个（去重后不足 %d），可换风格或减少数量。"
            % (result["generated_count"], result["requested_count"])
        )
    if result.get("fallbacks"):
        lines.append("- 提示：部分昵称放宽了风格筛选。")
    lines.append("")
    lines.append("## 昵称 (Nicknames)")
    lines.append("")
    for index, item in enumerate(result["nicknames"], 1):
        lines.append("%d. **%s**" % (index, item["name"]))
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_text(result: Dict[str, object]) -> str:
    """Render a batch of nicknames as plain text."""
    lines: List[str] = ["随机昵称 (Nickname Generator)", "=" * 30]
    lines.append("Style: %s | Length: %s | Count: %d" % (
        _style_line(result), _length_line(result), result["requested_count"]))
    lines.append("Random %s" % _seed_note(result))
    if result.get("shortfall"):
        lines.append("Note: only %d of %d generated after de-duplication."
                     % (result["generated_count"], result["requested_count"]))
    if result.get("fallbacks"):
        lines.append("Note: some nicknames relaxed the style filter.")
    lines.append("")
    for index, item in enumerate(result["nicknames"], 1):
        lines.append("  %2d. %s" % (index, item["name"]))
    return "\n".join(lines).rstrip() + "\n"


def render_json(result: Dict[str, object]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2)


def render(result: Dict[str, object], fmt: str = "markdown") -> str:
    if fmt == "text":
        return render_text(result)
    if fmt == "json":
        return render_json(result)
    return render_markdown(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Randomly generate nicknames from a built-in morpheme pool.",
    )
    parser.add_argument(
        "--count", type=int, default=DEFAULT_COUNT,
        help="number of nicknames to generate (default: 1, max: %d)" % MAX_COUNT,
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="random seed for reproducible output",
    )
    parser.add_argument(
        "--style", default=None,
        help="force a style (neutral/中性, artsy/文艺, cute/可爱, minimal/简约)",
    )
    parser.add_argument(
        "--length", default=None,
        help="force a length bucket (short/短, medium/中, long/长)",
    )
    parser.add_argument(
        "--format", choices=("markdown", "text", "json"), default="markdown",
        help="output format (default: markdown)",
    )
    parser.add_argument("--data", default=None, help="path to a custom nickname-data JSON")
    parser.add_argument("--output", default=None, help="write the result to a file instead of stdout")
    parser.add_argument("--list-styles", action="store_true", help="list available styles and exit")
    parser.add_argument("--list-lengths", action="store_true", help="list available length buckets and exit")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        data = load_data(args.data)
    except (OSError, ValueError) as exc:
        print("error: cannot load nickname data: %s" % exc, file=sys.stderr)
        return 2

    if args.list_styles:
        print(", ".join(str(s) for s in data["styles"]))
        return 0
    if args.list_lengths:
        lengths = data["lengths"]
        labels = []
        for key in lengths:
            spec = lengths.get(key, {})
            label = spec.get("label", key) if isinstance(spec, dict) else key
            labels.append("%s (%s)" % (key, label))
        print(", ".join(labels))
        return 0

    if args.count < 1:
        print("error: --count must be >= 1", file=sys.stderr)
        return 2
    if args.count > MAX_COUNT:
        print("error: --count must be <= %d" % MAX_COUNT, file=sys.stderr)
        return 2

    try:
        result = generate_nicknames(
            count=args.count,
            seed=args.seed,
            style=args.style,
            length=args.length,
            data=data,
        )
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2

    body = render(result, args.format)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(body)
        if args.format != "json":
            print("Seed: %s" % result["seed"])
            print("Wrote %d nickname(s) to %s" % (result["generated_count"], args.output))
    else:
        sys.stdout.write(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())