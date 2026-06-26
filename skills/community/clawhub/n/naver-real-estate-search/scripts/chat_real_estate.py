from __future__ import annotations

import argparse
import json
from typing import Any

from search_real_estate import PriceConverter, run_query, search_complex_candidates


def _fmt_price(value: int | None) -> str:
    return PriceConverter.to_string(value) if value else "-"


def _pick_headline(meta: dict[str, Any], trade_type: str) -> str:
    count = int(meta.get("count") or 0)
    if count == 0:
        return f"{trade_type} 매물이 거의 안 잡힙니다."
    if count <= 3:
        return f"{trade_type} 매물이 많지는 않지만 확인 가능한 건은 있습니다."
    if count <= 10:
        return f"{trade_type} 매물이 어느 정도 보입니다."
    return f"{trade_type} 매물이 비교적 넉넉하게 잡힙니다."


def _trend_line(meta: dict[str, Any]) -> str:
    min_price = meta.get("min_price")
    avg_price = meta.get("avg_price")
    max_price = meta.get("max_price")
    if not (min_price and avg_price and max_price):
        return "가격대 해석용 표본은 아직 제한적입니다."
    spread = max_price - min_price
    if spread <= max(1, avg_price * 0.05):
        return "가격 분산이 크지 않아 호가대가 비교적 촘촘합니다."
    if spread >= max(1, avg_price * 0.15):
        return "호가 폭이 꽤 넓어서 같은 단지 안에서도 조건 차이가 크게 보입니다."
    return "호가 차이는 있으나 극단적으로 벌어지지는 않습니다."


def _representative_lines(items: list[dict[str, Any]], max_items: int = 3) -> list[str]:
    lines: list[str] = []
    for row in items[:max_items]:
        price = row.get("매매가") or row.get("보증금") or "-"
        if row.get("거래유형") == "월세" and row.get("월세"):
            price = f"{price}/{row.get('월세')}"
        parts = [f"{price}", f"{row.get('면적(평)', 0)}평", row.get("층/방향", "-") or "-"]
        lines.append(f"  · 대표 매물: {', '.join(parts)}")
        if row.get("특징"):
            lines.append(f"    - 포인트: {row['특징']}")
        if row.get("매물URL"):
            lines.append(f"    - 링크: {row['매물URL']}")
    return lines


def brief_single(payload: dict[str, Any]) -> str:
    info = payload.get("complex_info") or {}
    parsed = payload.get("parsed") or {}
    lines = [f"{info.get('name', payload.get('selected_complex_id'))} 브리핑"]
    if info.get("address"):
        lines.append(f"- 위치: {info['address']}")
    filters = []
    if payload.get("trade_types"):
        filters.append("거래유형 " + ", ".join(payload["trade_types"]))
    if parsed.get("min_pyeong") or parsed.get("max_pyeong"):
        filters.append(f"평형 {parsed.get('min_pyeong', '-')}~{parsed.get('max_pyeong', '-')}평")
    if filters:
        lines.append(f"- 필터: {' / '.join(filters)}")
    summary = payload.get("market_summary") or {}
    if not summary:
        lines.append("- 조건에 맞는 매물이 아직 잡히지 않았습니다.")
        return "\n".join(lines)
    for trade_type, meta in summary.items():
        lines.append(f"- {trade_type}: {meta.get('count', 0)}건")
        lines.append(f"  · {_pick_headline(meta, trade_type)}")
        lines.append(f"  · 가격대: 최저 {_fmt_price(meta.get('min_price'))} / 평균 {_fmt_price(meta.get('avg_price'))} / 중앙값 {_fmt_price(meta.get('median_price'))} / 최고 {_fmt_price(meta.get('max_price'))}")
        lines.append(f"  · 해석: {_trend_line(meta)}")
        area_rows = meta.get("area_summary") or []
        if area_rows:
            head = area_rows[0]
            lines.append(f"  · 동일 평형 대표: {head.get('area_key')} {head.get('count')}건, 평균 {_fmt_price(head.get('avg_price'))}")
    lines.extend(_representative_lines(payload.get("items", [])))
    return "\n".join(lines)


