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
    unique_codes,
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


def _broad_row(destination, dep, ret, price=0, airline=""):
    return {
        "destination": destination,
        "destination_label": airport_label(destination),
        "departure_date": dep,
        "return_date": ret,
        "price": price,
        "airline": airline,
        "departure_time": "",
        "return_departure_time": "",
        "preferred_option": None,
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
        "destination": row["destination"],
        "departure_date": row["departure_date"],
        "price": row.get("price", 0),
        "reason": row.get("candidate_reason", "broad_rank"),
    }
    if row.get("return_date"):
        detail["return_date"] = row["return_date"]
    return detail


def _choose_refine_combos(destinations, dates, broad_rows):
    available = [row for row in broad_rows if row.get("price", 0) and row.get("price", 0) > 0]
    if not available:
        return []

    rows_by_destination = {
        destination: sorted(
            [row for row in available if row["destination"] == destination],
            key=lambda x: (x["price"], x["departure_date"]),
        )
        for destination in destinations
    }
    date_index = {pretty_date(d): idx for idx, d in enumerate(dates)}
    chosen = []
    seen = set()

    def add_row(row, reason):
        key = (row["destination"], row["departure_date"])
        if key in seen:
            return
        seen.add(key)
        enriched = dict(row)
        enriched["candidate_reason"] = reason
        chosen.append(enriched)

    per_destination_budget = max(3, min(6, math.ceil(len(dates) * 0.5)))
    for destination in destinations:
        rows = rows_by_destination.get(destination, [])
        for row in rows[:per_destination_budget]:
            add_row(row, "cheap_within_destination")
        for row in rows[: min(3, len(rows))]:
            idx = date_index.get(row["departure_date"])
            if idx is None:
                continue
            for neighbor in (idx - 1, idx + 1):
                if 0 <= neighbor < len(dates):
                    neighbor_label = pretty_date(dates[neighbor])
                    neighbor_row = next((item for item in rows if item["departure_date"] == neighbor_label), None)
                    if neighbor_row:
                        add_row(neighbor_row, "neighbor_of_destination_candidate")

    globally_sorted = sorted(available, key=lambda x: (x["price"], x["destination"], x["departure_date"]))
    global_budget = min(len(globally_sorted), max(len(destinations) * 4, math.ceil(len(available) * 0.35)))
    for row in globally_sorted[:global_budget]:
        add_row(row, "cheap_global_rank")

    anchor_positions = sorted({0, len(dates) - 1, len(dates) // 2})
    for destination in destinations:
        rows = {row["departure_date"]: row for row in rows_by_destination.get(destination, [])}
        for pos in anchor_positions:
            if 0 <= pos < len(dates):
                anchor_label = pretty_date(dates[pos])
                if anchor_label in rows:
                    add_row(rows[anchor_label], "coverage_anchor")

    return chosen


def _build_fallback_combos(destinations, dates, broad_rows, attempted_keys, limit, diagnostics=None):
    if limit <= 0:
        return []
    diagnostics = diagnostics or {}
    date_index = {pretty_date(d): idx for idx, d in enumerate(dates)}
    broad_index = {(row["destination"], row["departure_date"]): row for row in broad_rows}
    available = sorted(
        [row for row in broad_rows if row.get("price", 0) and row.get("price", 0) > 0 and (row["destination"], row["departure_date"]) not in attempted_keys],
        key=lambda x: (x["price"], x["destination"], x["departure_date"]),
    )
    fallback = []
    seen = set()
    dominant_reason = diagnostics.get("dominant_reason")

    def push(row, reason):
        key = (row["destination"], row["departure_date"])
        if key in attempted_keys or key in seen or len(fallback) >= limit:
            return
        seen.add(key)
        enriched = dict(row)
        enriched["candidate_reason"] = reason
        fallback.append(enriched)

    if dominant_reason == "detail_empty_after_broad_hit":
        for sample in diagnostics.get("samples", {}).get("detail_empty_after_broad_hit", []):
            label = str(sample).split(" (", 1)[0]
            parts = label.split()
            if len(parts) != 2:
                continue
            destination, dep = parts
            idx = date_index.get(dep)
            if idx is None:
                continue
            for neighbor in (idx - 1, idx + 1):
                if 0 <= neighbor < len(dates):
                    key = (destination, pretty_date(dates[neighbor]))
                    row = broad_index.get(key)
                    if row and (row.get("price") or 0) > 0:
                        push(row, "fallback_neighbor_of_empty_detail")

    for destination in destinations:
        destination_rows = [row for row in available if row["destination"] == destination]
        if destination_rows:
            preferred_reason = "fallback_best_per_destination"
            if dominant_reason in {"detail_missing_departure_times", "detail_missing_return_times"}:
                preferred_reason = "fallback_best_per_destination_after_missing_time"
            push(destination_rows[0], preferred_reason)

    for row in available:
        push(row, "fallback_global_rank")
        idx = date_index.get(row["departure_date"])
        if idx is not None:
            for neighbor in (idx - 1, idx + 1):
                if 0 <= neighbor < len(dates):
                    neighbor_key = (row["destination"], pretty_date(dates[neighbor]))
                    neighbor_row = broad_index.get(neighbor_key)
                    if neighbor_row and (neighbor_row.get("price") or 0) > 0:
                        push(neighbor_row, "fallback_neighbor")
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


def _refine_combo(searcher, origin, row, args, time_pref, logs, stage, broad_price=0):
    destination = row["destination"]
    dep = row["departure_date"]
    ret = row["return_date"]
    results = searcher.search(
        origin=origin,
        destination=destination,
        departure_date=dep,
        return_date=ret,
        adults=args.adults,
        cabin_class=args.cabin,
        max_results=20,
        progress_callback=lambda msg, dest=destination, dep=dep, stage=stage: logs.append(f"[{stage} {dest} {dep}] {msg}"),
        background_mode=False,
    )
    raw_results = [_normalize(item) for item in results]
    filtered, preferred_ranked = filter_and_rank_by_time_preference(raw_results, time_pref)
    cheapest = filtered[0] if filtered else None
    diagnostic_reason, diagnostic_detail = _diagnose_refine_failure(
        raw_results,
        filtered,
        broad_price,
        has_return_time_constraint=bool(ret and (time_pref.return_min is not None or time_pref.return_max is not None)),
    )
    return {
        "destination": destination,
        "destination_label": airport_label(destination),
        "departure_date": dep,
        "return_date": ret,
        "price": cheapest.get("price", 0) if cheapest else 0,
        "airline": cheapest.get("airline", "") if cheapest else "",
        "departure_time": cheapest.get("departure_time", "") if cheapest else "",
        "return_departure_time": cheapest.get("return_departure_time", "") if cheapest else "",
        "preferred_option": preferred_ranked[0] if preferred_ranked else None,
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
    parser = argparse.ArgumentParser(description="Search combined destination/date ranges for Korean domestic flights")
    parser.add_argument("--origin", required=True)
    parser.add_argument("--destinations", required=True, help="쉼표 구분 목적지 목록")
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--date-range", help="예: 내일부터 5일, 2026-03-25~2026-03-30")
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
        destinations = unique_codes([normalize_airport(x.strip()) for x in args.destinations.split(",") if x.strip()])
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
    if len(dates) * len(destinations) > 90:
        print(json.dumps({"status": "error", "message": "검색 조합 수는 90개 이하로 제한됩니다."}, ensure_ascii=False, indent=2))
        sys.exit(1)

    workspace = Path(__file__).resolve().parents[3]
    repo_path = workspace / "tmp" / "Scraping-flight-information"
    if not repo_path.exists():
        print(json.dumps({"status": "error", "message": "Source repository clone not found.", "expected": str(repo_path)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    sys.path.insert(0, str(repo_path))

    time_pref = parse_time_preference_args(args)

    logs = []
    destination_rows = []
    combos = []
    search_metadata = {
        "strategy": "parallel",
        "time_preference_active": time_pref.active(),
        "time_preference_summary": time_pref.describe(),
        "broad_scan_destinations": len(destinations),
        "broad_scan_dates": len(dates),
        "broad_scan_combos": len(destinations) * len(dates),
        "broad_scan_available": 0,
        "refined_combos": 0,
        "refined_candidates": [],
        "fallback_refined_combos": 0,
        "fallback_candidates": [],
        "refine_attempted_combos": 0,
        "refine_success_combos": 0,
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
        broad_rows = []
        parallel_searcher = ParallelSearcher()
        for destination in destinations:
            logs.append(f"[broad] matrix search start: {destination}")
            raw = parallel_searcher.search_date_range(
                origin=origin,
                destination=destination,
                dates=[d.strftime("%Y%m%d") for d in dates],
                return_offset=args.return_offset,
                adults=args.adults,
                cabin_class=args.cabin,
                progress_callback=lambda msg, dest=destination: logs.append(f"[broad {dest}] {msg}"),
            )
            for d in dates:
                key = d.strftime("%Y%m%d")
                price, airline = raw.get(key, (0, "N/A"))
                broad_rows.append(_broad_row(
                    destination=destination,
                    dep=pretty_date(d),
                    ret=pretty_date(d + timedelta(days=args.return_offset)) if args.return_offset > 0 else None,
                    price=price,
                    airline=airline,
                ))

        search_metadata["broad_scan_available"] = len([row for row in broad_rows if row["price"] and row["price"] > 0])
        refine_rows = _choose_refine_combos(destinations, dates, broad_rows)
        search_metadata["refined_combos"] = len(refine_rows)
        search_metadata["refined_candidates"] = [_candidate_detail(row) for row in refine_rows]
        logs.append(
            f"hybrid mode: broad scan complete, available={search_metadata['broad_scan_available']}, refining={search_metadata['refined_combos']}"
        )

        detailed_map = {}
        attempted_keys = {(row["destination"], row["departure_date"]) for row in refine_rows}
        searcher = FlightSearcher()
        try:
            broad_price_by_key = {(row["destination"], row["departure_date"]): row.get("price", 0) for row in broad_rows}
            for row in refine_rows:
                key = (row["destination"], row["departure_date"])
                detailed_map[key] = _refine_combo(searcher, origin, row, args, time_pref, logs, "refine", broad_price=broad_price_by_key.get(key, 0))

            successful = [row for row in detailed_map.values() if row.get("time_pref_match")]
            search_metadata["refine_attempted_combos"] = len(detailed_map)
            search_metadata["refine_success_combos"] = len(successful)
            diagnostics = build_refine_diagnostics(
                broad_rows,
                detailed_map.values(),
                key_fn=lambda row: (row["destination"], row["departure_date"]),
                label_fn=lambda row: f"{row['destination']} {row['departure_date']}",
            )
            search_metadata["refine_diagnostics"] = diagnostics
            search_metadata["diagnostic_hint"] = diagnostics.get("human_hint")
            search_metadata["developer_diagnostic_hint"] = diagnostics.get("developer_hint")
            logs.append(f"hybrid refine diagnostics: {diagnostics['summary_text']}")

            fallback_plan = choose_fallback_plan(
                diagnostics,
                minimum_target=max(len(destinations), math.ceil(search_metadata["broad_scan_combos"] * 0.18)),
                hard_cap=min(len(destinations) * 3, max(6, len(destinations) + len(dates))),
                pad=len(destinations),
            )
            search_metadata["fallback_decision"] = fallback_plan
            search_metadata["fallback_reason_codes"] = list(fallback_plan.get("reasons", []))
            if fallback_plan["triggered"]:
                fallback_rows = _build_fallback_combos(destinations, dates, broad_rows, attempted_keys, fallback_plan["limit"], diagnostics)
                if fallback_rows:
                    search_metadata["fallback_triggered"] = True
                    search_metadata["fallback_trigger_reasons"] = fallback_plan["reasons"]
                    search_metadata["fallback_reason"] = (
                        f"후보 확장: {diagnostics['summary_text']}"
                    )
                    search_metadata["fallback_refined_combos"] = len(fallback_rows)
                    search_metadata["fallback_candidates"] = [_candidate_detail(row) for row in fallback_rows]
                    logs.append(
                        f"hybrid mode: fallback refine triggered, reason={fallback_plan['primary_reason']}, extra={len(fallback_rows)}"
                    )
                    for row in fallback_rows:
                        key = (row["destination"], row["departure_date"])
                        detailed_map[key] = _refine_combo(searcher, origin, row, args, time_pref, logs, "fallback", broad_price=broad_price_by_key.get(key, 0))
                    search_metadata["refine_attempted_combos"] = len(detailed_map)
                    search_metadata["refine_success_combos"] = len([row for row in detailed_map.values() if row.get("time_pref_match")])
                    diagnostics = build_refine_diagnostics(
                        broad_rows,
                        detailed_map.values(),
                        key_fn=lambda row: (row["destination"], row["departure_date"]),
                        label_fn=lambda row: f"{row['destination']} {row['departure_date']}",
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

        all_rows = []
        for row in broad_rows:
            key = (row["destination"], row["departure_date"])
            all_rows.append(detailed_map.get(key, row))

        for destination in destinations:
            rows = [row for row in all_rows if row["destination"] == destination]
            combos.extend(rows)
            available_rows = [row for row in rows if row["price"] and row["price"] > 0]
            available_rows.sort(key=lambda x: x["price"])
            destination_rows.append({
                "destination": destination,
                "destination_label": airport_label(destination),
                "search_strategy": search_metadata["strategy"],
                "best_option": available_rows[0] if available_rows else None,
                "top_dates": available_rows[:3],
                "price_calendar": build_price_calendar(rows, date_key="departure_date", price_key="price"),
            })
    else:
        try:
            from scraping.parallel import ParallelSearcher
        except Exception as exc:
            print(json.dumps({"status": "error", "message": "Failed to import parallel searcher.", "details": str(exc)}, ensure_ascii=False, indent=2))
            sys.exit(1)
        searcher = ParallelSearcher()
        for destination in destinations:
            logs.append(f"matrix search start: {destination}")
            raw = searcher.search_date_range(
                origin=origin,
                destination=destination,
                dates=[d.strftime("%Y%m%d") for d in dates],
                return_offset=args.return_offset,
                adults=args.adults,
                cabin_class=args.cabin,
                progress_callback=lambda msg, dest=destination: logs.append(f"[{dest}] {msg}"),
            )
            rows = []
            for d in dates:
                key = d.strftime("%Y%m%d")
                price, airline = raw.get(key, (0, "N/A"))
                row = {
                    "destination": destination,
                    "destination_label": airport_label(destination),
                    "departure_date": pretty_date(d),
                    "return_date": pretty_date(d + timedelta(days=args.return_offset)) if args.return_offset > 0 else None,
                    "price": price,
                    "airline": airline,
                    "departure_time": "",
                    "return_departure_time": "",
                    "preferred_option": None,
                    "search_stage": "parallel",
                    "time_pref_match": None,
                    "raw_option_count": 0,
                    "time_pref_valid_count": 0,
                    "diagnostic_detail": {},
                }
                rows.append(row)
                combos.append(row)
            available_rows = [row for row in rows if row["price"] and row["price"] > 0]
            available_rows.sort(key=lambda x: x["price"])
            destination_rows.append({
                "destination": destination,
                "destination_label": airport_label(destination),
                "search_strategy": search_metadata["strategy"],
                "best_option": available_rows[0] if available_rows else None,
                "top_dates": available_rows[:3],
                "price_calendar": build_price_calendar(rows, date_key="departure_date", price_key="price"),
            })
        search_metadata["broad_scan_available"] = len([row for row in combos if row["price"] and row["price"] > 0])

    ranked_combos = sorted([row for row in combos if row["price"] and row["price"] > 0], key=lambda x: x["price"])
    best = ranked_combos[0] if ranked_combos else None
    balanced_combo = choose_balanced_round_trip_option(ranked_combos, time_pref) if args.return_offset > 0 else None
    second_price = ranked_combos[1]["price"] if len(ranked_combos) > 1 else None

    destination_rows.sort(key=lambda x: x["best_option"]["price"] if x["best_option"] else 10**12)
    summary = {
        "headline": (
            f"{airport_label(origin)} 출발 최적 조합은 {best['destination_label']} {best['departure_date']} {format_price(best['price'])}"
            if best else
            f"{airport_label(origin)} 출발 목적지+날짜 범위 검색 결과가 없습니다."
        ),
        "range": f"{pretty_date(start_dt)} ~ {pretty_date(end_dt)}",
        "search_strategy": search_metadata["strategy"],
        "search_metadata": search_metadata,
        "best_combo": best,
        "balanced_round_trip": balanced_combo,
        "top_combos": ranked_combos[:7],
        "by_destination": destination_rows,
        "diagnostic_hint": search_metadata.get("diagnostic_hint"),
        "recommendation": recommendation_line(
            f"{best['destination_label']} / {best['departure_date']}{f'~{best['return_date']}' if best and best['return_date'] else ''}",
            best["price"],
            second_price,
        ) if best else None,
        "recommendation_explained": explain_recommendation(
            f"{best['destination_label']} / {best['departure_date']}{f'~{best['return_date']}' if best and best['return_date'] else ''}",
            int(best["price"] or 0),
            second_price,
            build_best_option_reasons(best, second_price, time_pref),
        ) if best else None,
        "balanced_recommendation": round_trip_balance_recommendation(balanced_combo, best, time_pref) if balanced_combo else None,
        "balanced_recommendation_explained": explain_recommendation(
            f"{balanced_combo['destination_label']} / {balanced_combo['departure_date']}{f'~{balanced_combo['return_date']}' if balanced_combo and balanced_combo['return_date'] else ''}",
            int(balanced_combo["price"] or 0),
            int(best["price"] or 0) if best else None,
            build_balanced_option_reasons(balanced_combo, best, time_pref),
        ) if balanced_combo else None,
    }

    if args.human:
        def combo_text(item):
            date_text = f"{item['departure_date']} ~ {item['return_date']}" if item.get('return_date') else item['departure_date']
            time_bits = []
            if item.get('departure_time'):
                time_bits.append(f"가는편 {format_time_or_fallback(item.get('departure_time'))}")
            if item.get('return_departure_time'):
                time_bits.append(f"오는편 {format_time_or_fallback(item.get('return_departure_time'))}")
            return join_nonempty([
                item.get('destination_label') or None,
                date_text,
                format_price(item['price']),
                item.get('airline') or None,
                join_nonempty(time_bits),
            ])

        lines = [summary["headline"]]
        lines.append(f"범위: {summary['range']}")
        lines.append(f"조건: 출발 {airport_label(origin)} · 목적지 {len(destinations)}곳 · 성인 {args.adults}명 · {cabin_label(args.cabin)}")
        if args.return_offset > 0:
            lines.append(f"왕복 기준: 출발일 + {args.return_offset}일 귀국")
        if time_pref.describe():
            lines.append(f"시간 조건: {time_pref.describe()}")
        if search_metadata["strategy"].startswith("hybrid"):
            hybrid_text = f"검색 방식: 하이브리드(빠른 전체 스캔 {search_metadata['broad_scan_combos']}조합 → 상세 재검증 {search_metadata['refined_combos']}조합"
            if search_metadata.get("fallback_refined_combos"):
                hybrid_text += f" + fallback {search_metadata['fallback_refined_combos']}조합"
            hybrid_text += ")"
            lines.append(hybrid_text)
        if search_metadata.get("diagnostic_hint"):
            lines.append(f"참고: {search_metadata['diagnostic_hint']}")

        add_section(lines, "최저가", [
            f"최적 조합: {combo_text(best)}" if best else None,
            summary.get("recommendation"),
            summary.get("recommendation_explained"),
        ])
        add_section(lines, "왕복 균형 추천", [summary.get("balanced_recommendation"), summary.get("balanced_recommendation_explained")])
        add_section(lines, "목적지별 베스트", [
            (f"{idx}. {item['destination_label']} · {combo_text(best_option).replace(item['destination_label'] + ' · ', '', 1)}" if best_option else f"{idx}. {item['destination_label']} · 결과 없음")
            for idx, item in enumerate(destination_rows[:5], start=1)
            for best_option in [item.get('best_option')]
        ])
        if destination_rows:
            calendar_lines = []
            for item in destination_rows[:5]:
                calendar_lines.append(f"- {item['destination_label']}")
                calendar_rows = item.get("price_calendar", [])
                preview = calendar_rows[:7]
                calendar_lines.extend(f"  {entry['label']}" for entry in preview)
                if len(calendar_rows) > len(preview):
                    calendar_lines.append(f"  … 외 {len(calendar_rows) - len(preview)}일")
            add_section(lines, "목적지별 가격 캘린더", calendar_lines)
        add_section(lines, "전체 상위 조합", [f"{idx}. {combo_text(item)}" for idx, item in enumerate(ranked_combos[:7], start=1)])
        print("\n".join(lines))
        return

    print(json.dumps({
        "status": "success",
        "query": {
            "origin": origin,
            "destinations": destinations,
            "start_date": pretty_date(start_dt),
            "end_date": pretty_date(end_dt),
            "return_offset": args.return_offset,
            "adults": args.adults,
            "cabin": args.cabin,
            "time_preference": time_pref.describe(),
        },
        "summary": summary,
        "results": ranked_combos,
        "matrix": destination_rows,
        "logs": logs,
        "search_metadata": search_metadata,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
