from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import search_real_estate as sre

DEFAULT_GENERATED = SCRIPT_DIR.parent / "references" / "candidate-seeds.generated.json"
DEFAULT_TARGET = SCRIPT_DIR.parent / "references" / "candidate-seeds.json"
DEFAULT_CACHE = SCRIPT_DIR.parent / "data" / "candidate-cache.json"
DEFAULT_INCLUDE_STATUSES = ["verified", "weak-verified"]


def _load_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _dedupe_keep_order(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = str(value or "").strip()
        if not item or item in seen:
            continue
        out.append(item)
        seen.add(item)
    return out


def _normalize_names(values: list[str] | None) -> set[str]:
    return {sre.normalize_complex_alias(v) for v in (values or []) if sre.normalize_complex_alias(v)}


def _merge_aliases(*parts: list[str]) -> list[str]:
    flat: list[str] = []
    for group in parts:
        flat.extend([str(x) for x in group if str(x).strip()])
    expanded: list[str] = []
    for item in flat:
        expanded.extend(sre.expand_alias_variants(item))
    return _dedupe_keep_order(expanded)


def _build_review_row(result: dict[str, Any], existing: dict[str, Any] | None = None) -> dict[str, Any]:
    status = str(result.get("verification_status") or "unresolved")
    seed = result.get("seed_input") or {}
    complex_id = str(result.get("complex_id") or "").strip()
    reason_bits = []
    if result.get("blocked_reasons"):
        reason_bits.append("external-blocked:" + ", ".join(str(x) for x in result.get("blocked_reasons") or []))
    if not complex_id:
        reason_bits.append("complex_id 미확보")
    pool = result.get("candidate_pool") or []
    if complex_id and pool:
        top = pool[0]
        top_name = ((top.get("complex") or {}).get("name") or top.get("name") or "")
        if top_name:
            reason_bits.append(f"top-candidate={top_name} ({complex_id})")
    if not reason_bits:
        reason_bits.append(f"verification_status={status}")

    review_status = {
        "blocked": "blocked-but-high-priority",
        "unresolved": "manual-verification-needed",
        "unverified": "manual-verification-needed",
        "weak-verified": "review-before-promote",
    }.get(status, "manual-verification-needed")
    if existing and existing.get("review_status") == "excluded-for-now":
        review_status = "excluded-for-now"

    next_action = (
        "direct complex URL/ID를 확보해 name/address 정합성을 다시 확인한 뒤 승격한다."
        if not complex_id
        else "preview 결과를 보고 name/address/aliases가 맞으면 --apply-target으로 승격하고, 필요 시 --apply-cache로 warm-cache 한다."
    )

    return {
        "name": result.get("name") or seed.get("name"),
        "district": result.get("district") or seed.get("district"),
        "neighborhood": result.get("neighborhood") or seed.get("neighborhood"),
        "review_status": review_status,
        "reason": "; ".join(reason_bits),
        "next_action": next_action,
        "verification_status": status,
        "confidence": result.get("confidence"),
        "complex_id": complex_id or None,
    }


def _build_entry(result: dict[str, Any], previous: dict[str, Any] | None = None) -> dict[str, Any]:
    seed = result.get("seed_input") or {}
    previous_aliases = list((previous or {}).get("aliases") or [])
    aliases = _merge_aliases(
        [str(result.get("name") or "")],
        list(result.get("aliases") or []),
        list(seed.get("aliases") or []),
        previous_aliases,
    )
    note_bits = [str((previous or {}).get("note") or "").strip(), str(result.get("note") or "").strip()]
    note = " | ".join([x for x in note_bits if x])
    return {
        "complex_id": str(result.get("complex_id") or ""),
        "name": result.get("name") or seed.get("name"),
        "address": result.get("address") or seed.get("address") or (previous or {}).get("address"),
        "household_count": result.get("household_count") or (previous or {}).get("household_count"),
        "aliases": aliases,
        "verification_status": result.get("verification_status"),
        "confidence": result.get("confidence"),
        "source": result.get("source") or "generated:web-search+detail",
        "learned_from": result.get("learned_from") or "apply_generated_seeds.py",
        "note": note or "generated seed promoted to production",
    }


def build_plan(
    generated_payload: dict[str, Any],
    current_payload: dict[str, Any],
    *,
    include_statuses: set[str],
    min_confidence: float,
    only_names: set[str],
    exclude_names: set[str],
) -> dict[str, Any]:
    results = list(generated_payload.get("results") or [])
    existing_entries = list(current_payload.get("entries") or [])
    existing_reviews = list(current_payload.get("manual_review_queue") or [])
    existing_by_id = {str(row.get("complex_id") or ""): row for row in existing_entries if str(row.get("complex_id") or "").strip()}
    existing_reviews_by_name = {sre.normalize_complex_alias(row.get("name") or ""): row for row in existing_reviews}

    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []

    for result in results:
        name = str(result.get("name") or "").strip()
        name_key = sre.normalize_complex_alias(name)
        complex_id = str(result.get("complex_id") or "").strip()
        status = str(result.get("verification_status") or "")
        confidence = float(result.get("confidence") or 0.0)

        if only_names and name_key not in only_names:
            continue
        if exclude_names and name_key in exclude_names:
            continue

        eligible = bool(complex_id) and status in include_statuses and confidence >= min_confidence
        if eligible:
            accepted.append(_build_entry(result, previous=existing_by_id.get(complex_id)))
        else:
            rejected.append({
                "name": name,
                "complex_id": complex_id or None,
                "verification_status": status,
                "confidence": confidence,
            })
            review_rows.append(_build_review_row(result, existing_reviews_by_name.get(name_key)))

    preserved_entries: list[dict[str, Any]] = []
    accepted_ids = {str(row.get("complex_id") or "") for row in accepted}
    for row in existing_entries:
        row_id = str(row.get("complex_id") or "")
        if row_id and row_id not in accepted_ids:
            preserved_entries.append(row)
    merged_entries = sorted(
        [*preserved_entries, *accepted],
        key=lambda row: (str(row.get("name") or ""), str(row.get("complex_id") or "")),
    )

    merged_reviews_by_name = {sre.normalize_complex_alias(row.get("name") or ""): row for row in existing_reviews}
    for row in review_rows:
        merged_reviews_by_name[sre.normalize_complex_alias(row.get("name") or "")] = row
    for row in accepted:
        merged_reviews_by_name.pop(sre.normalize_complex_alias(row.get("name") or ""), None)
    merged_reviews = sorted(merged_reviews_by_name.values(), key=lambda row: str(row.get("name") or ""))

    next_payload = {
        "schema_version": max(2, int(current_payload.get("schema_version") or 2)),
        "updated_at": int(time.time()),
        "policy": current_payload.get("policy") or {
            "production_entry_rule": "verification_status가 verified 또는 weak-verified 이고, complex_id/name/address 정합성이 확인된 항목만 entries에 넣는다.",
            "excluded_rule": "generated 결과에서 complex_id가 있더라도 이름/주소 검증이 실패했거나 차단/오염 가능성이 있으면 entries에 넣지 않는다.",
        },
        "entries": merged_entries,
        "manual_review_queue": merged_reviews,
        "review_summary": {
            "accepted_for_production": [row.get("name") for row in accepted],
            "pending_manual_verification": [row.get("name") for row in merged_reviews],
            "generated_input_count": len(results),
            "accepted_count": len(accepted),
            "rejected_count": len(rejected),
        },
    }
    return {
        "accepted": accepted,
        "rejected": rejected,
        "next_payload": next_payload,
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="generated candidate seed preview/apply 도우미")
    p.add_argument("--input", default=str(DEFAULT_GENERATED), help="candidate-seeds.generated.json 경로")
    p.add_argument("--target", default=str(DEFAULT_TARGET), help="운영 candidate-seeds.json 경로")
    p.add_argument("--cache-file", default=str(DEFAULT_CACHE), help="candidate-cache.json 경로")
    p.add_argument("--include-statuses", default=",".join(DEFAULT_INCLUDE_STATUSES), help="승격 허용 상태 목록")
    p.add_argument("--min-confidence", type=float, default=0.65, help="승격 최소 confidence")
    p.add_argument("--only-names", default="", help="쉼표 구분 이름 필터")
    p.add_argument("--exclude-names", default="", help="쉼표 구분 제외 이름")
    p.add_argument("--apply-target", action="store_true", help="운영 candidate-seeds.json에 반영")
    p.add_argument("--apply-cache", action="store_true", help="accepted 항목을 candidate-cache에도 warm-cache")
    p.add_argument("--json", action="store_true", help="JSON으로 출력")
    p.add_argument("--self-test", action="store_true", help="내장 self-test 실행")
    return p


def run_self_test() -> int:
    sample_generated = {
        "results": [
            {
                "name": "리센츠",
                "district": "송파구",
                "neighborhood": "잠실동",
                "complex_id": "1147",
                "address": "서울특별시 송파구 잠실동",
                "household_count": 5563,
                "aliases": ["리센츠", "잠실 리센츠"],
                "seed_input": {"aliases": ["잠실리센츠"]},
                "verification_status": "verified",
                "confidence": 1.0,
                "source": "generated:test",
                "learned_from": "self-test",
                "note": "ok",
            },
            {
                "name": "은마",
                "district": "강남구",
                "neighborhood": "대치동",
                "complex_id": "",
                "aliases": ["은마", "대치 은마"],
                "verification_status": "blocked",
                "confidence": 0.0,
                "blocked_reasons": ["HTTP 403"],
            },
        ]
    }
    sample_current = {
        "schema_version": 2,
        "entries": [],
        "manual_review_queue": [],
    }
    plan = build_plan(
        sample_generated,
        sample_current,
        include_statuses={"verified", "weak-verified"},
        min_confidence=0.65,
        only_names=set(),
        exclude_names=set(),
    )
    assert len(plan["accepted"]) == 1
    assert plan["accepted"][0]["name"] == "리센츠"
    assert len(plan["next_payload"]["entries"]) == 1
    assert plan["next_payload"]["entries"][0]["complex_id"] == "1147"
    assert len(plan["next_payload"]["manual_review_queue"]) == 1
    assert plan["next_payload"]["manual_review_queue"][0]["name"] == "은마"
    print("SELF_TEST_OK")
    print(json.dumps({
        "accepted": plan["accepted"],
        "review_queue": plan["next_payload"]["manual_review_queue"],
    }, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    args = build_parser().parse_args()
    if args.self_test:
        return run_self_test()

    input_path = Path(args.input)
    target_path = Path(args.target)
    cache_path = Path(args.cache_file)
    include_statuses = {x.strip() for x in str(args.include_statuses or "").split(",") if x.strip()}
    only_names = _normalize_names([x.strip() for x in str(args.only_names or "").split(",") if x.strip()])
    exclude_names = _normalize_names([x.strip() for x in str(args.exclude_names or "").split(",") if x.strip()])

    generated_payload = _load_json(input_path, {"results": []})
    current_payload = _load_json(target_path, {"schema_version": 2, "entries": [], "manual_review_queue": []})
    plan = build_plan(
        generated_payload,
        current_payload,
        include_statuses=include_statuses,
        min_confidence=max(0.0, float(args.min_confidence)),
        only_names=only_names,
        exclude_names=exclude_names,
    )
    next_payload = plan["next_payload"]

    cache_result: dict[str, Any] | None = None
    if args.apply_target:
        _write_json(target_path, next_payload)
    if args.apply_cache:
        previous_cache = sre.CANDIDATE_CACHE_FILE
        sre.CANDIDATE_CACHE_FILE = cache_path
        try:
            cache_saved = sre.seed_candidate_cache(next_payload.get("entries") or [], source=f"generated-seed:{input_path.name}")
            cache_result = {"saved_count": len(cache_saved), "saved": cache_saved}
        finally:
            sre.CANDIDATE_CACHE_FILE = previous_cache

    summary = {
        "input": str(input_path),
        "target": str(target_path),
        "cache_file": str(cache_path),
        "applied_target": bool(args.apply_target),
        "applied_cache": bool(args.apply_cache),
        "accepted_count": len(plan["accepted"]),
        "rejected_count": len(plan["rejected"]),
        "accepted": [
            {
                "name": row.get("name"),
                "complex_id": row.get("complex_id"),
                "verification_status": row.get("verification_status"),
                "confidence": row.get("confidence"),
            }
            for row in plan["accepted"]
        ],
        "rejected": plan["rejected"],
        "manual_review_queue_count": len(next_payload.get("manual_review_queue") or []),
        "cache_result": cache_result,
    }
    if args.json or not (args.apply_target or args.apply_cache):
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