def brief_compare(payload: dict[str, Any]) -> str:
    results = payload.get("results") or []
    insights = payload.get("compare_insights") or {}
    lines = ["단지 비교 브리핑"]
    for result in results:
        info = result.get("complex_info") or {}
        name = info.get("name", result.get("complex_id"))
        address = info.get("address") or "-"
        lines.append(f"- {name} ({address})")
        summary = result.get("market_summary") or {}
        if not summary:
            lines.append("  · 조건에 맞는 매물이 거의 안 보입니다.")
            continue
        for trade_type, meta in summary.items():
            lines.append(f"  · {trade_type}: {meta.get('count', 0)}건 / 최저 {_fmt_price(meta.get('min_price'))} / 평균 {_fmt_price(meta.get('avg_price'))} / 중앙값 {_fmt_price(meta.get('median_price'))} / 최고 {_fmt_price(meta.get('max_price'))}")
            area_rows = meta.get("area_summary") or []
            if area_rows:
                head = area_rows[0]
                lines.append(f"    - 대표 동일 평형: {head.get('area_key')} {head.get('count')}건 / 평균 {_fmt_price(head.get('avg_price'))}")
    for trade_type, meta in (insights.get("trade") or {}).items():
        lines.append(f"- 종합 해석 ({trade_type}): {meta['cheapest']['name']} 쪽 평균이 가장 낮고 {meta['most_expensive']['name']} 쪽이 가장 높습니다. 전체 평균 차이는 {_fmt_price(meta['gap'])} 정도입니다.")
    for trade_type, area_rows in (insights.get("same_area") or {}).items():
        if not area_rows:
            continue
        head = area_rows[0]
        lines.append(f"- 동일 평형 해석 ({trade_type} {head['area_key']}): {head['cheapest']['name']} 쪽이 더 낮고 {head['most_expensive']['name']} 쪽이 더 높습니다. 같은 평형 기준 차이는 {_fmt_price(head['gap'])} 정도입니다.")
    if payload.get("meta", {}).get("rate_limited"):
        lines.append("- 참고: 현재 네이버 요청 제한이 감지돼 direct URL/complex ID 기반 조회가 더 안정적일 수 있습니다.")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="네이버 부동산 채팅형 브리핑 래퍼")
    p.add_argument("--query", help="자연어 질의")
    p.add_argument("--complex-id")
    p.add_argument("--url")
    p.add_argument("--trade-types", default="")
    p.add_argument("--pages", type=int, default=1)
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--candidate-limit", type=int, default=3)
    p.add_argument("--min-pyeong", type=float)
    p.add_argument("--max-pyeong", type=float)
    p.add_argument("--list-candidates", action="store_true")
    p.add_argument("--compare", action="store_true")
    p.add_argument("--json", action="store_true")
    return p


def main() -> int:
    args = build_parser().parse_args()
    if args.list_candidates:
        if not args.query:
            raise SystemExit("--list-candidates 는 --query 와 함께 사용하세요.")
        candidates = search_complex_candidates(args.query, candidate_limit=max(1, args.candidate_limit))
        if args.json:
            print(json.dumps(candidates, ensure_ascii=False, indent=2))
        else:
            lines = ["후보 단지"]
            for idx, row in enumerate(candidates, start=1):
                lines.append(f"- {idx}. {row.get('name')} | {row.get('address') or '-'} | ID {row.get('complex_id')} | score {row.get('match_score', '-')} | source {row.get('source', '-')}")
            print("\n".join(lines))
        return 0

    trade_types = [token.strip() for token in str(args.trade_types).split(",") if token.strip()]
    payload = run_query(
        query=args.query,
        complex_id=args.complex_id,
        url=args.url,
        trade_types=trade_types,
        pages=max(1, args.pages),
        limit=max(1, args.limit),
        candidate_limit=max(1, args.candidate_limit),
        min_pyeong=args.min_pyeong,
        max_pyeong=args.max_pyeong,
        compare=bool(args.compare),
    )
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(brief_compare(payload) if payload.get("compare_mode") else brief_single(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
