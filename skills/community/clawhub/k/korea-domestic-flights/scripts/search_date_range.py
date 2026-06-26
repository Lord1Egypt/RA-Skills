#!/usr/bin/env python3
import argparse
import json
import math
import sys
from dataclasses import asdict, is_dataclass
from datetime import timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common_cli import (
    add_section,
    airport_label,
    build_balanced_option_reasons,
    build_best_option_reasons,
    build_price_calendar,
    cabin_label,
    choose_balanced_round_trip_option,
    explain_recommendation,
    filter_and_rank_by_time_preference,
    format_price,
    format_time_or_fallback,
    join_nonempty,
    normalize_airport,
    parse_date_range_text,
    parse_flexible_date,
    parse_time_preference_args,
    pretty_date,
    recommendation_line,
    round_trip_balance_recommendation,
    time_preference_recommendation,
)
from hybrid_observability import build_refine_diagnostics, choose_fallback_plan


def build_dates(start_date, end_date):
    days = []
    current = start_date
    while current <= end_date:
        days.append(current)
        current += timedelta(days=1)
    return days


def _normalize(item):
    if is_dataclass(item):
        return asdict(item)
    if hasattr(item, "__dict__"):
        return dict(item.__dict__)
    return {"value": str(item)}


def _empty_row(dep, ret, price=0, airline=""):
    return {
        "departure_date": dep,
        "return_date": ret,
        "price": price,
        "airline": airline,
        "departure_time": "",
        "return_departure_time": "",
        "preferred_option": None,
        "time_recommendation": None,
        "search_stage": "broad_only",
        "time_pref_match": None,
        "raw_option_count": 0,
        "time_pref_valid_count": 0,
        "broad_price": price,
        "diagnostic_reason": "broad_only",
        "diagnostic_detail": {},
    }


def _candidate_detail(row):
    detail = {
        "departure_date": row["departure_date"],
        "price": row.get("price", 0),
        "reason": row.get("candidate_reason", "broad_rank"),
    }
    if row.get("return_date"):
        detail["return_date"] = row["return_date"]
    return detail


