"""
csv-to-md.py  (v2 — security-hardened)
Converts a CSV file to a Markdown table.

Usage:
    python csv-to-md.py <input.csv> <output.md>

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
        "pandas==2.2.3",
        "tabulate==0.9.0",
    ],
    check=True,
)
if str(_DEP_DIR) not in sys.path:
    sys.path.insert(0, str(_DEP_DIR))

import pandas as pd


def convert(src: str, dst: str):
    try:
        df = pd.read_csv(src, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(src, encoding="latin-1")

    md = df.to_markdown(index=False)
    Path(dst).write_text(md, encoding="utf-8")
    print(f"  Saved → {dst}  ({len(df)} rows × {len(df.columns)} columns)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: csv-to-md.py <input.csv> <output.md>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
