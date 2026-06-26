#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_STORE = SKILL_DIR / "price-alert-rules.json"
KST_LABEL = "Asia/Seoul"
DEFAULT_MESSAGE_TEMPLATE = """[국내선 가격 알림] {label}
- 노선: {route}
- 조건: 성인 {adults}명 · {cabin_label}
- 목표가: {target_price}
- 확인된 최저가: {observed_price}
- 일정: {date_text}{best_destination_line}{airline_line}{time_line}
- 상태: {status_line}"""

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common_cli import airport_label, cabin_label, describe_time_preference_payload, format_price, normalize_airport, parse_date_range_text, parse_flexible_date, pretty_date, time_preference_cli_args, unique_codes


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_store(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "version": 2,
            "timezone": KST_LABEL,
            "updated_at": now_iso(),
            "rules": [],
        }
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("version", 2)
    data.setdefault("timezone", KST_LABEL)
    data.setdefault("rules", [])
    for rule in data["rules"]:
        rule.setdefault("notify", {})
        rule["notify"].setdefault("channel", "stdout")
        rule["notify"].setdefault("dedupe_key", None)
        rule["notify"].setdefault("last_sent_at", None)
        rule["notify"].setdefault("message_template", None)
    return data


def save_store(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = now_iso()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _parse_destinations(args) -> list[str]:
    if args.destinations:
        return unique_codes([normalize_airport(x.strip()) for x in args.destinations.split(",") if x.strip()])
    if args.destination:
        return [normalize_airport(args.destination)]
    raise ValueError("--destination 또는 --destinations 가 필요합니다.")


def canonical_signature(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def make_rule(args) -> dict[str, Any]:
    origin = normalize_airport(args.origin)
    destinations = _parse_destinations(args)
    if args.date_range:
        start_dt, end_dt = parse_date_range_text(args.date_range)
        departure = None
        return_date = None
        date_range = {
            "start_date": pretty_date(start_dt),
            "end_date": pretty_date(end_dt),
        }
    else:
        departure = pretty_date(parse_flexible_date(args.departure))
        return_date = pretty_date(parse_flexible_date(args.return_date)) if args.return_date else None
        date_range = None

    trip_type = "round_trip" if return_date or args.return_offset > 0 else "one_way"
    destination_label = airport_label(destinations[0]) if len(destinations) == 1 else ", ".join(airport_label(code) for code in destinations)
    date_label = f"{date_range['start_date']}~{date_range['end_date']}" if date_range else departure
    label = args.label or f"{airport_label(origin)}→{destination_label} {date_label}"

    time_preference = {
        "time_pref": args.time_pref,
        "depart_after": args.depart_after,
        "return_after": args.return_after,
        "exclude_early_before": args.exclude_early_before,
        "prefer": args.prefer,
    }

    fingerprint_payload = {
        "origin": origin,
        "destinations": destinations,
        "departure": departure,
        "return_date": return_date,
        "date_range": date_range,
        "return_offset": args.return_offset,
        "adults": args.adults,
        "cabin": args.cabin,
        "trip_type": trip_type,
        "target_price_krw": args.target_price,
        "time_preference": time_preference,
    }

    return {
        "id": args.rule_id or f"kdf-{uuid.uuid4().hex[:8]}",
        "enabled": True,
        "label": label,
        "fingerprint": canonical_signature(fingerprint_payload),
        "query": {
            "origin": origin,
            "destination": destinations[0] if len(destinations) == 1 else None,
            "destinations": destinations,
            "departure": departure,
            "return_date": return_date,
            "date_range": date_range,
            "return_offset": args.return_offset,
            "adults": args.adults,
            "cabin": args.cabin,
            "trip_type": trip_type,
            "time_preference": time_preference,
        },
        "target_price_krw": args.target_price,
        "created_at": now_iso(),
        "last_checked_at": None,
        "last_result": None,
        "notify": {
            "channel": "stdout",
            "dedupe_key": None,
            "last_sent_at": None,
            "message_template": args.message_template or None,
        },
        "meta": {
            "source": "price_alerts.py",
            "notes": args.notes or "",
        },
    }


def describe_rule(rule: dict[str, Any]) -> str:
    q = rule["query"]
    destinations = q.get("destinations") or ([q["destination"]] if q.get("destination") else [])
    destination_text = ", ".join(airport_label(code) for code in destinations)
    if q.get("date_range"):
        date_text = f"{q['date_range']['start_date']}~{q['date_range']['end_date']}"
        if q.get("return_offset"):
            date_text += f" (귀국 +{q['return_offset']}일)"
    else:
        date_text = q["departure"]
        if q.get("return_date"):
            date_text += f" ~ {q['return_date']}"
    state = "ON" if rule.get("enabled", True) else "OFF"
    template_flag = "사용자 템플릿" if rule.get("notify", {}).get("message_template") else "기본 템플릿"
    time_pref = q.get("time_preference") or {}
    time_pref_text = describe_time_preference_payload(time_pref)
    time_pref_line = f"\n- 시간 조건: {time_pref_text}" if time_pref_text else ""
    return (
        f"[{state}] {rule['id']} | {rule['label']}\n"
        f"- 노선: {airport_label(q['origin'])} → {destination_text}\n"
        f"- 일정: {date_text}\n"
        f"- 조건: 성인 {q['adults']}명 · {cabin_label(q['cabin'])} · 목표가 {format_price(rule['target_price_krw'])}{time_pref_line}\n"
        f"- 알림: {template_flag} · 마지막 dedupe_key={rule.get('notify', {}).get('dedupe_key') or '없음'}"
    )


def run_search(script_name: str, params: list[str]) -> dict[str, Any]:
    command = [sys.executable, str(SCRIPT_DIR / script_name), *params]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(result.stdout or result.stderr or f"검색 스크립트 실패: {script_name}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"검색 결과를 JSON으로 해석하지 못했습니다: {exc}\n{result.stdout[:800]}") from exc


def check_rule(rule: dict[str, Any]) -> dict[str, Any]:
    q = rule["query"]
    destinations = q.get("destinations") or ([q["destination"]] if q.get("destination") else [])
    common = [
        "--origin", q["origin"],
        "--adults", str(q["adults"]),
        "--cabin", q["cabin"],
    ]
    tp = q.get("time_preference") or {}
    common.extend(time_preference_cli_args(tp))

    if len(destinations) > 1 and q.get("date_range"):
        payload = run_search(
            "search_destination_date_matrix.py",
            [
                *common,
                "--destinations", ",".join(destinations),
                "--start-date", q["date_range"]["start_date"],
                "--end-date", q["date_range"]["end_date"],
                "--return-offset", str(q.get("return_offset", 0)),
            ],
        )
        best = payload.get("summary", {}).get("best_combo")
        matched = bool(best and best.get("price", 0) and best["price"] <= rule["target_price_krw"])
        return {
            "matched": matched,
            "observed_price_krw": best.get("price", 0) if best else 0,
            "best_option": best,
            "search_type": "destination_date_matrix",
            "raw_summary": payload.get("summary"),
        }

    if len(destinations) > 1:
        payload = run_search(
            "search_multi_destination.py",
            [
                *common,
                "--destinations", ",".join(destinations),
                "--departure", q["departure"],
                *(["--return-date", q["return_date"]] if q.get("return_date") else []),
            ],
        )
        best = payload.get("summary", {}).get("best_option")
        matched = bool(best and best.get("cheapest_price", 0) and best["cheapest_price"] <= rule["target_price_krw"])
        return {
            "matched": matched,
            "observed_price_krw": best.get("cheapest_price", 0) if best else 0,
            "best_option": {
                "destination": best.get("destination") if best else None,
                "destination_label": best.get("destination_label") if best else None,
                "price": best.get("cheapest_price", 0) if best else 0,
                "airline": best.get("airline") if best else None,
                "departure_time": best.get("departure_time") if best else None,
                "arrival_time": best.get("arrival_time") if best else None,
                "departure_date": q.get("departure"),
                "return_date": q.get("return_date"),
            },
            "search_type": "multi_destination",
            "raw_summary": payload.get("summary"),
        }

    destination = destinations[0]
    single_common = [*common, "--destination", destination]
    if q.get("date_range"):
        payload = run_search(
            "search_date_range.py",
            [
                *single_common,
                "--start-date", q["date_range"]["start_date"],
                "--end-date", q["date_range"]["end_date"],
                "--return-offset", str(q.get("return_offset", 0)),
            ],
        )
        best = payload.get("summary", {}).get("best_date")
        matched = bool(best and best.get("price", 0) and best["price"] <= rule["target_price_krw"])
        return {
            "matched": matched,
            "observed_price_krw": best.get("price", 0) if best else 0,
            "best_option": best,
            "search_type": "date_range",
            "raw_summary": payload.get("summary"),
        }

    payload = run_search(
        "search_domestic.py",
        [
            *single_common,
            "--departure", q["departure"],
            *(["--return-date", q["return_date"]] if q.get("return_date") else []),
        ],
    )
    best = payload.get("cheapest")
    matched = bool(best and best.get("price", 0) and best["price"] <= rule["target_price_krw"])
    return {
        "matched": matched,
        "observed_price_krw": best.get("price", 0) if best else 0,
        "best_option": best,
        "search_type": "single_date",
        "raw_summary": payload.get("summary"),
    }


def _safe_format(template: str, context: dict[str, Any]) -> str:
    class SafeDict(dict):
        def __missing__(self, key):
            return ""

    return template.format_map(SafeDict({k: "" if v is None else v for k, v in context.items()})).strip()


def build_notification_context(rule: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    q = rule["query"]
    best = result.get("best_option") or {}
    destinations = q.get("destinations") or ([q["destination"]] if q.get("destination") else [])
    route = f"{airport_label(q['origin'])} → {', '.join(airport_label(code) for code in destinations)}"
    observed = result.get("observed_price_krw", 0)
    target = rule["target_price_krw"]
    diff = target - observed
    departure_date = best.get("departure_date") or q.get("departure") or (q.get("date_range") or {}).get("start_date")
    return_date = best.get("return_date") or q.get("return_date")
    if q.get("date_range"):
        date_text = f"최저가 날짜 {departure_date}"
        if return_date:
            date_text += f" ~ {return_date}"
        else:
            date_text += f" (탐색 범위 {q['date_range']['start_date']}~{q['date_range']['end_date']})"
    else:
        date_text = departure_date or ""
        if return_date:
            date_text += f" ~ {return_date}"
    best_destination_label = best.get("destination_label") or airport_label(best.get("destination")) if best.get("destination") else ""
    status_line = f"목표가 충족 ({diff:,}원 여유)" if diff >= 0 else f"목표가 초과 ({abs(diff):,}원 초과)"
    best_destination_line = f"\n- 최적 목적지: {best_destination_label}" if best_destination_label else ""
    airline_line = f"\n- 항공사: {best.get('airline')}" if best.get("airline") else ""
    time_line = ""
    if best.get("departure_time") and best.get("arrival_time"):
        time_line = f"\n- 시간: {best['departure_time']} → {best['arrival_time']}"
    return {
        "rule_id": rule["id"],
        "label": rule["label"],
        "route": route,
        "origin": q["origin"],
        "origin_label": airport_label(q["origin"]),
        "destinations": ",".join(destinations),
        "destinations_label": ", ".join(airport_label(code) for code in destinations),
        "best_destination": best.get("destination") or "",
        "best_destination_label": best_destination_label,
        "adults": q["adults"],
        "cabin": q["cabin"],
        "cabin_label": cabin_label(q["cabin"]),
        "target_price": format_price(target),
        "target_price_krw": target,
        "observed_price": format_price(observed),
        "observed_price_krw": observed,
        "difference_krw": diff,
        "departure_date": departure_date or "",
        "return_date": return_date or "",
        "date_text": date_text,
        "airline": best.get("airline") or "",
        "departure_time": best.get("departure_time") or "",
        "arrival_time": best.get("arrival_time") or "",
        "search_type": result.get("search_type") or "",
        "status_line": status_line,
        "best_destination_line": best_destination_line,
        "airline_line": airline_line,
        "time_line": time_line,
    }


def compute_dedupe_key(rule: dict[str, Any], result: dict[str, Any]) -> str:
    best = result.get("best_option") or {}
    payload = {
        "rule_id": rule["id"],
        "search_type": result.get("search_type"),
        "observed_price_krw": result.get("observed_price_krw", 0),
        "destination": best.get("destination"),
        "departure_date": best.get("departure_date"),
        "return_date": best.get("return_date"),
        "airline": best.get("airline"),
        "departure_time": best.get("departure_time"),
        "arrival_time": best.get("arrival_time"),
    }
    return canonical_signature(payload)


def build_notification(rule: dict[str, Any], result: dict[str, Any]) -> str:
    template = rule.get("notify", {}).get("message_template") or DEFAULT_MESSAGE_TEMPLATE
    context = build_notification_context(rule, result)
    return _safe_format(template, context)


def command_add(args) -> int:
    store_path = Path(args.store)
    data = load_store(store_path)
    rule = make_rule(args)
    if any(item["id"] == rule["id"] for item in data["rules"]):
        raise SystemExit(f"이미 같은 id 규칙이 있습니다: {rule['id']}")
    duplicate = next((item for item in data["rules"] if item.get("fingerprint") == rule["fingerprint"]), None)
    if duplicate:
        raise SystemExit(f"중복 규칙입니다. 기존 규칙 id={duplicate['id']} label={duplicate['label']}")
    data["rules"].append(rule)
    save_store(store_path, data)
    print("규칙 저장 완료")
    print(describe_rule(rule))
    print(f"저장 파일: {store_path}")
    return 0


def command_list(args) -> int:
    data = load_store(Path(args.store))
    rules = data.get("rules", [])
    if not rules:
        print("저장된 가격 감시 규칙이 없습니다.")
        return 0
    for idx, rule in enumerate(rules, start=1):
        print(f"{idx}. {describe_rule(rule)}")
    return 0


def command_check(args) -> int:
    store_path = Path(args.store)
    data = load_store(store_path)
    matched_messages: list[str] = []
    checked = 0
    failures: list[str] = []
    suppressed = 0

    for rule in data.get("rules", []):
        if not rule.get("enabled", True):
            continue
        if args.rule_id and rule["id"] != args.rule_id:
            continue
        checked += 1
        try:
            result = check_rule(rule)
            rule["last_checked_at"] = now_iso()
            rule["last_result"] = result
            if result["matched"]:
                dedupe_key = compute_dedupe_key(rule, result)
                if args.no_dedupe or rule.get("notify", {}).get("dedupe_key") != dedupe_key:
                    matched_messages.append(build_notification(rule, result))
                    rule.setdefault("notify", {})["dedupe_key"] = dedupe_key
                    rule["notify"]["last_sent_at"] = now_iso()
                else:
                    suppressed += 1
        except Exception as exc:
            failures.append(f"{rule['id']}: {exc}")
            rule["last_checked_at"] = now_iso()
            rule["last_result"] = {"matched": False, "error": str(exc)}

    save_store(store_path, data)

    if failures:
        print("[점검 오류]", file=sys.stderr)
        for item in failures:
            print(f"- {item}", file=sys.stderr)

    if matched_messages:
        print("\n\n".join(matched_messages))
        if suppressed:
            print(f"\n[dedupe] 동일 알림 {suppressed}건은 재전송하지 않았습니다.", file=sys.stderr)
        return 0

    if checked == 0:
        print("점검할 활성 규칙이 없습니다.")
    else:
        msg = f"점검 완료: {checked}개 규칙 확인, 목표가 충족 알림 없음"
        if suppressed:
            msg += f" (중복 억제 {suppressed}건)"
        print(msg)
    return 0 if not failures else 1


def command_remove(args) -> int:
    store_path = Path(args.store)
    data = load_store(store_path)
    before = len(data.get("rules", []))
    data["rules"] = [rule for rule in data.get("rules", []) if rule["id"] != args.rule_id]
    after = len(data["rules"])
    if before == after:
        raise SystemExit(f"삭제할 규칙을 찾지 못했습니다: {args.rule_id}")
    save_store(store_path, data)
    print(f"규칙 삭제 완료: {args.rule_id}")
    return 0


def command_render(args) -> int:
    data = load_store(Path(args.store))
    rule = next((item for item in data.get("rules", []) if item["id"] == args.rule_id), None)
    if not rule:
        raise SystemExit(f"규칙을 찾지 못했습니다: {args.rule_id}")
    if not rule.get("last_result"):
        raise SystemExit("아직 last_result 가 없습니다. 먼저 check 를 실행하세요.")
    print(build_notification(rule, rule["last_result"]))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="대한민국 국내선 가격 감시 규칙 저장/점검 도구")
    parser.add_argument("--store", default=str(DEFAULT_STORE), help="규칙 JSON 저장 파일 경로")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="감시 규칙 추가")
    add.add_argument("--rule-id", help="직접 지정할 규칙 ID")
    add.add_argument("--label", help="사람이 보기 쉬운 규칙 이름")
    add.add_argument("--origin", required=True)
    add_dest = add.add_mutually_exclusive_group(required=True)
    add_dest.add_argument("--destination", help="단일 목적지")
    add_dest.add_argument("--destinations", help="쉼표 구분 다중 목적지")
    add.add_argument("--departure", help="단일 출발일")
    add.add_argument("--return-date", help="왕복 귀국일")
    add.add_argument("--date-range", help="날짜 범위. 예: 내일부터 3일, 2026-03-20~2026-03-22")
    add.add_argument("--return-offset", type=int, default=0, help="날짜 범위 감시에서 출발일 기준 귀국일 오프셋")
    add.add_argument("--adults", type=int, default=1)
    add.add_argument("--cabin", default="ECONOMY", choices=["ECONOMY", "BUSINESS", "FIRST"])
    add.add_argument("--target-price", type=int, required=True, help="목표가(원)")
    add.add_argument("--time-pref", help="자연어 시간 조건. 예: 저녁, 출발 10시 이후, 복귀 18시 이후, 늦은 시간 선호")
    add.add_argument("--depart-after", help="출발 N시 이후. 예: 10, 10:30")
    add.add_argument("--return-after", help="복귀 N시 이후. 예: 18, 18:30")
    add.add_argument("--exclude-early-before", help="이 시간 이전 출발 제외. 예: 8, 08:30")
    add.add_argument("--prefer", choices=["late", "morning", "afternoon", "evening"], help="시간대 선호 추천")
    add.add_argument("--notes", help="메모")
    add.add_argument("--message-template", help="알림 메시지 포맷. 예: '[특가] {label} {observed_price} / {date_text}'")

    sub.add_parser("list", help="저장 규칙 목록")

    check = sub.add_parser("check", help="저장 규칙 점검")
    check.add_argument("--rule-id", help="특정 규칙만 점검")
    check.add_argument("--no-dedupe", action="store_true", help="중복 알림 억제를 끄고 이번 점검에서는 항상 출력")

    remove = sub.add_parser("remove", help="규칙 삭제")
    remove.add_argument("--rule-id", required=True)

    render = sub.add_parser("render", help="마지막 결과를 현재 템플릿으로 미리보기")
    render.add_argument("--rule-id", required=True)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "add":
        if not args.date_range and not args.departure:
            raise SystemExit("add 에서는 --departure 또는 --date-range 가 필요합니다.")
        return command_add(args)
    if args.command == "list":
        return command_list(args)
    if args.command == "check":
        return command_check(args)
    if args.command == "remove":
        return command_remove(args)
    if args.command == "render":
        return command_render(args)
    raise SystemExit("알 수 없는 명령입니다.")


if __name__ == "__main__":
    raise SystemExit(main())