def _choose_refine_dates(dates, broad_rows):
    available = [row for row in broad_rows if row.get("price", 0) and row.get("price", 0) > 0]
    if not available:
        return [], []

    index_by_date = {pretty_date(d): idx for idx, d in enumerate(dates)}
    chosen_indexes = set()
    selected = []
    seen_dates = set()

    def add_date_label(date_label, reason):
        if date_label in seen_dates:
            return
        idx = index_by_date.get(date_label)
        if idx is None:
            return
        seen_dates.add(date_label)
        chosen_indexes.add(idx)
        selected.append({
            "departure_date": date_label,
            "price": next((row["price"] for row in available if row["departure_date"] == date_label), 0),
            "candidate_reason": reason,
        })

    available_by_price = sorted(available, key=lambda x: (x["price"], x["departure_date"]))
    base_count = min(len(available_by_price), max(8, min(len(dates), math.ceil(len(dates) * 0.6))))
    for row in available_by_price[:base_count]:
        add_date_label(row["departure_date"], "cheap_broad_rank")

    for row in available_by_price[: min(4, len(available_by_price))]:
        idx = index_by_date.get(row["departure_date"])
        if idx is None:
            continue
        for neighbor in (idx - 1, idx + 1):
            if 0 <= neighbor < len(dates):
                add_date_label(pretty_date(dates[neighbor]), "neighbor_of_cheap")

    spread_positions = sorted({0, len(dates) - 1, len(dates) // 2, len(dates) // 3, (len(dates) * 2) // 3})
    for pos in spread_positions:
        if 0 <= pos < len(dates):
            add_date_label(pretty_date(dates[pos]), "coverage_anchor")

    for idx in sorted(chosen_indexes):
        row = next((item for item in selected if item["departure_date"] == pretty_date(dates[idx])), None)
        if row is None:
            selected.append({
                "departure_date": pretty_date(dates[idx]),
                "price": next((item["price"] for item in available if item["departure_date"] == pretty_date(dates[idx])), 0),
                "candidate_reason": "selected",
            })

    return [selected, [dates[idx] for idx in sorted(chosen_indexes)]]


def _build_fallback_dates(dates, broad_rows, attempted_dates, limit, diagnostics=None):
    if limit <= 0:
        return []
    diagnostics = diagnostics or {}
    attempted_labels = {pretty_date(d) for d in attempted_dates}
    index_by_date = {pretty_date(d): idx for idx, d in enumerate(dates)}
    broad_by_date = {row["departure_date"]: row for row in broad_rows}
    available = sorted(
        [row for row in broad_rows if row.get("price", 0) and row.get("price", 0) > 0 and row["departure_date"] not in attempted_labels],
        key=lambda x: (x["price"], x["departure_date"]),
    )
    fallback = []
    seen = set()
    dominant_reason = diagnostics.get("dominant_reason")

    def push(date_label, reason):
        if date_label in attempted_labels or date_label in seen or len(fallback) >= limit:
            return
        idx = index_by_date.get(date_label)
        if idx is None:
            return
        seen.add(date_label)
        fallback.append({
            "date": dates[idx],
            "detail": {
                "departure_date": date_label,
                "price": next((row["price"] for row in broad_rows if row["departure_date"] == date_label), 0),
                "reason": reason,
            },
        })

    if dominant_reason == "detail_empty_after_broad_hit":
        empty_labels = []
        for sample in diagnostics.get("samples", {}).get("detail_empty_after_broad_hit", []):
            label = str(sample).split(" (", 1)[0]
            if label in index_by_date:
                empty_labels.append(label)
        for label in empty_labels:
            idx = index_by_date.get(label)
            if idx is None:
                continue
            for neighbor in (idx - 2, idx - 1, idx + 1, idx + 2):
                if 0 <= neighbor < len(dates):
                    push(pretty_date(dates[neighbor]), "fallback_neighbor_of_empty_detail")

    if dominant_reason in {"detail_missing_departure_times", "detail_missing_return_times"}:
        for row in available[: min(limit, 4)]:
            idx = index_by_date.get(row["departure_date"])
            if idx is None:
                continue
            for neighbor in (idx - 1, idx + 1):
                if 0 <= neighbor < len(dates):
                    push(pretty_date(dates[neighbor]), "fallback_neighbor_of_missing_time")

    for row in available:
        push(row["departure_date"], "fallback_broad_rank")
        idx = index_by_date.get(row["departure_date"])
        if idx is None:
            continue
        for neighbor in (idx - 1, idx + 1):
            if 0 <= neighbor < len(dates):
                candidate_label = pretty_date(dates[neighbor])
                if candidate_label in broad_by_date and (broad_by_date[candidate_label].get("price") or 0) > 0:
                    push(candidate_label, "fallback_neighbor")
        if len(fallback) >= limit:
            break
    return fallback


def _diagnose_refine_failure(raw_results, filtered, broad_price, has_return_time_constraint):
    raw_count = len(raw_results)
    priced_count = sum(1 for item in raw_results if int(item.get("price", 0) or 0) > 0)
    depart_time_count = sum(1 for item in raw_results if str(item.get("departure_time") or "").strip())
    return_time_count = sum(1 for item in raw_results if str(item.get("return_departure_time") or "").strip())
    detail = {
        "raw_option_count": raw_count,
        "priced_option_count": priced_count,
        "departure_time_count": depart_time_count,
        "return_time_count": return_time_count,
        "has_return_time_constraint": bool(has_return_time_constraint),
    }
    if raw_count > 0:
        detail["price_coverage_ratio"] = round(priced_count / raw_count, 3)
        detail["departure_time_coverage_ratio"] = round(depart_time_count / raw_count, 3)
        detail["return_time_coverage_ratio"] = round(return_time_count / raw_count, 3)
    if filtered:
        return "detailed_match_with_time_pref", {**detail, "hint": "시간 조건 일치"}
    if not raw_results:
        if broad_price > 0:
            return "detail_empty_after_broad_hit", {**detail, "hint": "빠른 스캔 대비 상세 빈결과"}
        return "detail_empty_no_broad_signal", {**detail, "hint": "상세 빈결과"}
    if priced_count <= 0:
        return "detail_missing_price_data", {**detail, "hint": "가격 정보 없음"}
    if 0 < priced_count < raw_count:
        return "detail_sparse_price_data", {**detail, "hint": "가격 정보 일부 누락"}
    if depart_time_count <= 0:
        return "detail_missing_departure_times", {**detail, "hint": "출발 시간 정보 부족"}
    if 0 < depart_time_count < raw_count:
        return "detail_partial_departure_times", {**detail, "hint": "출발 시간 정보 부분 누락"}
    if has_return_time_constraint and return_time_count <= 0:
        return "detail_missing_return_times", {**detail, "hint": "복귀 시간 정보 부족"}
    if has_return_time_constraint and 0 < return_time_count < raw_count:
        return "detail_partial_return_times", {**detail, "hint": "복귀 시간 정보 부분 누락"}
    if broad_price > 0:
        return "broad_candidate_time_rejected", {**detail, "hint": "시간 조건 미충족"}
    return "detailed_no_usable_time_filter_match", {**detail, "hint": "usable match 없음"}


def _refine_single_date(searcher, origin, destination, dep, ret, args, time_pref, logs, stage, broad_price=0):
    results = searcher.search(
        origin=origin,
        destination=destination,
        departure_date=dep,
        return_date=ret,
        adults=args.adults,
        cabin_class=args.cabin,
        max_results=20,
        progress_callback=lambda msg, dep=dep, stage=stage: logs.append(f"[{stage} {dep}] {msg}"),
        background_mode=False,
    )
    raw_results = [_normalize(item) for item in results]
    filtered, preferred_ranked = filter_and_rank_by_time_preference(raw_results, time_pref)
    cheapest = filtered[0] if filtered else None
    preferred = preferred_ranked[0] if preferred_ranked else None
    diagnostic_reason, diagnostic_detail = _diagnose_refine_failure(
        raw_results,
        filtered,
        broad_price,
        has_return_time_constraint=bool(ret and (time_pref.return_min is not None or time_pref.return_max is not None)),
    )
    return {
        "departure_date": dep,
        "return_date": ret,
        "price": cheapest.get("price", 0) if cheapest else 0,
        "airline": cheapest.get("airline", "") if cheapest else "",
        "departure_time": cheapest.get("departure_time", "") if cheapest else "",
        "return_departure_time": cheapest.get("return_departure_time", "") if cheapest else "",
        "preferred_option": preferred,
        "time_recommendation": time_preference_recommendation(preferred, cheapest, time_pref),
        "search_stage": stage,
        "time_pref_match": bool(cheapest),
        "raw_option_count": len(raw_results),
        "priced_option_count": diagnostic_detail.get("priced_option_count", 0),
        "departure_time_count": diagnostic_detail.get("departure_time_count", 0),
        "return_time_count": diagnostic_detail.get("return_time_count", 0),
        "has_return_time_constraint": diagnostic_detail.get("has_return_time_constraint", False),
        "time_pref_valid_count": len(filtered),
        "broad_price": broad_price,
        "diagnostic_reason": diagnostic_reason,
        "diagnostic_detail": diagnostic_detail,
    }


def main():
    parser = argparse.ArgumentParser(description="Search Korean domestic flights across date ranges")
    parser.add_argument("--origin", required=True, help="예: GMP 또는 김포")
    parser.add_argument("--destination", required=True, help="예: CJU 또는 제주")
    parser.add_argument("--start-date", help="예: 2026-03-25, 내일")
    parser.add_argument("--end-date", help="예: 2026-03-30")
    parser.add_argument("--date-range", help="예: 내일부터 3일, 이번주말, 2026-03-25~2026-03-30")
    parser.add_argument("--return-offset", type=int, default=0)
    parser.add_argument("--adults", type=int, default=1)
    parser.add_argument("--cabin", default="ECONOMY", choices=["ECONOMY", "BUSINESS", "FIRST"])
    parser.add_argument("--time-pref")
    parser.add_argument("--depart-after")
    parser.add_argument("--return-after")
    parser.add_argument("--exclude-early-before")
    parser.add_argument("--prefer", choices=["late", "morning", "afternoon", "evening"])
    parser.add_argument("--human", action="store_true")
    args = parser.parse_args()

    try:
        origin = normalize_airport(args.origin)
        destination = normalize_airport(args.destination)
        if args.date_range:
            start_dt, end_dt = parse_date_range_text(args.date_range)
        elif args.start_date and args.end_date:
            start_dt = parse_flexible_date(args.start_date)
            end_dt = parse_flexible_date(args.end_date)
        else:
            raise ValueError("start/end-date 또는 --date-range 중 하나를 제공해야 합니다.")
    except ValueError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    if end_dt < start_dt:
        print(json.dumps({"status": "error", "message": "end-date must be after or equal to start-date"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    dates = build_dates(start_dt, end_dt)
    if len(dates) > 30:
        print(json.dumps({"status": "error", "message": "date range must be 30 days or less"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    workspace = Path(__file__).resolve().parents[3]
    repo_path = workspace / "tmp" / "Scraping-flight-information"
    if not repo_path.exists():
        print(json.dumps({"status": "error", "message": "Source repository clone not found.", "expected": str(repo_path)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    sys.path.insert(0, str(repo_path))

    time_pref = parse_time_preference_args(args)

    logs = []
    normalized = []
    search_metadata = {
        "strategy": "parallel",
        "time_preference_active": time_pref.active(),
        "time_preference_summary": time_pref.describe(),
        "broad_scan_dates": len(dates),
        "refined_dates": 0,
        "refined_candidates": [],
        "broad_scan_available": 0,
        "fallback_refined_dates": 0,
        "fallback_candidates": [],
        "refine_attempted_dates": 0,
        "refine_success_dates": 0,
        "fallback_triggered": False,
        "fallback_reason": None,
        "fallback_trigger_reasons": [],
        "fallback_reason_codes": [],
        "fallback_decision": None,
        "refine_diagnostics": None,
        "diagnostic_hint": None,
        "developer_diagnostic_hint": None,
    }

    if time_pref.active():
        try:
            from scraping.parallel import ParallelSearcher
            from scraping.searcher import FlightSearcher
        except Exception as exc:
            print(json.dumps({"status": "error", "message": "Failed to import hybrid search components.", "details": str(exc)}, ensure_ascii=False, indent=2))
            sys.exit(1)

        search_metadata["strategy"] = "hybrid_parallel_then_detailed"
        parallel_searcher = ParallelSearcher()
        logs.append("hybrid mode: broad parallel scan started")
        broad_raw = parallel_searcher.search_date_range(
            origin=origin,
            destination=destination,
            dates=[d.strftime("%Y%m%d") for d in dates],
            return_offset=args.return_offset,
            adults=args.adults,
            cabin_class=args.cabin,
            progress_callback=lambda msg: logs.append(f"[broad] {msg}"),
        )
        broad_rows = []
        for d in dates:
            dep = pretty_date(d)
            ret = pretty_date(d + timedelta(days=args.return_offset)) if args.return_offset > 0 else None
            price, airline = broad_raw.get(d.strftime("%Y%m%d"), (0, "N/A"))
            broad_rows.append(_empty_row(dep, ret, price=price, airline=airline))
        refine_candidate_details, refine_dates = _choose_refine_dates(dates, broad_rows)
        search_metadata["broad_scan_available"] = len([row for row in broad_rows if row["price"] and row["price"] > 0])
        search_metadata["refined_dates"] = len(refine_dates)
        search_metadata["refined_candidates"] = refine_candidate_details
        logs.append(
            f"hybrid mode: broad scan complete, available={search_metadata['broad_scan_available']}, refining={search_metadata['refined_dates']}"
        )

        detailed_by_date = {}
        attempted_dates = list(refine_dates)
        searcher = FlightSearcher()
        try:
            broad_price_by_dep = {row["departure_date"]: row.get("price", 0) for row in broad_rows}
            for d in refine_dates:
                dep = pretty_date(d)
                ret = pretty_date(d + timedelta(days=args.return_offset)) if args.return_offset > 0 else None
                detailed_by_date[dep] = _refine_single_date(
                    searcher,
                    origin,
                    destination,
                    dep,
                    ret,
                    args,
                    time_pref,
                    logs,
                    "refine",
                    broad_price=broad_price_by_dep.get(dep, 0),
                )

            successful_details = [row for row in detailed_by_date.values() if row.get("time_pref_match")]
            search_metadata["refine_attempted_dates"] = len(detailed_by_date)
            search_metadata["refine_success_dates"] = len(successful_details)
            diagnostics = build_refine_diagnostics(
                broad_rows,
                detailed_by_date.values(),
                key_fn=lambda row: row["departure_date"],
                label_fn=lambda row: row["departure_date"],
            )
            search_metadata["refine_diagnostics"] = diagnostics
            search_metadata["diagnostic_hint"] = diagnostics.get("human_hint")
            search_metadata["developer_diagnostic_hint"] = diagnostics.get("developer_hint")
            logs.append(f"hybrid refine diagnostics: {diagnostics['summary_text']}")

            fallback_plan = choose_fallback_plan(
                diagnostics,
                minimum_target=max(2, math.ceil(len(dates) * 0.35)),
                hard_cap=min(6, len(dates)),
                pad=2,
            )
            search_metadata["fallback_decision"] = fallback_plan
            search_metadata["fallback_reason_codes"] = list(fallback_plan.get("reasons", []))
            if fallback_plan["triggered"]:
                fallback_dates = _build_fallback_dates(dates, broad_rows, attempted_dates, fallback_plan["limit"], diagnostics)
                if fallback_dates:
                    search_metadata["fallback_triggered"] = True
                    search_metadata["fallback_trigger_reasons"] = fallback_plan["reasons"]
                    search_metadata["fallback_reason"] = (
                        f"후보 확장: {diagnostics['summary_text']}"
                    )
                    search_metadata["fallback_refined_dates"] = len(fallback_dates)
                    search_metadata["fallback_candidates"] = [item["detail"] for item in fallback_dates]
                    logs.append(
                        f"hybrid mode: fallback refine triggered, reason={fallback_plan['primary_reason']}, extra={len(fallback_dates)}"
                    )
                    for item in fallback_dates:
                        dep = pretty_date(item["date"])
                        ret = pretty_date(item["date"] + timedelta(days=args.return_offset)) if args.return_offset > 0 else None
                        detailed_by_date[dep] = _refine_single_date(
                            searcher,
                            origin,
                            destination,
                            dep,
                            ret,
                            args,
                            time_pref,
                            logs,
                            "fallback",
                            broad_price=broad_price_by_dep.get(dep, 0),
                        )
                    search_metadata["refine_attempted_dates"] = len(detailed_by_date)
                    search_metadata["refine_success_dates"] = len([row for row in detailed_by_date.values() if row.get("time_pref_match")])
                    diagnostics = build_refine_diagnostics(
                        broad_rows,
                        detailed_by_date.values(),
                        key_fn=lambda row: row["departure_date"],
                        label_fn=lambda row: row["departure_date"],
                    )
                    search_metadata["refine_diagnostics"] = diagnostics
                    search_metadata["diagnostic_hint"] = diagnostics.get("human_hint")
                    search_metadata["developer_diagnostic_hint"] = diagnostics.get("developer_hint")
                    logs.append(f"hybrid refine diagnostics (after fallback): {diagnostics['summary_text']}")
        finally:
            try:
                searcher.close()
            except Exception:
                pass

        for broad in broad_rows:
            normalized.append(detailed_by_date.get(broad["departure_date"], broad))
    else:
        try:
            from scraping.parallel import ParallelSearcher
        except Exception as exc:
            print(json.dumps({"status": "error", "message": "Failed to import parallel searcher.", "details": str(exc)}, ensure_ascii=False, indent=2))
            sys.exit(1)
        searcher = ParallelSearcher()
        raw = searcher.search_date_range(
            origin=origin,
            destination=destination,
            dates=[d.strftime("%Y%m%d") for d in dates],
            return_offset=args.return_offset,
            adults=args.adults,
            cabin_class=args.cabin,
            progress_callback=lambda msg: logs.append(str(msg)),
        )
        for d in dates:
            key = d.strftime("%Y%m%d")
            price, airline = raw.get(key, (0, "N/A"))
            normalized.append({
                "departure_date": pretty_date(d),
                "return_date": pretty_date(d + timedelta(days=args.return_offset)) if args.return_offset > 0 else None,
                "price": price,
                "airline": airline,
                "departure_time": "",
                "return_departure_time": "",
                "preferred_option": None,
                "time_recommendation": None,
                "search_stage": "parallel",
                "time_pref_match": None,
                "raw_option_count": 0,
                "time_pref_valid_count": 0,
                "diagnostic_detail": {},
            })
        search_metadata["broad_scan_available"] = len([item for item in normalized if item["price"] and item["price"] > 0])

    available = [item for item in normalized if item["price"] and item["price"] > 0]
    available.sort(key=lambda x: x["price"])
    cheapest = available[0] if available else None
    second_price = available[1]["price"] if len(available) > 1 else None

    price_calendar = build_price_calendar(normalized, date_key="departure_date", price_key="price")
    balanced_option = choose_balanced_round_trip_option(available, time_pref) if args.return_offset > 0 else None

    summary = {
        "headline": (
            f"{airport_label(origin)} → {airport_label(destination)} 날짜범위 최저가 {format_price(cheapest['price'])}"
            if cheapest else
            f"{airport_label(origin)} → {airport_label(destination)} 날짜범위 검색 결과가 없습니다."
        ),
        "range": f"{pretty_date(start_dt)} ~ {pretty_date(end_dt)}",
        "trip_type": "왕복 범위검색" if args.return_offset > 0 else "편도 범위검색",
        "search_strategy": search_metadata["strategy"],
        "search_metadata": search_metadata,
        "best_date": cheapest,
        "top_dates": available[:5],
        "price_calendar": price_calendar,
        "balanced_round_trip": balanced_option,
        "diagnostic_hint": search_metadata.get("diagnostic_hint"),
        "recommendation": recommendation_line(
            f"{cheapest['departure_date']}{f'~{cheapest['return_date']}' if cheapest and cheapest['return_date'] else ''}",
            cheapest["price"],
            second_price,
        ) if cheapest else None,
        "recommendation_explained": explain_recommendation(
            f"{cheapest['departure_date']}{f'~{cheapest['return_date']}' if cheapest and cheapest['return_date'] else ''}",
            int(cheapest["price"] or 0),
            second_price,
            build_best_option_reasons(cheapest, second_price, time_pref),
        ) if cheapest else None,
        "time_recommendation": next((item.get("time_recommendation") for item in available if item.get("time_recommendation")), None),
        "balanced_recommendation": round_trip_balance_recommendation(balanced_option, cheapest, time_pref) if balanced_option else None,
        "balanced_recommendation_explained": explain_recommendation(
            f"{balanced_option['departure_date']}~{balanced_option['return_date']}",
            int(balanced_option["price"] or 0),
            int(cheapest["price"] or 0) if cheapest else None,
            build_balanced_option_reasons(balanced_option, cheapest, time_pref),
        ) if balanced_option else None,
    }

    if args.human:
        def date_row_text(item):
            date_text = f"{item['departure_date']} ~ {item['return_date']}" if item.get('return_date') else item['departure_date']
            time_bits = []
            if item.get('return_date'):
                if item.get('departure_time'):
                    time_bits.append(f"가는편 {format_time_or_fallback(item.get('departure_time'))}")
                if item.get('return_departure_time'):
                    time_bits.append(f"오는편 {format_time_or_fallback(item.get('return_departure_time'))}")
            elif item.get('departure_time'):
                time_bits.append(format_time_or_fallback(item.get('departure_time')))
            return join_nonempty([
                date_text,
                format_price(item['price']),
                item.get('airline') or None,
                join_nonempty(time_bits),
            ])

        lines = [summary["headline"]]
        lines.append(f"범위: {summary['range']}")
        lines.append(f"조건: 성인 {args.adults}명 · {cabin_label(args.cabin)}")
        if args.return_offset > 0:
            lines.append(f"왕복 기준: 출발일 + {args.return_offset}일 귀국")
        if time_pref.describe():
            lines.append(f"시간 조건: {time_pref.describe()}")
        if search_metadata["strategy"].startswith("hybrid"):
            hybrid_text = f"검색 방식: 하이브리드(빠른 전체 스캔 {search_metadata['broad_scan_dates']}일 → 상세 재검증 {search_metadata['refined_dates']}일"
            if search_metadata.get("fallback_refined_dates"):
                hybrid_text += f" + fallback {search_metadata['fallback_refined_dates']}일"
            hybrid_text += ")"
            lines.append(hybrid_text)
        if search_metadata.get("diagnostic_hint"):
            lines.append(f"참고: {search_metadata['diagnostic_hint']}")

        add_section(lines, "최저가", [
            f"최저가 날짜: {date_row_text(cheapest)}" if cheapest else None,
            summary.get("recommendation"),
            summary.get("recommendation_explained"),
        ])
        add_section(lines, "시간대 추천", [summary.get("time_recommendation")])
        add_section(lines, "왕복 균형 추천", [summary.get("balanced_recommendation"), summary.get("balanced_recommendation_explained")])
        add_section(lines, "상위 날짜", [f"{idx}. {date_row_text(item)}" for idx, item in enumerate(summary.get("top_dates", []), start=1)])
        if summary["price_calendar"]:
            calendar_rows = summary["price_calendar"]
            preview = calendar_rows[:10]
            add_section(lines, "가격 캘린더", [*(item["label"] for item in preview), f"… 외 {len(calendar_rows) - len(preview)}일" if len(calendar_rows) > len(preview) else None])
        print("\n".join(lines))
        return

    print(json.dumps({
        "status": "success",
        "query": {
            "origin": origin,
            "destination": destination,
            "start_date": pretty_date(start_dt),
            "end_date": pretty_date(end_dt),
            "return_offset": args.return_offset,
            "adults": args.adults,
            "cabin": args.cabin,
            "time_preference": time_pref.describe(),
        },
        "summary": summary,
        "results": normalized,
        "logs": logs,
        "search_metadata": search_metadata,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
