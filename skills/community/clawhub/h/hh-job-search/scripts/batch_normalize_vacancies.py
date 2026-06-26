#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 4:
        print("Usage: batch_normalize_vacancies.py <source> <input-dir> <out.jsonl>", file=sys.stderr)
        sys.exit(2)

    source, input_dir, out_path = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    normalizer = Path(__file__).with_name("normalize_vacancy.py")
    rows = []
    for path in sorted([p for p in input_dir.iterdir() if p.is_file()]):
        proc = subprocess.run([sys.executable, str(normalizer), source, str(path)], capture_output=True, text=True, check=True)
        rows.append(json.loads(proc.stdout))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Normalized {len(rows)} vacancies from {input_dir} -> {out_path}")


if __name__ == "__main__":
    main()
