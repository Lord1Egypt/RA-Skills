#!/usr/bin/env python3
"""
validator.py — Validate and sanitize a slide plan JSON before PPTX generation.

Fixes common LLM output issues:
  - Missing required fields
  - Invalid layout names → fallback to "content"
  - Hex colors with "#" prefix → file corruption prevention (critical)
  - Layout-aware body limits (stat: max 3, quote: max 1, others: max 8)
  - Smart bullet truncation: split at sentence/clause boundary, not mid-word
  - Wrong body type (string instead of list)
  - Missing index fields
  - Duplicate slide indexes

Usage:
  python3 scripts/validator.py --plan slide_plan_raw.json --out slide_plan.json
  python3 scripts/validator.py --plan slide_plan_raw.json  # prints to stdout

Exit codes:
  0 — valid (possibly with auto-corrections)
  1 — unrecoverable error (missing "slides" field, invalid JSON, etc.)
"""

import sys
import json
import argparse
import re

VALID_LAYOUTS = {"title", "section", "content", "two-column", "quote", "stat"}

# Per-layout bullet limits (based on what each layout can visually fit)
LAYOUT_BULLET_LIMITS = {
    "title":      0,   # body not used
    "section":    0,   # body not used
    "content":    8,
    "two-column": 10,  # split across two columns
    "quote":      1,   # body[0] is the quote text
    "stat":       3,   # max 3 stat boxes
}

# Max characters per bullet — smart truncation at sentence/clause boundary
MAX_BULLET_CHARS = 80

# Palettes that should never have "#" in hex values
HEX_FIELD_KEYS = {"primary", "secondary", "accent"}


# ── Helpers ───────────────────────────────────────────────────────────────────

def strip_hash(hex_val) -> str:
    """Remove '#' prefix from hex color. Critical: PptxGenJS corrupts files on '#' prefix."""
    if isinstance(hex_val, str):
        return hex_val.lstrip("#").upper()
    return hex_val


def smart_truncate(text: str, max_chars: int) -> str:
    """
    Truncate text intelligently at a sentence or clause boundary.
    Prefers: sentence end (。.!?) > clause comma (，,；;) > word boundary > hard cut.
    """
    if len(text) <= max_chars:
        return text

    window = text[:max_chars]

    # Try sentence-ending punctuation first
    for punct in ["。", ".", "！", "!", "？", "?"]:
        idx = window.rfind(punct)
        if idx > max_chars // 2:
            return window[:idx + 1]

    # Try clause punctuation
    for punct in ["，", ",", "；", ";"]:
        idx = window.rfind(punct)
        if idx > max_chars // 2:
            return window[:idx] + "…"

    # Try space (word boundary for English)
    idx = window.rfind(" ")
    if idx > max_chars // 2:
        return window[:idx] + "…"

    # Hard cut as last resort
    return window[:max_chars - 1] + "…"


def detect_language(text: str) -> str:
    """Rough heuristic: if >20% CJK chars → Chinese, else English."""
    if not text:
        return "en"
    cjk = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    return "zh" if cjk / len(text) > 0.2 else "en"


# ── Core validation ───────────────────────────────────────────────────────────

def validate_palette(palette: dict, corrections: list) -> dict:
    """Strip '#' from all hex color fields. Returns cleaned palette."""
    if not isinstance(palette, dict):
        corrections.append("palette was not a dict — replaced with empty palette")
        return {}
    cleaned = {}
    for key, val in palette.items():
        if key in HEX_FIELD_KEYS and isinstance(val, str) and val.startswith("#"):
            cleaned[key] = strip_hash(val)
            corrections.append(f"palette.{key}: removed '#' prefix (was '{val}' → '{cleaned[key]}')")
        else:
            cleaned[key] = val
    return cleaned


