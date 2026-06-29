#!/usr/bin/env python3
"""Analyze the cached OpenRouter models listing.

Loads models_raw.json (created by fetch_models.py), converts per-token
prices to $/1M tokens, supports filtering by family / modality / context
length / free / has-cache-pricing, and prints a table or JSON.

Usage:
    python3 analyze.py [--family anthropic/] [--has-image] [--min-ctx 1000000]
                       [--free] [--has-cache] [--sort prompt|completion|cache_read|ctx]
                       [--desc] [--limit 30] [--json] [--stats]
                       [--path models_raw.json]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_PATH = Path(__file__).resolve().parent / "models_raw.json"

PRICING_FIELDS = (
    "prompt",
    "completion",
    "input_cache_read",
    "input_cache_write",
    "web_search",
    "internal_reasoning",
    "image",
    "audio",
)

SORT_KEYS = {"id", "prompt", "completion", "input_cache_read",
             "input_cache_write", "web_search", "internal_reasoning", "ctx"}


def per_million(raw: Any) -> float | None:
    """Convert a per-token price string to $/1M tokens. Returns None on failure or sentinel."""
    if raw is None:
        return None
    try:
        v = float(raw)
    except (TypeError, ValueError):
        return None
    if v < 0:
        return None
    return v * 1_000_000


def fmt(v: float | None) -> str:
    if v is None:
        return "-"
    if v == 0:
        return "0"
    if v < 0.01:
        return f"{v:.4f}"
    if v < 1:
        return f"{v:.3f}"
    return f"{v:.2f}"


def load(path: Path) -> list[dict]:
    data = json.loads(path.read_text())
    return data.get("data", [])


def normalize(model: dict) -> dict:
    pricing = model.get("pricing", {})
    arch = model.get("architecture", {})
    return {
        "id": model["id"],
        "name": model.get("name", ""),
        "context_length": model.get("context_length"),
        "modality": arch.get("modality", ""),
        "input_modalities": arch.get("input_modalities", []),
        "output_modalities": arch.get("output_modalities", []),
        "tokenizer": arch.get("tokenizer", ""),
        "prices": {f: per_million(pricing.get(f)) for f in PRICING_FIELDS},
        "raw_pricing": {f: pricing.get(f) for f in PRICING_FIELDS},
    }


def _is_free(raw_pricing: dict) -> bool:
    try:
        return float(raw_pricing.get("prompt") or "1") == 0 \
           and float(raw_pricing.get("completion") or "1") == 0
    except (TypeError, ValueError):
        return False


def apply_filters(rows: list[dict], args: argparse.Namespace) -> list[dict]:
    out = list(rows)
    if args.family:
        out = [r for r in out if r["id"].startswith(args.family)]
    if args.keyword:
        kw = args.keyword.lower()
        out = [r for r in out if kw in r["id"].lower() or kw in r["name"].lower()]
    if args.min_ctx is not None:
        out = [r for r in out if (r["context_length"] or 0) >= args.min_ctx]
    if args.max_ctx is not None:
        out = [r for r in out if (r["context_length"] or 0) <= args.max_ctx]
    if args.has_image:
        out = [r for r in out if "image" in r["input_modalities"]]
    if args.has_audio:
        out = [r for r in out if "audio" in r["input_modalities"]]
    if args.has_video:
        out = [r for r in out if "video" in r["input_modalities"]]
    if args.has_file:
        out = [r for r in out if "file" in r["input_modalities"]]
    if args.outputs_image:
        out = [r for r in out if "image" in r["output_modalities"]]
    if args.free:
        out = [r for r in out if _is_free(r["raw_pricing"])]
    if args.has_cache:
        out = [r for r in out if r["prices"]["input_cache_read"] is not None]
    if args.has_reasoning_price:
        out = [r for r in out if r["prices"]["internal_reasoning"] is not None]
    return out


def apply_sort(rows: list[dict], key: str, desc: bool = False) -> list[dict]:
    def sort_value(r: dict):
        if key == "ctx":
            return r["context_length"] or 0
        if key in PRICING_FIELDS:
            v = r["prices"].get(key)
            return v if v is not None else float("inf")
        return r["id"]

    return sorted(rows, key=sort_value, reverse=desc)


def render(rows: list[dict]) -> None:
    cols = [
        ("id", 50),
        ("ctx", 9),
        ("input", 26),
        ("output", 10),
        ("prompt", 8),
        ("compl", 8),
        ("cache_r", 8),
        ("cache_w", 8),
        ("web", 8),
        ("reason", 8),
        ("image", 8),
        ("audio", 8),
    ]
    header = " ".join(name.rjust(w) if name not in ("id", "input", "output") else name.ljust(w) for name, w in cols)
    print(header)
    print("-" * sum(w + 1 for _, w in cols))
    for r in rows:
        in_m = ",".join(r["input_modalities"])[:26]
        out_m = ",".join(r["output_modalities"])[:10]
        ctx = r["context_length"] or 0
        print(
            f"{r['id']:<50}"
            f" {ctx:>9}"
            f" {in_m:<26}"
            f" {out_m:<10}"
            f" {fmt(r['prices']['prompt']):>8}"
            f" {fmt(r['prices']['completion']):>8}"
            f" {fmt(r['prices']['input_cache_read']):>8}"
            f" {fmt(r['prices']['input_cache_write']):>8}"
            f" {fmt(r['prices']['web_search']):>8}"
            f" {fmt(r['prices']['internal_reasoning']):>8}"
            f" {fmt(r['prices']['image']):>8}"
            f" {fmt(r['prices']['audio']):>8}"
        )


def round_price(v: float | None) -> float | None:
    if v is None:
        return None
    return round(v, 4)


def render_json(rows: list[dict]) -> None:
    out = []
    for r in rows:
        out.append({
            "id": r["id"],
            "name": r["name"],
            "context_length": r["context_length"],
            "input_modalities": r["input_modalities"],
            "output_modalities": r["output_modalities"],
            "tokenizer": r["tokenizer"],
            "prices": {k: round_price(v) for k, v in r["prices"].items()},
        })
    print(json.dumps(out, ensure_ascii=False, indent=2))


def render_stats(rows: list[dict]) -> None:
    total = len(rows)
    print(f"Total models: {total}")
    for field in PRICING_FIELDS:
        count = sum(1 for r in rows if r["prices"][field] is not None)
        print(f"  {field}: {count}/{total} models have pricing")
    free_count = sum(1 for r in rows if _is_free(r["raw_pricing"]))
    print(f"  free (prompt=0 & completion=0): {free_count}/{total}")
    modalities = {}
    for r in rows:
        for m in r["input_modalities"]:
            modalities[m] = modalities.get(m, 0) + 1
    print("Input modalities:")
    for m, c in sorted(modalities.items(), key=lambda x: -x[1]):
        print(f"  {m}: {c}/{total}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = p.add_argument_group("source")
    src.add_argument("--path", type=Path, default=DEFAULT_PATH, help="Path to models_raw.json")

    flt = p.add_argument_group("filters")
    flt.add_argument("--family", help="Provider prefix, e.g. anthropic/, openai/, qwen/")
    flt.add_argument("--keyword", help="Case-insensitive substring match on id or name")
    flt.add_argument("--min-ctx", type=int, help="Minimum context length")
    flt.add_argument("--max-ctx", type=int, help="Maximum context length")
    flt.add_argument("--has-image", action="store_true")
    flt.add_argument("--has-audio", action="store_true")
    flt.add_argument("--has-video", action="store_true")
    flt.add_argument("--has-file", action="store_true")
    flt.add_argument("--outputs-image", action="store_true")
    flt.add_argument("--free", action="store_true", help="prompt=0 AND completion=0")
    flt.add_argument("--has-cache", action="store_true", help="input_cache_read is priced")
    flt.add_argument("--has-reasoning-price", action="store_true", help="internal_reasoning is priced")

    out = p.add_argument_group("output")
    out.add_argument("--sort", default="prompt",
                     help="One of: " + " | ".join(sorted(SORT_KEYS)))
    out.add_argument("--desc", action="store_true", help="Sort descending (e.g. most expensive first)")
    out.add_argument("--limit", type=int, default=0, help="Limit rows shown (0 = no limit)")
    out.add_argument("--json", action="store_true", dest="output_json", help="Output JSON instead of table")
    out.add_argument("--stats", action="store_true", help="Print coverage statistics instead of model list")
    args = p.parse_args()

    if args.sort not in SORT_KEYS:
        print(f"ERROR: invalid --sort key '{args.sort}'. Must be one of: {', '.join(sorted(SORT_KEYS))}", file=sys.stderr)
        return 2

    if not args.path.exists():
        print(f"ERROR: {args.path} not found. Run fetch_models.py first.", file=sys.stderr)
        return 2

    rows = [normalize(m) for m in load(args.path)]
    rows = apply_filters(rows, args)

    if args.stats:
        render_stats(rows)
        return 0

    rows = apply_sort(rows, args.sort, desc=args.desc)
    if args.limit:
        rows = rows[: args.limit]

    if args.output_json:
        render_json(rows)
    else:
        print(f"# {len(rows)} models (sorted by {args.sort}{'↓' if args.desc else '↑'})\n")
        render(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
