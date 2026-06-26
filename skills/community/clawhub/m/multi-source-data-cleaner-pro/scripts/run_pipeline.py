#!/usr/bin/env python3
"""Multi-Source Data Cleaner · end-to-end pipeline (demo)."""
from __future__ import annotations
import argparse, csv, json, sys
from pathlib import Path
from typing import Any, Dict, List
from profile import _read_rows, profile
from normalize_types import to_number, to_iso_date, to_phone, to_bool, mask_pii
from dedup import dedup


PII_GUESS = {"name": ["name","姓名"], "phone": ["phone","mobile","手机","电话"], "id": ["id_number","身份证","idcard"]}


def normalize_row(row: Dict[str, Any], pii_policy: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in row.items():
        kl = k.lower()
        # date columns by name hint
        if any(t in kl for t in ("date","time","日期","时间")):
            iso = to_iso_date(v); out[k] = iso if iso else v
        elif any(t in kl for t in ("phone","mobile","手机","电话")):
            p = to_phone(v)
            if p and pii_policy == "mask": p = mask_pii(p, "phone")
            elif p and pii_policy == "drop": p = None
            out[k] = p
        elif any(t in kl for t in ("amount","price","金额","价格","数量","qty")):
            n = to_number(v); out[k] = n if n is not None else v
        elif any(t in kl for t in ("is_","enabled","active","有效","启用")):
            b = to_bool(v); out[k] = b if b is not None else v
        elif kl in ("name","姓名"):
            v = str(v) if v is not None else v
            if v and pii_policy == "mask": v = mask_pii(v, "name")
            elif v and pii_policy == "drop": v = None
            out[k] = v
        elif any(t in kl for t in ("id_number","身份证","idcard")):
            v = str(v) if v is not None else v
            if v and pii_policy == "mask": v = mask_pii(v, "id")
            elif v and pii_policy == "drop": v = None
            out[k] = v
        else:
            out[k] = v
    return out


def run(input_path: Path, output_dir: Path, pii_policy: str, dedup_keys: List[str]) -> Dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sources = list(input_path.iterdir()) if input_path.is_dir() else [input_path]
    all_rows: List[Dict[str, Any]] = []
    per_source_profile: Dict[str, Any] = {}

    for src in sources:
        if src.is_dir(): continue
        try:
            rows = _read_rows(src)
        except Exception as e:
            per_source_profile[src.name] = {"error": str(e)}
            continue
        per_source_profile[src.name] = profile(rows)
        all_rows.extend(normalize_row(r, pii_policy) for r in rows)

    dq = {
        "completeness": _completeness(all_rows),
        "uniqueness": None,
    }

    if dedup_keys:
        d = dedup(all_rows, dedup_keys)
        all_rows = d["deduplicated_rows"]
        dq["uniqueness"] = {
            "input": d["input_count"], "output": d["output_count"],
            "removed": d["duplicate_pairs_removed"],
        }

    cleaned_path = output_dir / "cleaned.json"
    cleaned_path.write_text(json.dumps(all_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "audit").mkdir(exist_ok=True)
    (output_dir / "audit" / "per_source_profile.json").write_text(
        json.dumps(per_source_profile, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "dq_report.json").write_text(
        json.dumps(dq, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"rows_out": len(all_rows), "dq": dq, "cleaned": str(cleaned_path)}


def _completeness(rows: List[Dict[str, Any]]) -> float:
    if not rows: return 0.0
    total, filled = 0, 0
    for r in rows:
        for v in r.values():
            total += 1
            if v not in (None, "", " "): filled += 1
    return round(filled / total, 3) if total else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--pii-policy", choices=["keep","mask","drop"], default="mask")
    ap.add_argument("--dedup-keys", default="")
    args = ap.parse_args()
    keys = [k.strip() for k in args.dedup_keys.split(",") if k.strip()] if args.dedup_keys else []
    result = run(Path(args.input), Path(args.output_dir), args.pii_policy, keys)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