def validate_slide(slide: dict, idx: int, corrections: list) -> dict:
    """Validate and sanitize a single slide dict. Mutates in place, returns it."""
    prefix = f"slide[{idx}]"

    # Ensure index field exists
    if "index" not in slide:
        slide["index"] = idx + 1
        corrections.append(f"{prefix}: added missing 'index' field ({slide['index']})")

    # Ensure title
    if "title" not in slide or not isinstance(slide["title"], str):
        slide["title"] = ""
        corrections.append(f"{prefix}: missing or invalid 'title' — set to empty string")

    # Validate layout
    raw_layout = slide.get("layout", "")
    if raw_layout not in VALID_LAYOUTS:
        slide["layout"] = "content"
        corrections.append(
            f"{prefix}: invalid layout '{raw_layout}' → replaced with 'content' "
            f"(valid: {sorted(VALID_LAYOUTS)})"
        )
    layout = slide["layout"]

    # Normalize body: must be a list of strings
    body = slide.get("body", [])
    if isinstance(body, str):
        body = [body]
        corrections.append(f"{prefix}: body was a string — wrapped in list")
    elif not isinstance(body, list):
        body = []
        corrections.append(f"{prefix}: body was not a list — reset to []")

    # Ensure all body items are strings
    body = [str(item) for item in body]

    # Layout-aware bullet limit
    limit = LAYOUT_BULLET_LIMITS.get(layout, 8)
    if limit == 0 and body:
        # title/section: body is not rendered — preserve but warn
        corrections.append(
            f"{prefix}: layout '{layout}' does not render body bullets "
            f"(body has {len(body)} items — kept but will not appear on slide)"
        )
    elif len(body) > limit:
        original_count = len(body)
        body = body[:limit]
        corrections.append(
            f"{prefix}: body trimmed from {original_count} → {limit} items "
            f"(layout '{layout}' limit is {limit})"
        )

    # Smart truncation per bullet
    truncated = []
    for i, bullet in enumerate(body):
        short = smart_truncate(bullet, MAX_BULLET_CHARS)
        if short != bullet:
            corrections.append(
                f"{prefix}.body[{i}]: truncated at clause boundary "
                f"({len(bullet)} → {len(short)} chars)"
            )
        truncated.append(short)
    slide["body"] = truncated

    # Ensure subtitle is a string
    if "subtitle" in slide and not isinstance(slide["subtitle"], str):
        slide["subtitle"] = str(slide["subtitle"])
        corrections.append(f"{prefix}: subtitle coerced to string")

    # Ensure notes is a string
    if "notes" in slide and not isinstance(slide["notes"], str):
        slide["notes"] = str(slide["notes"])

    # Ensure visual_hint is a string
    if "visual_hint" in slide and not isinstance(slide["visual_hint"], str):
        slide["visual_hint"] = str(slide["visual_hint"])

    # ── Validate chart field (new in v4.1) ────────────────────────────────────
    # chart is a first-class structured field; validate it here so chart_builder
    # receives clean data and never needs to parse or guess formats.
    if "chart" in slide and slide["chart"] is not None:
        slide["chart"] = _validate_chart(slide["chart"], prefix, corrections)

    return slide


VALID_CHART_TYPES = {"bar", "line", "pie", "doughnut", "area"}


def _validate_chart(chart, prefix: str, corrections: list) -> dict | None:
    """
    Validate and sanitize a chart dict.
    Returns cleaned dict, or None if unrecoverable.

    Expected schema:
      {
        "type": "bar" | "line" | "pie" | "doughnut" | "area",
        "title": "optional string",
        "data": [{"label": "Q1", "value": 120}, ...]
      }
    """
    if not isinstance(chart, dict):
        corrections.append(f"{prefix}.chart: not a dict — removed")
        return None

    # Validate type
    chart_type = chart.get("type", "bar")
    if not isinstance(chart_type, str) or chart_type.lower() not in VALID_CHART_TYPES:
        corrections.append(
            f"{prefix}.chart.type: '{chart_type}' is invalid → replaced with 'bar' "
            f"(valid: {sorted(VALID_CHART_TYPES)})"
        )
        chart["type"] = "bar"
    else:
        chart["type"] = chart_type.lower()

    # Validate title
    if "title" not in chart:
        chart["title"] = ""
    elif not isinstance(chart["title"], str):
        chart["title"] = str(chart["title"])
        corrections.append(f"{prefix}.chart.title: coerced to string")

    # Validate data array
    data = chart.get("data")
    if not isinstance(data, list) or len(data) == 0:
        corrections.append(f"{prefix}.chart: 'data' is missing or empty — chart removed")
        return None

    cleaned_data = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            corrections.append(f"{prefix}.chart.data[{i}]: not a dict — skipped")
            continue

        # Label: must be a non-empty string
        label = item.get("label", "")
        if not isinstance(label, str) or not label.strip():
            label = f"Item {i + 1}"
            corrections.append(f"{prefix}.chart.data[{i}].label: missing or empty → '{label}'")
        label = label.strip()

        # Value: must be numeric — coerce strings, reject non-numeric
        raw_val = item.get("value", None)
        value = _coerce_numeric(raw_val)
        if value is None:
            corrections.append(
                f"{prefix}.chart.data[{i}].value: '{raw_val}' is not numeric → set to 0"
            )
            value = 0.0
        elif raw_val != value:
            corrections.append(
                f"{prefix}.chart.data[{i}].value: '{raw_val}' coerced to {value}"
            )

        cleaned_data.append({"label": label, "value": value})

    if not cleaned_data:
        corrections.append(f"{prefix}.chart: no valid data items after cleaning — chart removed")
        return None

    # Enforce max data points (pie/doughnut: 8, others: 20)
    max_points = 8 if chart["type"] in ("pie", "doughnut") else 20
    if len(cleaned_data) > max_points:
        corrections.append(
            f"{prefix}.chart: {len(cleaned_data)} data points → trimmed to {max_points} "
            f"(limit for '{chart['type']}')"
        )
        cleaned_data = cleaned_data[:max_points]

    chart["data"] = cleaned_data
    return chart


