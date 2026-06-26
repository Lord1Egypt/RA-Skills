from __future__ import annotations

from typing import Callable, Iterable


EMPTY_LIKE_REASONS = {
    "not_attempted",
    "broad_only",
    "detailed_match",
    "detailed_match_with_time_pref",
}

REASON_LABELS = {
    "not_attempted": "미시도",
    "broad_only": "빠른 스캔 전용",
    "detailed_match": "상세 검색 일치",
    "detailed_match_with_time_pref": "시간 조건 일치",
    "broad_candidate_time_rejected": "시간 조건 탈락",
    "detailed_no_usable_time_filter_match": "usable match 없음",
    "detail_empty_after_broad_hit": "빠른 스캔 가격 있었지만 상세 결과 비어 있음",
    "detail_empty_no_broad_signal": "상세 결과 비어 있음",
    "detail_missing_departure_times": "출발 시간 정보 부족",
    "detail_partial_departure_times": "출발 시간 정보 부분 누락",
    "detail_missing_return_times": "복귀 시간 정보 부족",
    "detail_partial_return_times": "복귀 시간 정보 부분 누락",
    "detail_missing_price_data": "가격 정보 부족",
    "detail_sparse_price_data": "가격 정보 일부 누락",
}

REASON_CODES = {
    "not_attempted": "diagnostic.not_attempted",
    "broad_only": "diagnostic.broad_only",
    "detailed_match": "success.detail_match",
    "detailed_match_with_time_pref": "success.time_pref_match",
    "broad_candidate_time_rejected": "filter.time_pref_rejected",
    "detailed_no_usable_time_filter_match": "filter.no_usable_match",
    "detail_empty_after_broad_hit": "extraction.detail_empty_after_broad_hit",
    "detail_empty_no_broad_signal": "extraction.detail_empty_no_broad_signal",
    "detail_missing_departure_times": "extraction.missing_departure_times",
    "detail_partial_departure_times": "extraction.partial_departure_times",
    "detail_missing_return_times": "extraction.missing_return_times",
    "detail_partial_return_times": "extraction.partial_return_times",
    "detail_missing_price_data": "extraction.missing_price_data",
    "detail_sparse_price_data": "extraction.sparse_price_data",
}

REASON_CATEGORIES = {
    "not_attempted": "diagnostic",
    "broad_only": "diagnostic",
    "detailed_match": "success",
    "detailed_match_with_time_pref": "success",
    "broad_candidate_time_rejected": "time_filter",
    "detailed_no_usable_time_filter_match": "time_filter",
    "detail_empty_after_broad_hit": "extraction",
    "detail_empty_no_broad_signal": "extraction",
    "detail_missing_departure_times": "extraction",
    "detail_partial_departure_times": "extraction",
    "detail_missing_return_times": "extraction",
    "detail_partial_return_times": "extraction",
    "detail_missing_price_data": "extraction",
    "detail_sparse_price_data": "extraction",
}

REASON_PRIORITY = {
    "detail_empty_after_broad_hit": 100,
    "detail_missing_return_times": 95,
    "detail_missing_departure_times": 94,
    "detail_missing_price_data": 93,
    "detail_partial_return_times": 92,
    "detail_partial_departure_times": 91,
    "detail_sparse_price_data": 90,
    "broad_candidate_time_rejected": 70,
    "detailed_no_usable_time_filter_match": 69,
    "detailed_match_with_time_pref": 10,
    "detailed_match": 9,
    "broad_only": 2,
    "not_attempted": 1,
}


def short_reason_label(reason: str) -> str:
    return REASON_LABELS.get(reason, reason)


def reason_code(reason: str | None) -> str | None:
    if not reason:
        return None
    return REASON_CODES.get(reason, f"unknown.{reason}")



def reason_category(reason: str | None) -> str | None:
    if not reason:
        return None
    return REASON_CATEGORIES.get(reason, "unknown")



def classify_refine_row(row: dict | None) -> str:
    if not row:
        return "not_attempted"
    explicit = str(row.get("diagnostic_reason") or "").strip()
    if explicit:
        return explicit
    if row.get("search_stage") == "broad_only":
        return "broad_only"
    raw_count = int(row.get("raw_option_count") or 0)
    valid_count = int(row.get("time_pref_valid_count") or 0)
    broad_price = int(row.get("broad_price") or 0)
    if valid_count > 0:
        return "detailed_match_with_time_pref" if row.get("time_pref_match") else "detailed_match"
    if raw_count <= 0:
        return "detail_empty_after_broad_hit" if broad_price > 0 else "detail_empty_no_broad_signal"
    if broad_price > 0:
        return "broad_candidate_time_rejected"
    return "detailed_no_usable_time_filter_match"



