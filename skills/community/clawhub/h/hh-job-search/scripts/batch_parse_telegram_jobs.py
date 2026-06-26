#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print("Usage: batch_parse_telegram_jobs.py <posts-dir> <out.jsonl>", file=sys.stderr)
        sys.exit(2)

    posts_dir = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    parser = Path(__file__).with_name("parse_telegram_job.py")

    rows = []
    for path in sorted(posts_dir.glob("*.txt")):
        proc = subprocess.run([sys.executable, str(parser), str(path)], capture_output=True, text=True, check=True)
        rows.append(json.loads(proc.stdout))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Parsed {len(rows)} Telegram posts -> {out_path}")


if __name__ == "__main__":
    main()
