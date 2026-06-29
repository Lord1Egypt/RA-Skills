#!/usr/bin/env python3
"""
Pre-translation truncation fixer.

Scans all paddleocr per-page markdown files. For any page where the markdown
was truncated (marked [truncated] or has unbalanced <table>/</table>), rebuilds
the full text from the elements JSON via build_page_text.py and overwrites the
original markdown file.

After this, all *_p*.md files contain complete text — downstream agents never
need to worry about truncation.
"""
import json, re, sys, subprocess, os
from pathlib import Path


def is_truncated(text: str) -> bool:
    """Check if markdown text was truncated."""
    if "[truncated]" in text:
        return True
    table_open = text.count("<table")
    table_close = text.count("</table>")
    if table_open != table_close:
        return True
    return False


def main():
    import argparse
    p = argparse.ArgumentParser(description="Fix truncated markdown pages before translation")
    p.add_argument("--paddleocr-dir", required=True,
                   help="PaddleOCR output directory (contains markdown/ and recognition_json/)")
    p.add_argument("--elements", required=True,
                   help="Path to recognition_json/<file>.json (full elements)")
    p.add_argument("--python-exe", default=sys.executable,
                   help="Path to Python executable")
    p.add_argument("--build-page-script", default=None,
                   help="Path to build_page_text.py (auto-detected if not given)")
    args = p.parse_args()

    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    paddleocr_dir = Path(args.paddleocr_dir)
    markdown_dir = paddleocr_dir / "markdown"
    elements_path = Path(args.elements)
    python_exe = args.python_exe

    # Auto-detect build_page_text.py
    if args.build_page_script:
        build_script = Path(args.build_page_script)
    else:
        skill_dir = Path(__file__).resolve().parent.parent
        build_script = skill_dir / "scripts" / "build_page_text.py"

    if not build_script.exists():
        print(f"ERROR: build_page_text.py not found at {build_script}")
        sys.exit(1)

    if not elements_path.exists():
        print(f"ERROR: elements JSON not found: {elements_path}")
        sys.exit(1)

    page_files = sorted(markdown_dir.glob("*_p*.md"))
    if not page_files:
        print(f"ERROR: No *_p*.md files in {markdown_dir}")
        sys.exit(1)

    fixed = 0
    for pf in page_files:
        text = pf.read_text(encoding="utf-8-sig")

        if not is_truncated(text):
            continue

        # Extract page number from filename
        m = re.search(r'_p(\d+)', pf.name)
        if not m:
            print(f"⚠️  Cannot parse page number from {pf.name}, skipping")
            continue
        page_num = int(m.group(1))

        print(f"⚠️  Truncated: {pf.name} → rebuilding from JSON…")

        # Rebuild full text from elements JSON
        temp_out = pf.with_suffix(".rebuilt_tmp")
        result = subprocess.run(
            [python_exe, str(build_script),
             "--elements", str(elements_path),
             "--page", str(page_num),
             "--output", str(temp_out)],
            capture_output=True, text=True
        )

        if result.returncode != 0 or not temp_out.exists():
            print(f"   ❌ build_page_text.py failed for page {page_num}: {result.stderr[:200]}")
            continue

        # Overwrite the original markdown with the rebuilt text
        rebuilt = temp_out.read_text(encoding="utf-8-sig")
        pf.write_text(rebuilt, encoding="utf-8-sig")
        temp_out.unlink()

        fixed += 1
        print(f"   ✅ {pf.name} fixed ({len(text)} → {len(rebuilt)} chars)")

    print(f"\n✅ Truncation fix complete: {fixed}/{len(page_files)} pages fixed")


if __name__ == "__main__":
    main()