def _coerce_numeric(val) -> float | None:
    """
    Try to coerce val to float.
    Handles: int, float, numeric strings, strings with units ("120万", "85%").
    Returns None if unrecoverable.
    """
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        # Strip common suffixes: %, 万, 亿, k, K, m, M, +, etc.
        cleaned = val.strip()
        cleaned = cleaned.rstrip("%万亿kKmM+千百")
        # Remove thousands separators
        cleaned = cleaned.replace(",", "").replace("，", "")
        try:
            return float(cleaned)
        except ValueError:
            pass
    return None


def validate_plan(plan: dict) -> tuple[dict, list, bool]:
    """
    Validate entire slide plan.
    Returns: (corrected_plan, list_of_corrections, is_valid)
    """
    corrections = []

    if not isinstance(plan, dict):
        return plan, ["FATAL: plan is not a JSON object"], False

    if "slides" not in plan:
        return plan, ["FATAL: missing top-level 'slides' field"], False

    if not isinstance(plan["slides"], list):
        return plan, ["FATAL: 'slides' field is not an array"], False

    # Validate palette
    if "palette" in plan:
        plan["palette"] = validate_palette(plan["palette"], corrections)

    # Ensure top-level title
    if "title" not in plan or not isinstance(plan.get("title"), str):
        plan["title"] = "Presentation"
        corrections.append("top-level 'title' missing — set to 'Presentation'")

    # Validate each slide
    for i, slide in enumerate(plan["slides"]):
        if not isinstance(slide, dict):
            plan["slides"][i] = {"index": i + 1, "layout": "content", "title": "", "body": []}
            corrections.append(f"slide[{i}]: was not an object — replaced with blank content slide")
            continue
        plan["slides"][i] = validate_slide(slide, i, corrections)

    # Fix duplicate indexes
    seen_indexes = {}
    for slide in plan["slides"]:
        idx = slide.get("index")
        if idx in seen_indexes:
            new_idx = max(s.get("index", 0) for s in plan["slides"]) + 1
            corrections.append(f"duplicate index {idx} — reassigned to {new_idx}")
            slide["index"] = new_idx
        seen_indexes[slide.get("index")] = True

    return plan, corrections, True


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Validate and sanitize a slide plan JSON")
    parser.add_argument("--plan", required=True, help="Path to raw slide plan JSON")
    parser.add_argument("--out", help="Output path for corrected JSON (default: stdout)")
    parser.add_argument("--strict", action="store_true",
                        help="Exit code 2 if any corrections were made (for CI use)")
    args = parser.parse_args()

    # Load plan
    try:
        with open(args.plan, "r", encoding="utf-8") as f:
            raw = f.read()
        # Strip markdown fences if LLM wrapped output in ```json
        raw = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.MULTILINE)
        raw = re.sub(r"```\s*$", "", raw.strip(), flags=re.MULTILINE)
        plan = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({
            "status": "error",
            "message": f"Invalid JSON: {e}",
            "corrections": [],
        }), file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(json.dumps({
            "status": "error",
            "message": f"File not found: {args.plan}",
            "corrections": [],
        }), file=sys.stderr)
        sys.exit(1)

    # Validate
    corrected, corrections, is_valid = validate_plan(plan)

    if not is_valid:
        print(json.dumps({
            "status": "error",
            "message": corrections[0],
            "corrections": corrections,
        }), file=sys.stderr)
        sys.exit(1)

    # Output corrected plan
    corrected_json = json.dumps(corrected, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(corrected_json)
    else:
        print(corrected_json)

    # Print correction report to stderr
    report = {
        "status": "ok",
        "slide_count": len(corrected.get("slides", [])),
        "corrections_count": len(corrections),
        "corrections": corrections,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2), file=sys.stderr)

    if args.strict and corrections:
        sys.exit(2)


if __name__ == "__main__":
    main()
