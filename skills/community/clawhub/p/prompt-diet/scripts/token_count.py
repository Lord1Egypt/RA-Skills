#!/usr/bin/env python3
"""
token_count.py — Estimate token usage of OpenClaw workspace files.

Usage:
  python3 token_count.py <path> [<path2> ...]
  python3 token_count.py <directory>
  python3 token_count.py <directory> --format json
  python3 token_count.py <directory> --detail

Options:
  --format json   Output machine-readable JSON instead of table
  --detail        Show per-section token breakdown (splits on ## headers)
  --help          Show this help message

Examples:
  python3 token_count.py /home/aif/.openclaw/workspace/
  python3 token_count.py /home/aif/.openclaw/workspace/MEMORY.md --detail
  python3 token_count.py /home/aif/.openclaw/workspace/ --format json
"""

import sys
import os
import json
import argparse
import re

# Target filenames for workspace scan (when a directory is given)
WORKSPACE_FILES = [
    "AGENTS.md",
    "SOUL.md",
    "USER.md",
    "TOOLS.md",
    "IDENTITY.md",
    "HEARTBEAT.md",
    "MEMORY.md",
]

# ── Token counting ────────────────────────────────────────────────────────────

def _try_tiktoken(text: str) -> int | None:
    """Return token count using tiktoken, or None if not available."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except ImportError:
        return None
    except Exception:
        return None


def count_tokens(text: str) -> tuple[int, bool]:
    """
    Returns (token_count, used_tiktoken).
    Falls back to chars/4 approximation if tiktoken is unavailable.
    """
    result = _try_tiktoken(text)
    if result is not None:
        return result, True
    # Fallback: rough approximation (chars / 4)
    return max(1, len(text) // 4), False


# ── Per-section breakdown ─────────────────────────────────────────────────────

def split_sections(text: str) -> list[tuple[str, str]]:
    """
    Split markdown text on ## headings.
    Returns list of (heading, content) tuples.
    The first tuple has heading = "(preamble)" for content before the first ##.
    """
    parts = re.split(r"^(##[^#].*)", text, flags=re.MULTILINE)
    sections = []
    # parts alternates: [pre-heading-text, heading, content, heading, content, ...]
    if parts[0].strip():
        sections.append(("(preamble)", parts[0]))
    i = 1
    while i < len(parts) - 1:
        heading = parts[i].strip()
        content = parts[i + 1] if i + 1 < len(parts) else ""
        sections.append((heading, content))
        i += 2
    if not sections:
        sections.append(("(full file)", text))
    return sections


# ── File discovery ────────────────────────────────────────────────────────────

def resolve_paths(inputs: list[str]) -> list[str]:
    """
    Given a list of paths (files or directories), return list of .md file paths.
    For directories: scan for WORKSPACE_FILES first; if none found, all .md files.
    """
    result = []
    for p in inputs:
        if os.path.isfile(p):
            result.append(p)
        elif os.path.isdir(p):
            found = []
            for fname in WORKSPACE_FILES:
                candidate = os.path.join(p, fname)
                if os.path.isfile(candidate):
                    found.append(candidate)
            if found:
                result.extend(found)
            else:
                # Fallback: all .md files in the directory (non-recursive)
                for fname in sorted(os.listdir(p)):
                    if fname.endswith(".md"):
                        result.append(os.path.join(p, fname))
        else:
            print(f"Warning: '{p}' not found, skipping.", file=sys.stderr)
    return result


# ── Formatting ────────────────────────────────────────────────────────────────

def fmt_table(rows: list[dict], total_tokens: int, used_tiktoken: bool) -> str:
    """Render a plain-text table from file rows."""
    method = "tiktoken cl100k_base" if used_tiktoken else "chars/4 estimate"
    lines = [f"Token count  [{method}]\n"]

    col_file   = max(len(r["file"]) for r in rows)
    col_file   = max(col_file, 4)

    header = f"{'File':<{col_file}}  {'Lines':>6}  {'Tokens':>7}  {'% Total':>7}"
    lines.append(header)
    lines.append("-" * len(header))

    for r in rows:
        pct = (r["tokens"] / total_tokens * 100) if total_tokens else 0
        lines.append(
            f"{r['file']:<{col_file}}  {r['lines']:>6}  {r['tokens']:>7,}  {pct:>6.1f}%"
        )

    lines.append("-" * len(header))
    lines.append(
        f"{'TOTAL':<{col_file}}  {'':>6}  {total_tokens:>7,}  {'100.0%':>7}"
    )
    return "\n".join(lines)


def fmt_detail_section(file_path: str, sections: list[tuple[str, str]], total_tokens: int) -> str:
    """Render per-section detail for one file."""
    col_sec = max((len(h) for h, _ in sections), default=10)
    col_sec = max(col_sec, 7)
    lines = [f"\n  {os.path.basename(file_path)} — section breakdown:"]
    lines.append(f"  {'Section':<{col_sec}}  {'Tokens':>7}")
    lines.append("  " + "-" * (col_sec + 10))
    for heading, content in sections:
        tok, _ = count_tokens(content)
        pct = (tok / total_tokens * 100) if total_tokens else 0
        lines.append(f"  {heading:<{col_sec}}  {tok:>6,}  ({pct:.0f}%)")
    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Estimate token usage of OpenClaw workspace files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="+", help="Files or directories to analyze")
    parser.add_argument(
        "--format", choices=["table", "json"], default="table",
        help="Output format (default: table)"
    )
    parser.add_argument(
        "--detail", action="store_true",
        help="Show per-section breakdown for each file"
    )
    args = parser.parse_args()

    file_paths = resolve_paths(args.paths)
    if not file_paths:
        print("No files found.", file=sys.stderr)
        sys.exit(1)

    rows = []
    used_tiktoken_any = False
    detail_data = {}

    for fp in file_paths:
        try:
            with open(fp, encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            print(f"Warning: cannot read '{fp}': {e}", file=sys.stderr)
            continue

        tokens, used_tiktoken = count_tokens(text)
        used_tiktoken_any = used_tiktoken_any or used_tiktoken
        lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)

        rows.append({
            "file": os.path.basename(fp),
            "path": fp,
            "lines": lines,
            "tokens": tokens,
        })

        if args.detail or args.format == "json":
            sections = split_sections(text)
            detail_data[fp] = [
                {"heading": h, "tokens": count_tokens(c)[0], "chars": len(c)}
                for h, c in sections
            ]

    if not rows:
        print("No files processed.", file=sys.stderr)
        sys.exit(1)

    total_tokens = sum(r["tokens"] for r in rows)

    # ── JSON output ───────────────────────────────────────────────────────────
    if args.format == "json":
        output = {
            "encoding": "cl100k_base" if used_tiktoken_any else "chars/4_estimate",
            "total_tokens": total_tokens,
            "files": [
                {
                    "file": r["file"],
                    "path": r["path"],
                    "lines": r["lines"],
                    "tokens": r["tokens"],
                    "pct_of_total": round(r["tokens"] / total_tokens * 100, 1) if total_tokens else 0,
                    **({"sections": detail_data.get(r["path"], [])} if args.detail else {}),
                }
                for r in rows
            ],
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    # ── Table output ──────────────────────────────────────────────────────────
    print(fmt_table(rows, total_tokens, used_tiktoken_any))

    if args.detail:
        for r in rows:
            sections_raw = split_sections(open(r["path"], encoding="utf-8").read())
            print(fmt_detail_section(r["path"], sections_raw, r["tokens"]))

    if not used_tiktoken_any:
        print(
            "\nNote: tiktoken not installed. Using chars/4 approximation.",
            file=sys.stderr,
        )
        print(
            "      Install with: pip install tiktoken",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
