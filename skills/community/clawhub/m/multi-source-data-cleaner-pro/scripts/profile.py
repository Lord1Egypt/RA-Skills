"""Profile a tabular dataset (CSV / JSON list) and emit a quality summary."""
from __future__ import annotations
import argparse, csv, json, sys
from pathlib import Path
from typing import Any, Dict, List


def _read_rows(path: Path) -> List[Dict[str, Any]]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else [data]
    # CSV: sniff encoding (utf-8 first, fall back to gbk)
    for enc in ("utf-8-sig", "utf-8", "gbk", "gb18030"):
        try:
            with path.open(encoding=enc, newline="") as f:
                return list(csv.DictReader(f))
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Could not decode {path}")


def profile(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not rows:
        return {"row_count": 0, "columns": {}}
    cols = {k: [] for k in rows[0].keys()}
    for r in rows:
        for k, v in r.items():
            cols.setdefault(k, []).append(v)
    summary: Dict[str, Any] = {}
    for k, vals in cols.items():
        non_null = [v for v in vals if v not in (None, "", " ")]
        unique = len(set(map(str, non_null)))
        summary[k] = {
            "count": len(vals),
            "non_null": len(non_null),
            "null_rate": round(1 - len(non_null) / max(len(vals), 1), 3),
            "unique": unique,
            "sample": non_null[:3],
        }
    return {"row_count": len(rows), "columns": summary}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", default="-")
    args = ap.parse_args()
    rows = _read_rows(Path(args.input))
    rep = profile(rows)
    txt = json.dumps(rep, ensure_ascii=False, indent=2)
    if args.out == "-":
        print(txt)
    else:
        Path(args.out).write_text(txt, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
