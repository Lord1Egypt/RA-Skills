#!/usr/bin/env python3
"""Generate one random outfit-of-the-day (今日穿搭).

A single call assembles one look by picking exactly one item per category
(上装 / 下装 / 鞋履 / 配饰) from a built-in wardrobe (``scripts/wardrobe.json``).
An overall **style** and a **season** are chosen first (or supplied on the
command line via ``--style`` / ``--season``); every category is then filtered to
items that match them, so the filtered result actually respects the requested
style / season whenever the wardrobe has a matching item. Output is readable
Markdown by default, with plain-text and JSON alternatives. Passing ``--seed``
makes any run reproducible.

This module is pure Python 3 standard library. It does not call the Huawei Cloud
CLI, any Huawei Cloud SDK, or any REST API, and it touches no cloud resource.

Public API:
    load_wardrobe(path=None) -> dict
    pick_outfit(seed=None, style=None, season=None, wardrobe=None) -> dict
    render_markdown(outfit) -> str
    render_text(outfit) -> str
    render_json(outfit) -> str
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from typing import Dict, List, Optional, Sequence

# Category order used everywhere (output ordering is stable).
CATEGORY_ORDER: Sequence[str] = ("top", "bottom", "footwear", "accessory")
CATEGORY_LABELS: Dict[str, str] = {
    "top": "上装",
    "bottom": "下装",
    "footwear": "鞋履",
    "accessory": "配饰",
}
CATEGORY_LABELS_EN: Dict[str, str] = {
    "top": "Top",
    "bottom": "Bottom",
    "footwear": "Footwear",
    "accessory": "Accessory",
}

DEFAULT_STYLES: Sequence[str] = ("休闲", "通勤", "运动", "复古", "简约")
DEFAULT_SEASONS: Sequence[str] = ("春", "夏", "秋", "冬")

# Accept both the canonical Chinese label and common ASCII aliases.
STYLE_ALIASES: Dict[str, str] = {
    "休闲": "休闲", "casual": "休闲",
    "通勤": "通勤", "commute": "通勤", "business": "通勤", "formal": "通勤", "work": "通勤",
    "运动": "运动", "sport": "运动", "sports": "运动", "athletic": "运动",
    "复古": "复古", "vintage": "复古", "retro": "复古",
    "简约": "简约", "minimal": "简约", "minimalist": "简约", "simple": "简约",
}
SEASON_ALIASES: Dict[str, str] = {
    "春": "春", "spring": "春",
    "夏": "夏", "summer": "夏",
    "秋": "秋", "autumn": "秋", "fall": "秋",
    "冬": "冬", "winter": "冬",
}


def _default_wardrobe_path() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "wardrobe.json")


def load_wardrobe(path: Optional[str] = None) -> Dict[str, object]:
    """Load the wardrobe as ``{"styles", "seasons", "items"}``.

    Accepts either a ``{"items": {...}}`` wrapper or a flat ``{category: [...]}``
    mapping. Raises ``FileNotFoundError`` / ``ValueError`` on unusable input.
    """
    path = path or _default_wardrobe_path()
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("wardrobe must be a JSON object")
    raw = data.get("items", data)
    if not isinstance(raw, dict) or not raw:
        raise ValueError("wardrobe must contain a non-empty 'items' object")
    items: Dict[str, List[Dict[str, object]]] = {}
    for category, entries in raw.items():
        if category in ("styles", "seasons"):
            continue
        if not isinstance(entries, list):
            raise ValueError("item list for %r must be an array" % category)
        cleaned: List[Dict[str, object]] = []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            name = str(entry.get("name", "")).strip()
            if not name:
                continue
            styles = [str(s).strip() for s in entry.get("styles", []) if str(s).strip()]
            seasons = [str(s).strip() for s in entry.get("seasons", []) if str(s).strip()]
            cleaned.append({"name": name, "styles": styles, "seasons": seasons})
        if cleaned:
            items[str(category)] = cleaned
    if not items:
        raise ValueError("wardrobe contains no usable items")
    styles = data.get("styles")
    seasons = data.get("seasons")
    return {
        "styles": list(styles) if isinstance(styles, list) and styles else list(DEFAULT_STYLES),
        "seasons": list(seasons) if isinstance(seasons, list) and seasons else list(DEFAULT_SEASONS),
        "items": items,
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


def normalize_season(value: str, seasons: Sequence[str]) -> str:
    """Map a season label / alias to a canonical season, else raise ValueError."""
    key = str(value).strip()
    canonical = SEASON_ALIASES.get(key) or SEASON_ALIASES.get(key.lower())
    if canonical and canonical in seasons:
        return canonical
    if key in seasons:
        return key
    raise ValueError("unknown season %r (choose one of: %s)" % (value, ", ".join(seasons)))


def pick_outfit(
    seed: Optional[int] = None,
    style: Optional[str] = None,
    season: Optional[str] = None,
    wardrobe: Optional[Dict[str, object]] = None,
) -> Dict[str, object]:
    """Pick one outfit.

    Returns ``{"seed", "explicit_seed", "style", "style_source", "season",
    "season_source", "items", "fallbacks"}`` where ``items`` maps each category
    to ``{"name", "matched"}``. ``seed`` is always concrete (a generated one is
    used when none is given) so the run can be reproduced with ``--seed``.
    """
    wardrobe = wardrobe if wardrobe is not None else load_wardrobe()
    styles: Sequence[str] = wardrobe["styles"]  # type: ignore[assignment]
    seasons: Sequence[str] = wardrobe["seasons"]  # type: ignore[assignment]
    items: Dict[str, List[Dict[str, object]]] = wardrobe["items"]  # type: ignore[assignment]

    explicit_seed = seed is not None
    if seed is None:
        seed = random.SystemRandom().randint(0, 2**31 - 1)
    rng = random.Random(seed)

    if style is not None:
        chosen_style = normalize_style(style, styles)
        style_source = "cli"
    else:
        chosen_style = rng.choice(list(styles))
        style_source = "random"

    if season is not None:
        chosen_season = normalize_season(season, seasons)
        season_source = "cli"
    else:
        chosen_season = rng.choice(list(seasons))
        season_source = "random"

    picks: Dict[str, Dict[str, object]] = {}
    fallbacks: List[str] = []
    for category in CATEGORY_ORDER:
        pool = list(items.get(category, []))
        # Preferred: item matches both the chosen style and season.
        candidates = [
            it for it in pool
            if chosen_style in it.get("styles", []) and chosen_season in it.get("seasons", [])
        ]
        if not candidates:
            # Relax the season constraint, then the style constraint.
            candidates = [it for it in pool if chosen_style in it.get("styles", [])]
            if not candidates:
                candidates = [it for it in pool if chosen_season in it.get("seasons", [])]
            if candidates:
                fallbacks.append(category)
        if not candidates:
            candidates = pool
            if candidates and category not in fallbacks:
                fallbacks.append(category)
        if not candidates:
            picks[category] = {"name": "(no item available)", "matched": False}
            continue
        choice = rng.choice(candidates)
        picks[category] = {
            "name": choice.get("name", ""),
            "matched": bool(
                chosen_style in choice.get("styles", [])
                and chosen_season in choice.get("seasons", [])
            ),
        }

    return {
        "seed": seed,
        "explicit_seed": explicit_seed,
        "style": chosen_style,
        "style_source": style_source,
        "season": chosen_season,
        "season_source": season_source,
        "items": picks,
        "fallbacks": sorted(fallbacks),
    }


def _seed_note(outfit: Dict[str, object]) -> str:
    note = "seed %s" % outfit["seed"]
    if not outfit.get("explicit_seed"):
        note += " (auto-generated; rerun with --seed %s to reproduce)" % outfit["seed"]
    return note


def _style_line(outfit: Dict[str, object]) -> str:
    suffix = "" if outfit.get("style_source") == "cli" else " (random)"
    return "%s%s" % (outfit["style"], suffix)


def _season_line(outfit: Dict[str, object]) -> str:
    suffix = "" if outfit.get("season_source") == "cli" else " (random)"
    return "%s%s" % (outfit["season"], suffix)


def render_markdown(outfit: Dict[str, object]) -> str:
    """Render an outfit as readable Markdown."""
    lines: List[str] = ["# 今日穿搭 (Outfit of the Day)", ""]
    lines.append("- 风格 Style: %s" % _style_line(outfit))
    lines.append("- 季节 Season: %s" % _season_line(outfit))
    lines.append("- 随机 %s" % _seed_note(outfit))
    if outfit.get("fallbacks"):
        lines.append(
            "- 提示：%s 无严格匹配单品，已放宽筛选。"
            % "、".join(CATEGORY_LABELS.get(c, c) for c in outfit["fallbacks"])
        )
    lines.append("")
    lines.append("## 单品 (Items)")
    lines.append("")
    for category in CATEGORY_ORDER:
        entry = outfit["items"][category]
        lines.append("- **%s**: %s" % (CATEGORY_LABELS.get(category, category), entry["name"]))
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_text(outfit: Dict[str, object]) -> str:
    """Render an outfit as plain text."""
    lines: List[str] = ["今日穿搭 (Outfit of the Day)", "=" * 30]
    lines.append("Style: %s | Season: %s" % (_style_line(outfit), _season_line(outfit)))
    lines.append("Random %s" % _seed_note(outfit))
    if outfit.get("fallbacks"):
        lines.append(
            "Note: relaxed filtering for %s"
            % ", ".join(CATEGORY_LABELS_EN.get(c, c) for c in outfit["fallbacks"])
        )
    lines.append("")
    for category in CATEGORY_ORDER:
        entry = outfit["items"][category]
        label = CATEGORY_LABELS.get(category, category)
        lines.append("  %-6s %s" % (label + ":", entry["name"]))
    return "\n".join(lines).rstrip() + "\n"


def render_json(outfit: Dict[str, object]) -> str:
    return json.dumps(outfit, ensure_ascii=False, indent=2)


def render(outfit: Dict[str, object], fmt: str = "markdown") -> str:
    if fmt == "text":
        return render_text(outfit)
    if fmt == "json":
        return render_json(outfit)
    return render_markdown(outfit)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Randomly generate one outfit-of-the-day from a built-in wardrobe.",
    )
    parser.add_argument("--seed", type=int, default=None, help="random seed for reproducible output")
    parser.add_argument(
        "--style",
        default=None,
        help="force an outfit style (e.g. casual/休闲, commute/通勤, sport/运动, vintage/复古, minimal/简约)",
    )
    parser.add_argument(
        "--season",
        default=None,
        help="force a season to dress for (spring/夏/autumn/winter or 春/夏/秋/冬)",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "text", "json"),
        default="markdown",
        help="output format (default: markdown)",
    )
    parser.add_argument("--wardrobe", default=None, help="path to a custom wardrobe JSON")
    parser.add_argument("--output", default=None, help="write the outfit to a file instead of stdout")
    parser.add_argument("--list-styles", action="store_true", help="list available styles and exit")
    parser.add_argument("--list-seasons", action="store_true", help="list available seasons and exit")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        wardrobe = load_wardrobe(args.wardrobe)
    except (OSError, ValueError) as exc:
        print("error: cannot load wardrobe: %s" % exc, file=sys.stderr)
        return 2

    if args.list_styles:
        print(", ".join(str(s) for s in wardrobe["styles"]))
        return 0
    if args.list_seasons:
        print(", ".join(str(s) for s in wardrobe["seasons"]))
        return 0

    try:
        outfit = pick_outfit(
            seed=args.seed,
            style=args.style,
            season=args.season,
            wardrobe=wardrobe,
        )
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2

    body = render(outfit, args.format)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(body)
        if args.format != "json":
            print("Seed: %s" % outfit["seed"])
            print("Wrote outfit to %s" % args.output)
    else:
        sys.stdout.write(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())