def _detail_hint(row: dict) -> str | None:
    detail = row.get("diagnostic_detail") or {}
    hint = str(detail.get("hint") or "").strip()
    return hint or None



def _rank_reasons(counts: dict[str, int]) -> list[dict]:
    ranked = []
    for reason, count in counts.items():
        ranked.append({
            "reason": reason,
            "reason_code": reason_code(reason),
            "label": short_reason_label(reason),
            "category": reason_category(reason),
            "count": count,
            "priority": REASON_PRIORITY.get(reason, 0),
        })
    ranked.sort(key=lambda item: (-item["priority"], -item["count"], item["reason"]))
    return ranked



def build_refine_diagnostics(
    broad_rows: Iterable[dict],
    detailed_rows: Iterable[dict],
    *,
    key_fn: Callable[[dict], object],
    label_fn: Callable[[dict], str],
    sample_limit: int = 5,
) -> dict:
    broad_rows = list(broad_rows)
    detailed_rows = list(detailed_rows)
    broad_map = {key_fn(row): row for row in broad_rows}
    detailed_map = {key_fn(row): row for row in detailed_rows}
    counts: dict[str, int] = {}
    samples: dict[str, list[str]] = {}
    hint_counts: dict[str, int] = {}
    hint_samples: list[str] = []
    extraction_totals = {
        "rows": 0,
        "raw_options": 0,
        "priced_options": 0,
        "departure_time_options": 0,
        "return_time_options": 0,
        "missing_price_rows": 0,
        "sparse_price_rows": 0,
        "missing_departure_time_rows": 0,
        "partial_departure_time_rows": 0,
        "missing_return_time_rows": 0,
        "partial_return_time_rows": 0,
    }

    for key, broad in broad_map.items():
        detailed = detailed_map.get(key)
        if detailed is None:
            merged = dict(broad)
            merged.setdefault("search_stage", "broad_only")
        else:
            merged = dict(broad)
            merged.update(detailed)
        reason = classify_refine_row(merged)
        counts[reason] = counts.get(reason, 0) + 1
        samples.setdefault(reason, [])
        sample_label = label_fn(merged)
        hint = _detail_hint(merged)
        if hint:
            sample_label = f"{sample_label} ({hint})"
            hint_counts[hint] = hint_counts.get(hint, 0) + 1
            if len(hint_samples) < sample_limit and hint not in hint_samples:
                hint_samples.append(hint)
        if len(samples[reason]) < sample_limit:
            samples[reason].append(sample_label)

        if detailed is not None:
            raw_option_count = int(merged.get("raw_option_count") or 0)
            priced_option_count = int(merged.get("priced_option_count") or 0)
            departure_time_count = int(merged.get("departure_time_count") or 0)
            return_time_count = int(merged.get("return_time_count") or 0)
            extraction_totals["rows"] += 1
            extraction_totals["raw_options"] += raw_option_count
            extraction_totals["priced_options"] += priced_option_count
            extraction_totals["departure_time_options"] += departure_time_count
            extraction_totals["return_time_options"] += return_time_count
            if raw_option_count > 0:
                if priced_option_count <= 0:
                    extraction_totals["missing_price_rows"] += 1
                elif priced_option_count < raw_option_count:
                    extraction_totals["sparse_price_rows"] += 1
                if departure_time_count <= 0:
                    extraction_totals["missing_departure_time_rows"] += 1
                elif departure_time_count < raw_option_count:
                    extraction_totals["partial_departure_time_rows"] += 1
                if bool(merged.get("has_return_time_constraint")):
                    if return_time_count <= 0:
                        extraction_totals["missing_return_time_rows"] += 1
                    elif return_time_count < raw_option_count:
                        extraction_totals["partial_return_time_rows"] += 1

    attempted = len(detailed_map)
    broad_available = sum(1 for row in broad_rows if (row.get("price") or 0) > 0)
    success = counts.get("detailed_match_with_time_pref", 0)
    rejected = counts.get("broad_candidate_time_rejected", 0) + counts.get("detailed_no_usable_time_filter_match", 0)
    extraction_incomplete = sum(
        counts.get(reason, 0)
        for reason in (
            "detail_empty_after_broad_hit",
            "detail_empty_no_broad_signal",
            "detail_missing_departure_times",
            "detail_partial_departure_times",
            "detail_missing_return_times",
            "detail_partial_return_times",
            "detail_missing_price_data",
            "detail_sparse_price_data",
        )
    )
    empty_like = (
        counts.get("detail_empty_after_broad_hit", 0)
        + counts.get("detail_empty_no_broad_signal", 0)
    )
    remaining_available = max(0, broad_available - attempted)
    attempted_with_broad = max(1, sum(1 for row in detailed_rows if (row.get("broad_price") or 0) > 0))

    extraction_summary = {
        **extraction_totals,
        "price_coverage_ratio": extraction_totals["priced_options"] / max(1, extraction_totals["raw_options"]),
        "departure_time_coverage_ratio": extraction_totals["departure_time_options"] / max(1, extraction_totals["raw_options"]),
        "return_time_coverage_ratio": extraction_totals["return_time_options"] / max(1, extraction_totals["raw_options"]),
    }

    summary_bits = []
    if success:
        summary_bits.append(f"시간 조건 일치 {success}건")
    if counts.get("broad_candidate_time_rejected"):
        summary_bits.append(f"시간 조건 탈락 {counts['broad_candidate_time_rejected']}건")
    if counts.get("detailed_no_usable_time_filter_match"):
        summary_bits.append(f"usable match 없음 {counts['detailed_no_usable_time_filter_match']}건")
    if counts.get("detail_empty_after_broad_hit"):
        summary_bits.append(f"빠른 스캔가 있었지만 상세 비어 있음 {counts['detail_empty_after_broad_hit']}건")
    if counts.get("detail_empty_no_broad_signal"):
        summary_bits.append(f"상세 빈결과 {counts['detail_empty_no_broad_signal']}건")
    if counts.get("detail_missing_departure_times"):
        summary_bits.append(f"출발 시간 정보 부족 {counts['detail_missing_departure_times']}건")
    if counts.get("detail_partial_departure_times"):
        summary_bits.append(f"출발 시간 부분 누락 {counts['detail_partial_departure_times']}건")
    if counts.get("detail_missing_return_times"):
        summary_bits.append(f"복귀 시간 정보 부족 {counts['detail_missing_return_times']}건")
    if counts.get("detail_partial_return_times"):
        summary_bits.append(f"복귀 시간 부분 누락 {counts['detail_partial_return_times']}건")
    if counts.get("detail_missing_price_data"):
        summary_bits.append(f"가격 정보 부족 {counts['detail_missing_price_data']}건")
    if counts.get("detail_sparse_price_data"):
        summary_bits.append(f"가격 정보 일부 누락 {counts['detail_sparse_price_data']}건")
    if extraction_totals["partial_departure_time_rows"] and not counts.get("detail_partial_departure_times"):
        summary_bits.append(f"출발 시간 일부 누락 후보 {extraction_totals['partial_departure_time_rows']}건")
    if extraction_totals["partial_return_time_rows"] and not counts.get("detail_partial_return_times"):
        summary_bits.append(f"복귀 시간 일부 누락 후보 {extraction_totals['partial_return_time_rows']}건")
    if extraction_totals["sparse_price_rows"] and not counts.get("detail_sparse_price_data"):
        summary_bits.append(f"가격 일부 누락 후보 {extraction_totals['sparse_price_rows']}건")
    if not summary_bits:
        summary_bits.append("상세 진단 데이터 없음")

    ranked_reasons = _rank_reasons(counts)
    dominant_reason = ranked_reasons[0]["reason"] if ranked_reasons else None

    user_hint = None
    developer_hint = None
    if counts.get("detail_empty_after_broad_hit"):
        user_hint = "일부 날짜/조합은 빠른 스캔 가격이 있었지만 상세 단계에서 빈결과가 나와 추가 후보를 다시 확인했습니다."
        developer_hint = "broad/detail 불일치 빈도가 있어 upstream DOM 변화나 상세 페이지 추출 불안정 가능성을 점검하세요."
    elif counts.get("detail_missing_return_times") or counts.get("detail_partial_return_times"):
        if counts.get("detail_missing_return_times"):
            user_hint = "일부 왕복 후보는 복귀 시간 정보가 부족해 시간 조건 판단에서 제외됐습니다."
        else:
            user_hint = "일부 왕복 후보는 복귀 시간 정보가 들쭉날쭉해 시간 조건 판단 신뢰도가 낮았습니다."
        developer_hint = "return_departure_time 추출 커버리지와 왕복 결과 shape 변화를 점검하세요."
    elif counts.get("detail_missing_departure_times") or counts.get("detail_partial_departure_times"):
        if counts.get("detail_missing_departure_times"):
            user_hint = "일부 후보는 출발 시간 정보가 부족해 시간 조건 판단에서 제외됐습니다."
        else:
            user_hint = "일부 후보는 출발 시간 정보가 부분 누락되어 시간 조건 판단 신뢰도가 낮았습니다."
        developer_hint = "departure_time 추출 커버리지와 시간 셀렉터 안정성을 점검하세요."
    elif counts.get("detail_missing_price_data") or counts.get("detail_sparse_price_data"):
        user_hint = "일부 상세 후보는 가격 정보가 불완전해 제외됐습니다."
        developer_hint = "price 추출 커버리지와 결과 카드별 가격 필드 누락 비율을 점검하세요."
    elif counts.get("broad_candidate_time_rejected"):
        user_hint = "빠른 스캔 최저가 중 일부는 요청한 시간 조건과 맞지 않아 제외됐습니다."

    human_hint = user_hint

    return {
        "counts": counts,
        "reason_codes": {reason: reason_code(reason) for reason in counts},
        "reason_categories": {reason: reason_category(reason) for reason in counts},
        "ranked_reasons": ranked_reasons,
        "samples": samples,
        "summary_text": ", ".join(summary_bits),
        "broad_available": broad_available,
        "attempted": attempted,
        "success": success,
        "rejected": rejected,
        "extraction_incomplete": extraction_incomplete,
        "empty_like": empty_like,
        "remaining_available": remaining_available,
        "rejection_ratio": rejected / attempted_with_broad,
        "empty_like_ratio": empty_like / max(1, attempted),
        "extraction_incomplete_ratio": extraction_incomplete / max(1, attempted),
        "dominant_reason": dominant_reason,
        "dominant_reason_code": reason_code(dominant_reason),
        "dominant_reason_category": reason_category(dominant_reason),
        "dominant_reason_label": short_reason_label(dominant_reason) if dominant_reason else None,
        "primary_interpretation": "extraction_incomplete" if reason_category(dominant_reason) == "extraction" else ("time_filter_rejection" if reason_category(dominant_reason) == "time_filter" else reason_category(dominant_reason)),
        "hint_counts": hint_counts,
        "hint_samples": hint_samples,
        "human_hint": human_hint,
        "user_hint": user_hint,
        "developer_hint": developer_hint,
        "extraction_summary": extraction_summary,
    }



