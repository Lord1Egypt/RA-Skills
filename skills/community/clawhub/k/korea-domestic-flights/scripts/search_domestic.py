#!/usr/bin/env python3
import argparse
import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common_cli import (
    add_section,
    airport_label,
    build_best_option_reasons,
    cabin_label,
    explain_recommendation,
    filter_and_rank_by_time_preference,
    format_price,
    format_time_or_fallback,
    join_nonempty,
    normalize_airport,
    parse_flexible_date,
    parse_time_preference_args,
    pretty_date,
    recommendation_line,
    time_preference_recommendation,
)


def normalize_result(item):
    if is_dataclass(item):
        data = asdict(item)
    elif hasattr(item, "__dict__"):
        data = dict(item.__dict__)
    else:
        data = {"value": str(item)}

    return {
        "airline": data.get("airline", ""),
        "price": data.get("price", 0),
        "departure_time": data.get("departure_time", ""),
        "arrival_time": data.get("arrival_time", ""),
        "stops": data.get("stops", 0),
        "source": data.get("source", ""),
        "return_departure_time": data.get("return_departure_time", ""),
        "return_arrival_time": data.get("return_arrival_time", ""),
        "return_stops": data.get("return_stops", 0),
        "is_round_trip": data.get("is_round_trip", False),
        "outbound_price": data.get("outbound_price", 0),
        "return_price": data.get("return_price", 0),
        "return_airline": data.get("return_airline", ""),
        "confidence": data.get("confidence", 0),
        "extraction_source": data.get("extraction_source", ""),
    }


def option_text(item):
    airline = item.get('airline', '')
    if item.get("is_round_trip"):
        return join_nonempty([
            f"{airline}/{item.get('return_airline') or airline}" if airline else None,
            f"총 {format_price(item.get('price', 0))}",
            f"가는편 {join_nonempty([format_time_or_fallback(item.get('departure_time')), item.get('arrival_time')], '→')}",
            f"오는편 {join_nonempty([format_time_or_fallback(item.get('return_departure_time')), item.get('return_arrival_time')], '→')}",
        ])
    return join_nonempty([
        airline or None,
        format_price(item.get('price', 0)),
        join_nonempty([format_time_or_fallback(item.get('departure_time')), item.get('arrival_time')], '→'),
    ])


def build_summary(query, normalized, preferred, time_pref):
    route = f"{airport_label(query['origin'])} → {airport_label(query['destination'])}"
    trip_type = "왕복" if query.get("return_date") else "편도"

    if not normalized:
        return {
            "headline": f"{route} {trip_type} 검색 결과가 없습니다.",
            "route": route,
            "trip_type": trip_type,
            "cheapest_text": None,
            "top_options": [],
            "recommendation": None,
            "time_preference_recommendation": None,
            "preferred_option": preferred,
        }

    cheapest = normalized[0]
    second_price = normalized[1].get("price", 0) if len(normalized) > 1 else None
    return {
        "headline": f"{route} {trip_type} 최저가 {format_price(cheapest.get('price', 0))}",
        "route": route,
        "trip_type": trip_type,
        "cheapest_text": option_text(cheapest),
        "top_options": [option_text(item) for item in normalized[:3]],
        "recommendation": recommendation_line(option_text(cheapest), cheapest.get("price", 0), second_price),
        "recommendation_explained": explain_recommendation(
            option_text(cheapest),
            int(cheapest.get("price", 0) or 0),
            second_price,
            build_best_option_reasons(cheapest, second_price, time_pref),
        ),
        "time_preference_recommendation": time_preference_recommendation(preferred, cheapest, time_pref),
        "preferred_option": preferred,
    }


