#!/usr/bin/env python3
"""
Gxpcode-translator: write translation log.
Receives JSON data via --data, writes log to logs/ directory.
Performs fallback validation: checks if all matched cn terms appear in translated text.

Usage:
  python write_log.py --data '<json>'
"""

import json, sys, os
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path(__file__).resolve().parent
LOG_DIR = SKILL_DIR / "logs"


def write_log(data: dict):
    """Write translation log to logs/YYYY-MM-DD_HH-MM-SS_trans.md"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = LOG_DIR / f"{ts}_trans.md"

    source_text = data.get("source_text", "")
    translated_text = data.get("translated_text", "")
    matches = data.get("matches", [])
    source_type = data.get("source_type", "text")
    pdf_meta = data.get("pdf_meta", {})

    # Fallback validation: check if cn appears in translated text
    missing_terms = []
    seen = set()
    for m in matches:
        cn = m.get("cn", "")
        en = m.get("en", "")
        if cn and cn not in seen:
            seen.add(cn)
            if cn not in translated_text:
                missing_terms.append(f"{en} → {cn}")

    lines = [
        f"# Translation Log — {ts}",
        "",
        f"- **Type**: {source_type}",
    ]
    if pdf_meta:
        lines.append(f"- **Source**: {pdf_meta.get('source_path', 'N/A')}")
        lines.append(f"- **Pages**: {pdf_meta.get('total_pages', 'N/A')}")

    lines.extend([
        "",
        "## Matched Terms",
        "",
        "| EN | CN |",
        "|---|---|",
    ])
    seen_en = set()
    for m in matches:
        en, cn = m.get("en", ""), m.get("cn", "")
        if en not in seen_en:
            seen_en.add(en)
            lines.append(f"| {en} | {cn} |")

    lines.extend([
        "",
        "## Source Text (first 500 chars)",
        "",
        "```",
        source_text[:500],
        "```",
        "",
        "## Full Source Text",
        "",
        "```",
        source_text,
        "```",
        "",
        "## Translated Text",
        "",
        "```",
        translated_text,
        "```",
    ])

    if missing_terms:
        lines.extend([
            "",
            "## ⚠️ Missing Terms (cn not found in translation)",
            "",
        ])
        for t in missing_terms:
            lines.append(f"- {t}")

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return str(log_path)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Write translation log")
    parser.add_argument("--data", type=str, required=True, help="JSON data string")
    args = parser.parse_args()

    try:
        data = json.loads(args.data)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    log_path = write_log(data)
    # Silent — only print path if something goes wrong and caller needs it
    # but keep it quiet: the caller knows where the log is.


if __name__ == "__main__":
    main()
