#!/usr/bin/env python3
"""
apply.py - Parse code blocks from Grok responses and write them to files.

Handles markdown code blocks with optional language hints and file paths
from fenced code block attributes.
"""

import argparse
import re
import sys
from pathlib import Path


def parse_code_blocks(markdown_text):
    blocks = []
    lines = markdown_text.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]
        fence_match = re.match(r'^(`{3,})(.*)$', line)
        if fence_match:
            fence = fence_match.group(1)
            header = fence_match.group(2).strip()
            parts = header.split(None, 1)
            lang = parts[0] if parts else ""
            path_hint = parts[1] if len(parts) > 1 else ""

            code_lines = []
            i += 1
            while i < len(lines):
                if re.match(r'^' + re.escape(fence) + r'$', lines[i]):
                    i += 1  # Skip past closing fence
                    break
                code_lines.append(lines[i])
                i += 1

            code = '\n'.join(code_lines).strip()

            if code:
                blocks.append({
                    "language": lang,
                    "code": code,
                    "path_hint": path_hint
                })
        else:
            i += 1

    return blocks


def infer_filename(block, base_dir):
    if block.get("path_hint"):
        return block["path_hint"]

    code = block["code"]
    lang = block.get("language", "").lower()

    shebang_match = re.match(r'#!\S+/(\S+)', code.split('\n')[0])
    if shebang_match:
        name = shebang_match.group(1)
        return f"script.{name}"

    lang_map = {
        "python": "output.py", "py": "output.py",
        "javascript": "output.js", "js": "output.js",
        "typescript": "output.ts", "ts": "output.ts",
        "rust": "output.rs", "go": "output.go",
        "java": "Output.java", "c": "output.c",
        "cpp": "output.cpp", "c++": "output.cpp",
        "ruby": "output.rb", "rb": "output.rb",
        "php": "output.php", "shell": "output.sh",
        "bash": "output.sh", "sh": "output.sh",
        "yaml": "output.yaml", "yml": "output.yml",
        "json": "output.json", "toml": "output.toml",
        "html": "output.html", "css": "output.css",
        "sql": "output.sql", "markdown": "output.md",
        "md": "output.md",
    }

    if lang in lang_map:
        return lang_map[lang]

    return "output.txt"


def apply_blocks(blocks, base_dir, dry_run=True):
    base = Path(base_dir).resolve()
    if not dry_run:
        base.mkdir(parents=True, exist_ok=True)

    files_written = 0
    files_skipped = 0
    changes = []

    for block in blocks:
        filename = infer_filename(block, base_dir)
        filepath = (base / filename).resolve()

        # Validate containment using try/except instead of is_relative_to (Python 3.8 compat)
        try:
            rel = filepath.relative_to(base)
            rel_path = str(rel)
        except ValueError:
            # Path is outside base_dir
            files_skipped += 1
            changes.append({
                "path": str(filepath),
                "action": "skipped",
                "reason": "path outside base_dir"
            })
            continue

        if dry_run:
            files_skipped += 1
            action = "would write"
        else:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(block["code"])
            files_written += 1
            action = "written"

        changes.append({
            "path": rel_path,
            "action": action,
            "language": block.get("language", ""),
            "size": len(block["code"])
        })

    return {
        "files_written": files_written,
        "files_skipped": files_skipped,
        "changes": changes
    }


def format_summary(result, base_dir):
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"Applied code blocks to: {base_dir}/")
    lines.append(f"{'='*60}")

    for change in result["changes"]:
        path = change["path"]
        action = change["action"]
        lang = change.get("language", "")
        size = change.get("size", 0)

        if action == "skipped":
            lines.append(f"  SKIPPED: {path} ({change.get('reason', 'n/a')})")
        else:
            lines.append(f"  {path} ({lang}, {size:,} chars) - {action}")

    lines.append(f"\nSummary: {result['files_written']} written, {result['files_skipped']} skipped")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Parse code blocks from Grok responses and write to files")
    parser.add_argument("input", help="Input markdown file, or - for stdin")
    parser.add_argument("--base-dir", "-d", default="./grok-output", help="Base directory for output files")
    parser.add_argument("--yes", "-y", action="store_true", help="Actually write files (default is dry-run)")
    parser.add_argument("--json", action="store_true", help="Output JSON summary")

    args = parser.parse_args()

    if args.input == "-":
        markdown_text = sys.stdin.read()
    else:
        markdown_text = Path(args.input).read_text()

    blocks = parse_code_blocks(markdown_text)

    if not blocks:
        print("No code blocks found in input.", file=sys.stderr)
        sys.exit(0)

    print(f"Found {len(blocks)} code block(s)", file=sys.stderr)

    result = apply_blocks(blocks, args.base_dir, dry_run=not args.yes)

    if args.json:
        import json
        print(json.dumps(result, indent=2))
    else:
        print(format_summary(result, args.base_dir))


if __name__ == "__main__":
    main()