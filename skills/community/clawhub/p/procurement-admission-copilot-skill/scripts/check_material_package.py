# -*- coding: utf-8 -*-
"""Deterministic readiness check for a supplier procurement-admission material package.

Reads a material manifest JSON (produced by the agent from the supplier's documents),
runs completeness + internal-consistency checks, and writes 01-readiness-check.json.

This is the audit baseline: it owns the numeric / consistency judgments. The LLM layer
explains and extends the findings; it must never override a deterministic result.

Usage:
    python -X utf8 check_material_package.py <manifest.json> [--out <dir>] [--ref-date YYYY-MM-DD]

Manifest schema (all fields optional except where noted):
{
  "reference_date": "2026-07-31",                 # optional; defaults to today
  "company_identity": {
    "legal_name_per_doc": {"营业执照": "X有限公司", "产品册": "X公司"},
    "unified_social_credit_code": "91XXXXXXXXXXXXXXXX"   # optional, placeholder
  },
  "certs": [
    {"name": "ISO 9001", "issued": "2023-01-01", "expiry": "2026-01-01", "mandatory": true}
  ],
  "required_docs": [
    {"doc": "营业执照", "present": true, "mandatory": true}
  ],
  "financials": [
    {"source": "财报摘要", "revenue_yuan": 500000000}
  ]
}
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path


NEAR_EXPIRY_DAYS = 90
FINANCIAL_TOLERANCE = 1.10  # max/min revenue ratio above this -> flag inconsistency


def _norm_name(s: str) -> str:
    """Normalize a company name for identity comparison: drop spaces/punctuation, lower-case."""
    if not s:
        return ""
    keep = [c for c in str(s) if c.isalnum()]
    return "".join(keep).lower()


def _parse_date(s):
    if not s:
        return None
    try:
        return datetime.strptime(str(s).strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def _severity_counts(checks):
    out = {"P0": 0, "P1": 0, "P2": 0, "pass": 0}
    for c in checks:
        out[c["severity"]] = out.get(c["severity"], 0) + 1
    return out


def run(manifest: dict) -> dict:
    checks = []
    ref_raw = manifest.get("reference_date")
    ref = _parse_date(ref_raw) or date.today()

    # ---- 1. Identity consistency ----
    identity = manifest.get("company_identity") or {}
    names = identity.get("legal_name_per_doc") or {}
    if names:
        normed = {k: _norm_name(v) for k, v in names.items() if v}
        distinct = set(n for n in normed.values() if n)
        if len(distinct) > 1:
            detail = "; ".join(f"{k}={v}" for k, v in names.items())
            checks.append({
                "id": "identity_conflict", "status": "fail", "severity": "P0",
                "detail": f"同一供应商在不同材料上的法定名称不一致：{detail}",
            })
        else:
            checks.append({
                "id": "identity_conflict", "status": "pass", "severity": "pass",
                "detail": "各材料法定名称一致。",
            })
    else:
        checks.append({
            "id": "identity_conflict", "status": "fail", "severity": "P0",
            "detail": "未提供任何材料上的公司名称，无法确认身份。",
        })

    # ---- 2. USCC presence ----
    uscc = (identity.get("unified_social_credit_code") or "").strip()
    if not uscc:
        checks.append({
            "id": "uscc_missing", "status": "fail", "severity": "P0",
            "detail": "缺失统一社会信用代码（USCC）。",
        })
    else:
        checks.append({
            "id": "uscc_missing", "status": "pass", "severity": "pass",
            "detail": f"USCC 已提供：{uscc}。",
        })

    # ---- 3. Certificate validity ----
    for cert in manifest.get("certs") or []:
        name = cert.get("name", "未命名证书")
        mandatory = bool(cert.get("mandatory", False))
        exp = _parse_date(cert.get("expiry"))
        if not exp:
            checks.append({
                "id": "cert_date", "status": "fail", "severity": "P1" if not mandatory else "P0",
                "detail": f"证书「{name}」缺少有效到期日，无法判定有效性。",
            })
            continue
        days = (exp - ref).days
        if days < 0:
            checks.append({
                "id": "cert_expired", "status": "fail",
                "severity": "P0" if mandatory else "P1",
                "detail": f"证书「{name}」已于 {exp.isoformat()} 过期（强制={mandatory}）。",
            })
        elif days <= NEAR_EXPIRY_DAYS:
            checks.append({
                "id": "cert_near_expiry", "status": "fail", "severity": "P1",
                "detail": f"证书「{name}」将于 {exp.isoformat()} 到期（剩 {days} 天）。",
            })
        else:
            checks.append({
                "id": "cert_valid", "status": "pass", "severity": "pass",
                "detail": f"证书「{name}」有效，到期 {exp.isoformat()}（剩 {days} 天）。",
            })

    # ---- 4. Required-document completeness ----
    for doc in manifest.get("required_docs") or []:
        dname = doc.get("doc", "未命名材料")
        mandatory = bool(doc.get("mandatory", False))
        present = bool(doc.get("present", False))
        if mandatory and not present:
            checks.append({
                "id": "doc_missing", "status": "fail", "severity": "P0",
                "detail": f"缺失强制材料「{dname}」。",
            })
        elif not present:
            checks.append({
                "id": "doc_missing", "status": "fail", "severity": "P2",
                "detail": f"缺失推荐材料「{dname}」（非强制）。",
            })
        else:
            checks.append({
                "id": "doc_present", "status": "pass", "severity": "pass",
                "detail": f"材料「{dname}」已提供。",
            })

    # ---- 5. Financial consistency ----
    revs = []
    for f in manifest.get("financials") or []:
        rv = f.get("revenue_yuan") if f.get("revenue_yuan") is not None else f.get("revenue")
        if isinstance(rv, (int, float)):
            revs.append((f.get("source", "?"), rv))
    if len(revs) >= 2:
        lo = min(v for _, v in revs)
        hi = max(v for _, v in revs)
        if lo > 0 and hi / lo > FINANCIAL_TOLERANCE:
            pairs = "; ".join(f"{s}={v:,}" for s, v in revs)
            checks.append({
                "id": "financial_inconsistency", "status": "fail", "severity": "P1",
                "detail": f"营收数字跨来源不一致（容差 {FINANCIAL_TOLERANCE:.2f}）：{pairs}。",
            })
        else:
            checks.append({
                "id": "financial_consistent", "status": "pass", "severity": "pass",
                "detail": "各来源营收数字在容差内一致。",
            })

    summary = _severity_counts(checks)
    return {
        "reference_date": ref.isoformat(),
        "checks": checks,
        "summary": summary,
        "ready": summary["P0"] == 0,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Deterministic supplier material-package readiness check.")
    ap.add_argument("manifest", help="Path to the material manifest JSON.")
    ap.add_argument("--out", default=".", help="Output directory for 01-readiness-check.json.")
    ap.add_argument("--ref-date", default=None, help="Reference date YYYY-MM-DD (overrides manifest).")
    args = ap.parse_args(argv)

    manifest_path = Path(args.manifest)
    if not manifest_path.is_file():
        print(f"[ERROR] manifest not found: {manifest_path}", file=sys.stderr)
        return 2
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if args.ref_date:
        manifest["reference_date"] = args.ref_date

    result = run(manifest)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "01-readiness-check.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] wrote {out_path}")
    print(f"     reference_date={result['reference_date']}  "
          f"P0={result['summary']['P0']} P1={result['summary']['P1']} P2={result['summary']['P2']}  "
          f"ready={result['ready']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
