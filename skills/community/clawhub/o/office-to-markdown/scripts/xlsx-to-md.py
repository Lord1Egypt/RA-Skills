"""
xlsx-to-md.py  (v2 — security-hardened)
Converts an Excel (.xlsx / .xls) file to Markdown.
Each sheet becomes a ## section with a Markdown table.

Usage:
    python xlsx-to-md.py <input.xlsx> <output.md>

Dependencies installed to /tmp/office_md_deps/ (isolated, pinned versions).
"""

import sys, subprocess
from pathlib import Path

# ── isolated dependency install ───────────────────────────────────────────────
_DEP_DIR = Path("/tmp/office_md_deps")
_DEP_DIR.mkdir(exist_ok=True)
subprocess.run(
    [
        sys.executable, "-m", "pip", "install", "--quiet",
        "--target", str(_DEP_DIR),
        "openpyxl==3.1.5",
        "pandas==2.2.3",
        "tabulate==0.9.0",
    ],
    check=True,
)
if str(_DEP_DIR) not in sys.path:
    sys.path.insert(0, str(_DEP_DIR))

import pandas as pd


def convert(src: str, dst: str):
    xl = pd.ExcelFile(src)
    md_lines = []

    for sheet in xl.sheet_names:
        df = xl.parse(sheet)
        md_lines.append(f"## Sheet: {sheet}\n")
        md_lines.append(df.to_markdown(index=False))
        md_lines.append("")

    Path(dst).write_text("\n".join(md_lines), encoding="utf-8")
    print(f"  Saved → {dst}  ({len(xl.sheet_names)} sheet(s))")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: xlsx-to-md.py <input.xlsx> <output.md>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
