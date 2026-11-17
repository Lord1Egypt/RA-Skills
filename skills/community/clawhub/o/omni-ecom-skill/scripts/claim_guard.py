#!/usr/bin/env python3
"""Fail-closed validation for numeric claims, formulas and attribution."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from metric_semantics import canonical, definition_errors
from artifact_contract import validate_native_claim_identity


HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")
PRIVATE_PATH = re.compile(r"(?i)(?:^[A-Z]:[\\/]|/Users/|/home/)")
CLAIM_ID = re.compile(r"^C-[A-Za-z0-9_-]+$")
BAD_FORMULA = re.compile(r"(?:转化率|conversion)[^。\n]{0,40}(?:GMV|销售额)[^。\n]{0,20}(?:访客|UV|visitor)", re.I)
BAD_ROAS_FORMULA = re.compile(r"(?:ROI|ROAS)[^。\n]{0,40}(?:访客|UV|visitor)", re.I)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"json_root_invalid:{path.name}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def fail(errors: list[str], reason: str) -> None:
    errors.append(reason)


def source_errors(source: Any, index: int) -> list[str]:
    errors: list[str] = []
    if not isinstance(source, dict):
        return [f"claim_{index}_source_ref_missing"]
    for key in ("source_id", "source_file", "field", "source_sha256"):
        if not str(source.get(key) or "").strip():
            errors.append(f"claim_{index}_source_{key}_missing")
    digest = str(source.get("source_sha256") or "")
    if digest and not HEX64.fullmatch(digest):
        errors.append(f"claim_{index}_source_sha256_invalid")
    file_name = str(source.get("source_file") or "")
    if PRIVATE_PATH.search(file_name):
        errors.append(f"claim_{index}_private_source_path_forbidden")
    return errors


def validate_claims(payload: dict[str, Any], report_text: str = "") -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    try:
        validate_native_claim_identity(payload)
    except ValueError as exc:
        fail(errors, str(exc))
    if not str(payload.get("run_id") or "").strip():
        fail(errors, "claim_run_id_missing")
    root_period = str(payload.get("period") or "").strip()
    if not root_period:
        fail(errors, "claim_period_missing")
    additional=payload.get('additional_periods',[])
    if not isinstance(additional,list) or not all(isinstance(p,str) and bool(p.strip()) for p in additional):
        fail(errors,'claim_additional_periods_invalid')
        additional=[]
    if len(additional)!=len(set(additional)) or root_period in additional:
        fail(errors,'claim_additional_periods_duplicate')
    allowed_periods={root_period,*additional}
    claims = payload.get("claims")
    if not isinstance(claims, list) or not claims:
        fail(errors, "claim_ledger_empty")
        return errors, {"claims_count": 0, "verified_count": 0, "derived_count": 0, "unknown_count": 0}

    by_id = {str(row.get('claim_id')): row for row in claims if isinstance(row,dict)}
    seen: set[str] = set()
    for index, claim in enumerate(claims, 1):
        if not isinstance(claim, dict):
            fail(errors, f"claim_{index}_not_object")
            continue
        claim_id = str(claim.get("claim_id") or "")
        if not CLAIM_ID.fullmatch(claim_id):
            fail(errors, f"claim_{index}_id_invalid")
        elif claim_id in seen:
            fail(errors, f"claim_id_duplicate:{claim_id}")
        else:
            seen.add(claim_id)
        metric = canonical(claim.get("metric") or "")
        status = str(claim.get("status") or "").strip().lower()
        period = str(claim.get("period") or "").strip()
        if not metric:
            fail(errors, f"claim_{index}_metric_missing")
        if not period or period not in allowed_periods:
            fail(errors, f"claim_{index}_period_mismatch")
        errors.extend(source_errors(claim.get("source_ref"), index))
        value = claim.get("value")
        if status not in {"verified", "derived", "unknown"}:
            fail(errors, f"claim_{index}_status_invalid")
        if status == "unknown":
            if value is not None:
                fail(errors, f"claim_{index}_unknown_numeric_value_forbidden")
            continue
        if not is_number(value):
            fail(errors, f"claim_{index}_numeric_value_required")
        if status == "derived":
            formula = claim.get("formula")
            if not isinstance(formula, dict) or not all(str(formula.get(k) or "").strip() for k in ("name", "numerator", "denominator", "expression")):
                fail(errors, f"claim_{index}_derived_formula_missing")
            inputs = claim.get("inputs")
            if not isinstance(inputs, list) or len(inputs) < 2 or not all(str(item) in by_id or str(item) in {str(x.get("claim_id")) for x in claims if isinstance(x, dict)} for item in inputs):
                fail(errors, f"claim_{index}_derived_inputs_missing")
            elif any(by_id.get(str(item),{}).get('period')!=claim.get('period') for item in inputs):
                fail(errors,f'claim_{index}_derived_input_period_mismatch')
        errors.extend(definition_errors(claim, by_id, index))
        from net_return_guard import definition as net_return_definition
        try:
            net_return_definition(claim,by_id,payload)
        except (ValueError,TypeError,KeyError) as exc:
            fail(errors,f'claim_{index}_{exc}')
        if metric in {"conversion_rate", "conversion", "转化率"}:
            formula = claim.get("formula") or {}
            numerator = str(formula.get("numerator") or "").lower()
            denominator = str(formula.get("denominator") or "").lower()
            if numerator not in {"paid_buyers", "buyers", "支付买家数"} or denominator not in {"visitors", "uv", "访客", "访客数"}:
                fail(errors, f"claim_{index}_conversion_formula_invalid")
            if "gmv" in numerator or "gmv" in denominator or "销售额" in numerator or "销售额" in denominator:
                fail(errors, f"claim_{index}_conversion_must_not_use_gmv")
        elif metric in {"uv_value", "gmv_per_visitor", "访客价值"}:
            formula = claim.get("formula") or {}
            if str(formula.get("numerator") or "").lower() not in {"gmv", "销售额"} or str(formula.get("denominator") or "").lower() not in {"visitors", "uv", "访客", "访客数"}:
                fail(errors, f"claim_{index}_uv_value_formula_invalid")
        elif metric == "roas":
            formula = claim.get("formula") or {}
            if str(formula.get("name") or "").lower() != "roas" or str(formula.get("numerator") or "").lower() not in {"attributed_gmv", "归因gmv"} or str(formula.get("denominator") or "").lower() not in {"ad_spend", "推广花费", "广告花费"}:
                fail(errors, f"claim_{index}_roas_formula_invalid")
            attribution = claim.get("attribution")
            source = claim.get("source_ref") or {}
            if not isinstance(attribution, dict) or not str(attribution.get("source_id") or "").strip() or not str(attribution.get("window") or "").strip() or not str(attribution.get("level") or "").strip():
                fail(errors, f"claim_{index}_roas_attribution_missing")
            elif str(attribution.get("source_id")) != str(source.get("source_id")):
                fail(errors, f"claim_{index}_roas_source_attribution_mismatch")
            else:
                try:
                    from acquisition_guard import validate as validate_acquisition
                    validate_acquisition(attribution,payload)
                except (ValueError,TypeError) as exc:
                    fail(errors,f"claim_{index}_{exc}")
            inputs = claim.get("inputs") or []
            input_claims = [by_id.get(str(item)) for item in inputs]
            if not any(str(item.get("metric", "")).lower() in {"ad_spend", "推广花费", "广告花费"} for item in input_claims if isinstance(item, dict)):
                fail(errors, f"claim_{index}_roas_spend_input_missing")
            if not any(str(item.get("metric", "")).lower() in {"attributed_gmv", "归因gmv"} for item in input_claims if isinstance(item, dict)):
                fail(errors, f"claim_{index}_roas_gmv_input_missing")
            if any(isinstance(item, dict) and str((item.get("source_ref") or {}).get("source_id")) != str(source.get("source_id")) for item in input_claims):
                fail(errors, f"claim_{index}_roas_input_source_mismatch")
        elif metric in {"net_roi", "净roi"}:
            fail(errors, f"claim_{index}_net_return_definition_unresolved")

    if report_text:
        for claim_id in by_id:
            if claim_id not in report_text:
                fail(errors, f"claim_not_referenced_in_report:{claim_id}")
        if BAD_FORMULA.search(report_text):
            fail(errors, "report_conversion_formula_uses_gmv_per_visitor")
        if BAD_ROAS_FORMULA.search(report_text):
            fail(errors, "report_roas_formula_uses_visitor_value")
    counts = {
        "claims_count": len(claims),
        "verified_count": sum(1 for item in claims if isinstance(item, dict) and item.get("status") == "verified"),
        "derived_count": sum(1 for item in claims if isinstance(item, dict) and item.get("status") == "derived"),
        "unknown_count": sum(1 for item in claims if isinstance(item, dict) and item.get("status") == "unknown"),
    }
    return errors, counts


def main() -> int:
    parser = argparse.ArgumentParser(description="数字来源、公式和归因硬闸门")
    parser.add_argument("validate", nargs="?", help="兼容子命令：validate")
    parser.add_argument("--claims", required=True, help="claim-ledger.json")
    parser.add_argument("--report", help="可选的 report.md；绑定 claim_id 并扫描错误公式")
    parser.add_argument("--output", required=True, help="claim-receipt.json")
    parser.add_argument("--structure-only", action="store_true", help="仅检查索引结构，不生成正式通过凭证")
    parser.add_argument("--require-context", action="store_true", help="按正式完成要求核对原表范围；不改写旧索引或原表")
    args = parser.parse_args()
    output = Path(args.output).expanduser().resolve()
    output_safe = False
    try:
        claims_path = Path(args.claims).expanduser().resolve()
        report_path = Path(args.report).expanduser().resolve() if args.report else None
        payload = read_json(claims_path)
        protected = [claims_path]
        if report_path:
            protected.extend(report_path.parent/name for name in
                             ('report.json','report.md','report.pdf','pdf-delivery.json'))
            protected.append(report_path)
        rows=payload.get('claims',[])
        if isinstance(rows,list):
            for row in rows:
                source=row.get('source_ref') if isinstance(row,dict) else None
                name=source.get('source_file') if isinstance(source,dict) else None
                if isinstance(name,str) and name:
                    protected.append(claims_path.parent/name)
        for path in protected:
            if output==path.resolve() or (output.exists() and path.exists() and output.samefile(path)):
                raise ValueError('claim_output_overlaps_input')
        output_safe = True
        if args.structure_only and args.require_context:
            raise ValueError('claim_context_requires_source_read')
        report_text = report_path.read_text(encoding="utf-8-sig") if report_path else ""
        errors, counts = validate_claims(payload, report_text)
        source_checks = []
        if not errors and not args.structure_only:
            from claim_source_guard import validate_sources
            effective=dict(payload,source_context_policy='required') if args.require_context else payload
            source_checks = validate_sources(effective, claims_path.parent)
            if args.require_context:
                from source_context_guard import summary
                if summary(source_checks)['status']!='all_verified_source_labels_checked':
                    raise ValueError('formal_source_context_evidence_missing')
        from artifact_contract import native_receipt_identity
        receipt: dict[str, Any] = {
            **native_receipt_identity("claim_guard", payload.get("created_by_team_version")),
            "status": ("claim_structure_passed" if args.structure_only else "claim_guard_passed") if not errors else "claim_guard_blocked",
            "source_checks": source_checks,
            "verification_kind": "structure_only" if args.structure_only else "local_source_reproduction_not_authenticity",
            "run_id": payload.get("run_id"),
            "client_scope": payload.get("client_scope"),
            "period": payload.get("period"),
            "claims_file": claims_path.name,
            "claims_sha256": sha256(claims_path),
            **counts,
            "report_file": report_path.name if report_path else None,
            "report_sha256": sha256(report_path) if report_path and report_path.is_file() else None,
            "errors": errors,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }
        from source_context_guard import summary as context_summary
        receipt['source_context_summary']=context_summary(source_checks)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
        return 0 if not errors else 2
    except (OSError, ValueError, KeyError, IndexError, TypeError, ArithmeticError, ImportError, RecursionError) as exc:
        from artifact_contract import native_failure_diagnostic
        receipt = {**native_failure_diagnostic("claim_guard"),
                   "status": "claim_guard_blocked", "errors": [str(exc)],
                   "checked_at": datetime.now(timezone.utc).isoformat()}
        if output_safe:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(receipt, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
