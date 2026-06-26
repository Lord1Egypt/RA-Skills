#!/usr/bin/env python3
import argparse, csv, os
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--out", default="media_manifest.csv")
    args = ap.parse_args()
    root = Path(args.folder)
    rows = []
    for p in root.rglob("*"):
        if p.is_file():
            stat = p.stat()
            rows.append({
                "path": str(p),
                "filename": p.name,
                "ext": p.suffix.lower(),
                "size_bytes": stat.st_size,
                "created_at": getattr(stat, "st_ctime", ""),
                "modified_at": getattr(stat, "st_mtime", "")
            })
    fields = ["path","filename","ext","size_bytes","created_at","modified_at"]
    with open(args.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
