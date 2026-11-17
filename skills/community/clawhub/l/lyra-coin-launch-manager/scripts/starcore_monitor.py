#!/usr/bin/env python3
"""In-process normalize → verify → local bookmark chain (no process spawn)."""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


def append_log(path: Path, line: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write("\n" + line)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default="STARCORE,STARCOREX,STARCORECOIN")
    ap.add_argument("--workspace", default=".")
    ap.add_argument("--log", default="daily_health.md")
    args = ap.parse_args()
    workspace = Path(args.workspace).resolve()
    log_path = Path(args.log)
    if not log_path.is_absolute():
        log_path = workspace / log_path

    # Import sibling scripts as modules via runpy-style argv
    import normalize_starcore_family as norm
    import verify_starcore_family as ver
    import bookmark_starcore_family as book

    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        old = sys.argv[:]
        sys.argv = ["normalize_starcore_family.py", "--symbols", args.symbols, "--workspace", str(workspace)]
        rc1 = norm.main() if hasattr(norm, "main") else 0
        sys.argv = ["verify_starcore_family.py", "--symbols", args.symbols, "--workspace", str(workspace)]
        rc2 = ver.main() if hasattr(ver, "main") else 0
        sys.argv = [
            "bookmark_starcore_family.py",
            "--symbols",
            args.symbols,
            "--workspace",
            str(workspace),
            "--receipts",
            str(workspace / "state" / "starcore_family_receipts_summary.json"),
        ]
        rc3 = book.main() if hasattr(book, "main") else 0
        sys.argv = old
        if any(r not in (0, None) for r in (rc1, rc2, rc3)):
            append_log(log_path, f"[{ts}] STARCORE monitor: partial fail normalize={rc1} verify={rc2} book={rc3}")
            return 1
        append_log(log_path, f"[{ts}] STARCORE monitor: normalize+verify+bookmark OK for {args.symbols}")
        return 0
    except Exception as exc:
        append_log(log_path, f"[{ts}] STARCORE monitor: ERROR {exc}")
        raise


if __name__ == "__main__":
    raise SystemExit(main())