def format_human(summary, query, count, time_pref):
    lines = [summary["headline"]]
    meta = [f"조건: 성인 {query['adults']}명 · {cabin_label(query['cabin'])} · 결과 {count}건"]
    if query.get("return_date"):
        meta.append(f"일정: {query['departure']} ~ {query['return_date']}")
    else:
        meta.append(f"일정: {query['departure']}")
    if time_pref.describe():
        meta.append(f"시간 조건: {time_pref.describe()}")
    lines.extend(meta)

    add_section(lines, "최저가", [summary.get("cheapest_text"), summary.get("recommendation"), summary.get("recommendation_explained")])
    add_section(lines, "시간대 추천", [summary.get("time_preference_recommendation")])
    add_section(lines, "상위 옵션", [f"{idx}. {item}" for idx, item in enumerate(summary.get("top_options", []), start=1)])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Search Korean domestic flights")
    parser.add_argument("--origin", required=True, help="예: GMP 또는 김포")
    parser.add_argument("--destination", required=True, help="예: CJU 또는 제주")
    parser.add_argument("--departure", required=True, help="예: 2026-03-25, 20260325, 내일")
    parser.add_argument("--return-date", dest="return_date", help="예: 2026-03-28, 모레")
    parser.add_argument("--adults", type=int, default=1)
    parser.add_argument("--cabin", default="ECONOMY", choices=["ECONOMY", "BUSINESS", "FIRST"])
    parser.add_argument("--max-results", type=int, default=20)
    parser.add_argument("--time-pref", help="예: 오전, 저녁, 출발 10시 이후, 복귀 18시 이후, 너무 이른 비행 제외 8시")
    parser.add_argument("--depart-after", help="출발 N시 이후. 예: 10, 10:30")
    parser.add_argument("--return-after", help="복귀 N시 이후. 예: 18, 18:30")
    parser.add_argument("--exclude-early-before", help="이 시간 이전 출발 제외. 예: 8, 08:30")
    parser.add_argument("--prefer", choices=["late", "morning", "afternoon", "evening"], help="시간대 선호 추천")
    parser.add_argument("--human", action="store_true")
    args = parser.parse_args()

    workspace = Path(__file__).resolve().parents[3]
    repo_path = workspace / "tmp" / "Scraping-flight-information"

    if not repo_path.exists():
        print(json.dumps({"status": "error", "message": "Source repository clone not found.", "expected": str(repo_path)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    sys.path.insert(0, str(repo_path))

    try:
        from scraping.searcher import FlightSearcher
    except Exception as exc:
        print(json.dumps({"status": "error", "message": "Failed to import flight searcher.", "details": str(exc), "repo": str(repo_path)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    try:
        origin = normalize_airport(args.origin)
        destination = normalize_airport(args.destination)
        departure = pretty_date(parse_flexible_date(args.departure))
        return_date = pretty_date(parse_flexible_date(args.return_date)) if args.return_date else None
    except ValueError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)

    time_pref = parse_time_preference_args(args)

    logs = []

    def progress(msg):
        logs.append(str(msg))

    query = {
        "origin": origin,
        "destination": destination,
        "departure": departure,
        "return_date": return_date,
        "adults": args.adults,
        "cabin": args.cabin,
        "max_results": args.max_results,
        "time_preference": time_pref.describe(),
    }

    searcher = FlightSearcher()
    try:
        results = searcher.search(
            origin=query["origin"],
            destination=query["destination"],
            departure_date=query["departure"],
            return_date=query["return_date"],
            adults=query["adults"],
            cabin_class=query["cabin"],
            max_results=query["max_results"],
            progress_callback=progress,
            background_mode=False,
        )

        all_results = [normalize_result(item) for item in results]
        normalized, preferred_ranked = filter_and_rank_by_time_preference(all_results, time_pref)
        preferred = preferred_ranked[0] if preferred_ranked else None
        cheapest = normalized[0] if normalized else None
        summary = build_summary(query, normalized, preferred, time_pref)

        if args.human:
            print(format_human(summary, query, len(normalized), time_pref))
            return

        print(json.dumps({
            "status": "success",
            "query": query,
            "count": len(normalized),
            "summary": summary,
            "cheapest": cheapest,
            "preferred_option": preferred,
            "results": normalized,
            "all_results_before_time_filter": all_results,
            "logs": logs,
        }, ensure_ascii=False, indent=2))
    finally:
        try:
            searcher.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
