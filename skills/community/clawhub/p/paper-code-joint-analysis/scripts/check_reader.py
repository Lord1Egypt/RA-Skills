#!/usr/bin/env python3
"""Check that a generated static reader exists beside analysis artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path


MOJIBAKE_MARKERS = [
    "鎬", "绮捐", "鐞", "瀹", "楠", "璁", "婧", "鍥", "鍏",
    "闂", "妫", "骞", "乣", "銆", "€", "�", "Ã", "Â",
]


def mojibake_hits(text: str) -> list[str]:
    return [marker for marker in MOJIBAKE_MARKERS if marker in text]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("analysis_dir")
    args = parser.parse_args()
    root = Path(args.analysis_dir).resolve()
    required = [
        root / "analysis_bundle.json",
        root / "paper_reading_report.md",
        root / "site" / "index.html",
        root / "site" / "assets" / "app.js",
        root / "site" / "assets" / "styles.css",
        root / "site" / "vendor" / "katex" / "katex.min.js",
        root / "site" / "vendor" / "katex" / "katex.min.css",
        root / "site" / "vendor" / "mermaid.min.js",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        print("INVALID reader")
        for path in missing:
            print(f"- missing {path}")
        return 1
    index = (root / "site" / "index.html").read_text(encoding="utf-8")
    app = (root / "site" / "assets" / "app.js").read_text(encoding="utf-8")
    styles = (root / "site" / "assets" / "styles.css").read_text(encoding="utf-8")
    mojibake = []
    for name, text in [("index.html", index), ("app.js", app), ("styles.css", styles)]:
        hits = mojibake_hits(text)
        if hits:
            mojibake.append(f"{name}: {', '.join(hits[:8])}")
    checks = [
        ("loads analysis_bundle.json", "analysis_bundle.json" in app),
        ("loads paper_reading_report.md", "paper_reading_report.md" in app),
        ("loads paper_questions_for_code.md", "paper_questions_for_code.md" in app),
        ("has report nav", "#report" in index),
        ("has questions nav", "#questions" in index),
        ("has formula renderer", "renderFormula" in app),
        ("has markdown math renderer", "markdown-math" in app and "renderMarkdownMath" in app),
        ("hides raw formula fallback after successful render", "formula-rendered .fallback" in styles and "formula-rendered" in app),
        ("has diagram renderer", "renderDiagrams" in app),
        ("does not expose comparison page", "#compare" not in index and "comparison_with_previous" not in app and "renderCompare" not in app),
        ("has no mojibake markers in reader template", not mojibake),
    ]
    failures = [name for name, ok in checks if not ok]
    if failures:
        print("INVALID reader")
        for name in failures:
            print(f"- failed {name}")
        for item in mojibake:
            print(f"- mojibake {item}")
        return 1
    print(f"VALID reader {root / 'site' / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
