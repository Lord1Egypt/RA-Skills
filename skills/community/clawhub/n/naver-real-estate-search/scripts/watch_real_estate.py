from __future__ import annotations

import argparse
import json
import time
import uuid
from pathlib import Path
from typing import Any

from search_real_estate import WATCH_STATE_FILE, PriceConverter, run_query

SCHEMA_VERSION = 2


def _load_rules() -> dict[str, Any]:
    if WATCH_STATE_FILE.exists():
        data = json.loads(WATCH_STATE_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "rules" in data:
            data.setdefault("schema_version", SCHEMA_VERSION)
            data.setdefault("last_checked_at", None)
            data.setdefault("events", [])
            data.setdefault("last_seen", {})
            return data
    return {"schema_version": SCHEMA_VERSION, "last_checked_at": None, "rules": [], "events": [], "last_seen": {}}


def _save_rules(data: dict[str, Any]) -> None:
    WATCH_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    WATCH_STATE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _fmt_price(value: int | None) -> str:
    return PriceConverter.to_string(value) if value else "-"


def _article_key(item: dict[str, Any]) -> str:
    return str(item.get("article_key") or f"{item.get('complex_id', '')}:{item.get('매물ID', '')}")


def _normalize_rule(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "id": getattr(args, "rule_id", None) or f"rule-{uuid.uuid4().hex[:10]}",
        "name": args.name,
        "query": args.query,
        "complex_id": args.complex_id,
        "url": args.url,
        "trade_types": [token.strip() for token in str(args.trade_types or "").split(",") if token.strip()],
        "target_max_price": args.target_max_price,
        "pages": args.pages,
        "limit": args.limit,
        "candidate_limit": args.candidate_limit,
        "min_pyeong": args.min_pyeong,
        "max_pyeong": args.max_pyeong,
        "notify_on_new": bool(args.notify_on_new),
        "notify_on_price_drop": bool(args.notify_on_price_drop),
        "enabled": True,
        "created_at": int(time.time()),
        "updated_at": int(time.time()),
        "notes": getattr(args, "notes", None),
    }


def add_rule(args: argparse.Namespace) -> int:
    data = _load_rules()
    rule = _normalize_rule(args)
    data.setdefault("rules", []).append(rule)
    _save_rules(data)
    print(json.dumps({"saved": True, "rule": rule}, ensure_ascii=False, indent=2))
    return 0


def list_rules() -> int:
    print(json.dumps(_load_rules(), ensure_ascii=False, indent=2))
    return 0


def _make_match(rule: dict[str, Any], item: dict[str, Any], *, event_type: str, previous: dict[str, Any] | None = None) -> dict[str, Any]:
    price = PriceConverter.to_int(item.get("매매가") or item.get("보증금") or "0")
    return {
        "event_type": event_type,
        "article_key": _article_key(item),
        "price": price,
        "price_text": _fmt_price(price),
        "complex_id": item.get("complex_id"),
        "complex_name": item.get("단지명"),
        "article_url": item.get("매물URL"),
        "area_pyeong": item.get("면적(평)"),
        "trade_type": item.get("거래유형"),
        "floor_direction": item.get("층/방향"),
        "feature": item.get("특징"),
        "previous_price": previous.get("price") if previous else None,
        "previous_price_text": _fmt_price(previous.get("price")) if previous and previous.get("price") else None,
        "target_max_price": rule.get("target_max_price"),
        "target_max_price_text": _fmt_price(rule.get("target_max_price")),
        "detected_at": int(time.time()),
    }


def _build_alert_lines(alerts: list[dict[str, Any]], *, max_matches_per_rule: int = 3) -> list[str]:
    lines = []
    for row in alerts:
        rule = row.get("rule") or {}
        matched = row.get("matched") or []
        snapshot = row.get("snapshot") or {}
        complex_info = snapshot.get("complex_info") or {}
        label = rule.get("name") or rule.get("id") or "이름없는 규칙"
        header = f"- {label}: {row.get('matched_count', 0)}건"
        if complex_info.get("name"):
            header += f" | {complex_info.get('name')}"
        if row.get("error"):
            header += f" | 오류: {row['error']}"
        lines.append(header)
        for item in matched[:max_matches_per_rule]:
            badges = []
            if item.get("event_type") == "new_listing":
                badges.append("신규")
            elif item.get("event_type") == "price_drop":
                badges.append("가격하락")
            elif item.get("event_type") == "target_hit":
                badges.append("목표가도달")
            if item.get("previous_price_text"):
                badges.append(f"이전 {item['previous_price_text']}")
            badge_text = f" ({', '.join(badges)})" if badges else ""
            lines.append(f"  · {item.get('complex_name')} {item.get('trade_type')} {item.get('price_text')} / {item.get('area_pyeong')}평{badge_text}")
            if item.get("article_url"):
                lines.append(f"    - {item['article_url']}")
    return lines


def _build_message_preview(alerts: list[dict[str, Any]], *, checked_at: int) -> str:
    total = sum(int(row.get("matched_count") or 0) for row in alerts)
    lines = [f"부동산 감시 점검 결과: {total}건 알림", f"checked_at={checked_at}"]
    lines.extend(_build_alert_lines(alerts))
    return "\n".join(lines)


def _stdout_payload(alerts: list[dict[str, Any]], *, checked_at: int) -> dict[str, Any]:
    preview = _build_message_preview(alerts, checked_at=checked_at)
    return {
        "kind": "naver-real-estate-watch-check",
        "schema_version": SCHEMA_VERSION,
        "checked_at": checked_at,
        "alert_count": sum(int(row.get("matched_count") or 0) for row in alerts),
        "alerts": alerts,
        "message_preview": preview,
        "summary": {
            "rule_count": len(alerts),
            "rules_with_matches": sum(1 for row in alerts if int(row.get("matched_count") or 0) > 0),
            "rules_with_errors": sum(1 for row in alerts if row.get("error")),
        },
    }


def check_rules(args: argparse.Namespace) -> int:
    data = _load_rules()
    last_seen = data.setdefault("last_seen", {})
    checked_at = int(time.time())
    alerts = []
    new_events = []

    for rule in data.get("rules", []):
        if rule.get("enabled") is False:
            continue
        try:
            payload = run_query(
                query=rule.get("query"),
                complex_id=rule.get("complex_id"),
                url=rule.get("url"),
                trade_types=rule.get("trade_types") or [],
                pages=max(1, int(rule.get("pages") or 1)),
                limit=max(1, int(rule.get("limit") or 10)),
                candidate_limit=max(1, int(rule.get("candidate_limit") or 1)),
                min_pyeong=rule.get("min_pyeong"),
                max_pyeong=rule.get("max_pyeong"),
                compare=False,
            )
        except Exception as exc:
            alerts.append({
                "rule": rule,
                "matched": [],
                "matched_count": 0,
                "error": str(exc),
                "snapshot": None,
            })
            continue
        threshold = rule.get("target_max_price")
        matches = []
        for item in payload.get("items", []):
            price = PriceConverter.to_int(item.get("매매가") or item.get("보증금") or "0")
            article_key = _article_key(item)
            prev = last_seen.get(article_key)
            is_new = prev is None
            is_price_drop = bool(prev and prev.get("price") and price and price < prev.get("price"))
            threshold_hit = bool(threshold and price and price <= threshold)
            emit = False
            event_type = None
            if threshold_hit:
                emit = True
                event_type = "target_hit"
            if is_new and rule.get("notify_on_new"):
                emit = True
                event_type = event_type or "new_listing"
            if is_price_drop and rule.get("notify_on_price_drop"):
                emit = True
                event_type = event_type or "price_drop"
            if emit:
                match = _make_match(rule, item, event_type=event_type or "matched", previous=prev)
                matches.append(match)
                dedupe_key = f"{rule.get('id')}::{event_type}::{article_key}::{price}"
                known_event_keys = {e.get('dedupe_key') for e in data.get('events', [])[-500:]}
                if dedupe_key not in known_event_keys:
                    event = {"rule_id": rule.get("id"), "rule_name": rule.get("name"), "dedupe_key": dedupe_key, **match}
                    new_events.append(event)
            last_seen[article_key] = {
                "rule_id": rule.get("id"),
                "price": price,
                "last_seen_at": checked_at,
                "trade_type": item.get("거래유형"),
                "complex_name": item.get("단지명"),
                "article_url": item.get("매물URL"),
            }
        alerts.append({
            "rule": rule,
            "matched": matches,
            "matched_count": len(matches),
            "snapshot": {
                "selected_complex_id": payload.get("selected_complex_id"),
                "complex_info": payload.get("complex_info"),
                "market_summary": payload.get("market_summary"),
                "meta": payload.get("meta"),
            },
        })

    data["last_checked_at"] = checked_at
    data.setdefault("events", []).extend(new_events)
    data["events"] = data["events"][-1000:]
    data["last_seen"] = last_seen
    _save_rules(data)

    payload = _stdout_payload(alerts, checked_at=checked_at)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif args.preview:
        print(payload["message_preview"])
    else:
        print(payload["message_preview"])
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="네이버 부동산 가격 감시/새 매물 감지")
    sub = p.add_subparsers(dest="cmd", required=True)

    add_p = sub.add_parser("add")
    add_p.add_argument("--name", required=True)
    add_p.add_argument("--query")
    add_p.add_argument("--complex-id")
    add_p.add_argument("--url")
    add_p.add_argument("--trade-types", default="")
    add_p.add_argument("--target-max-price", type=int, help="정수 가격 기준. 예: 950000000")
    add_p.add_argument("--pages", type=int, default=1)
    add_p.add_argument("--limit", type=int, default=10)
    add_p.add_argument("--candidate-limit", type=int, default=1)
    add_p.add_argument("--min-pyeong", type=float)
    add_p.add_argument("--max-pyeong", type=float)
    add_p.add_argument("--notify-on-new", action="store_true")
    add_p.add_argument("--notify-on-price-drop", action="store_true")
    add_p.add_argument("--notes")

    sub.add_parser("list")
    check_p = sub.add_parser("check")
    check_p.add_argument("--json", action="store_true")
    check_p.add_argument("--preview", action="store_true", help="사람이 읽기 쉬운 preview만 출력")
    return p


def main() -> int:
    args = build_parser().parse_args()
    if args.cmd == "add":
        return add_rule(args)
    if args.cmd == "list":
        return list_rules()
    if args.cmd == "check":
        return check_rules(args)
    raise SystemExit(2)


if __name__ == "__main__":
    raise SystemExit(main())