def choose_fallback_plan(diag: dict, *, minimum_target: int, hard_cap: int, pad: int) -> dict:
    broad_available = int(diag.get("broad_available") or 0)
    success = int(diag.get("success") or 0)
    remaining_available = int(diag.get("remaining_available") or 0)
    rejected = int(diag.get("rejected") or 0)
    extraction_incomplete = int(diag.get("extraction_incomplete") or 0)
    empty_like = int(diag.get("empty_like") or 0)
    rejection_ratio = float(diag.get("rejection_ratio") or 0.0)
    empty_like_ratio = float(diag.get("empty_like_ratio") or 0.0)
    extraction_incomplete_ratio = float(diag.get("extraction_incomplete_ratio") or 0.0)
    dominant_reason = str(diag.get("dominant_reason") or "")
    dominant_category = str(diag.get("dominant_reason_category") or "")
    target = min(max(1, minimum_target), broad_available) if broad_available else 0
    shortfall = max(0, target - success)

    reasons = []
    if shortfall > 0:
        reasons.append("coverage.time_pref_shortfall")
    if success == 0 and rejected > 0:
        reasons.append("coverage.zero_success_with_rejections")
    if remaining_available > 0 and rejection_ratio >= 0.5:
        reasons.append("signal.high_time_filter_rejection_ratio")
    if remaining_available > 0 and extraction_incomplete > 0 and extraction_incomplete_ratio >= 0.35:
        reasons.append("signal.high_extraction_incomplete_ratio")
    if remaining_available > 0 and empty_like > 0 and empty_like_ratio >= 0.35:
        reasons.append("signal.high_empty_like_ratio")
    if remaining_available > 0 and dominant_reason == "detail_empty_after_broad_hit":
        reasons.append("signal.broad_detail_disagreement")
    if remaining_available > 0 and dominant_category == "extraction":
        reasons.append(f"signal.extraction_dominant:{reason_code(dominant_reason)}")
    if remaining_available > 0 and dominant_category == "time_filter":
        reasons.append(f"signal.time_filter_dominant:{reason_code(dominant_reason)}")

    triggered = bool(reasons) and remaining_available > 0
    limit = 0
    if triggered:
        extra_pad = pad
        if dominant_reason == "detail_empty_after_broad_hit":
            extra_pad += 1
        if dominant_category == "extraction":
            extra_pad += 1
        limit = min(remaining_available, max(shortfall + extra_pad, min(hard_cap, remaining_available)))

    return {
        "triggered": triggered,
        "target": target,
        "shortfall": shortfall,
        "limit": limit,
        "reasons": reasons,
        "primary_reason": reasons[0] if reasons else None,
        "dominant_reason": dominant_reason or None,
        "dominant_reason_code": reason_code(dominant_reason),
        "dominant_reason_category": dominant_category or None,
    }
