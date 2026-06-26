from __future__ import annotations

import argparse
import getpass
import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from automation_plans import (
    build_integration_bundle,
    parse_automation_request,
    plan_to_dict,
    render_integration_bundle_text,
    render_plan_text,
)
from briefing_templates import build_combined_payload, render_combined_json, render_combined_text, supported_templates
from config_store import get_runtime_credentials, set_credentials
from group_store import create_group, get_group, list_groups, remove_group, update_group
from naver_api import fetch_news
from query_utils import build_intent
from watch_store import add_rule, get_rule, list_rules, mark_seen, remove_rule


MISSING_CREDENTIALS_ERROR = "네이버 API 자격증명이 설정되지 않았습니다."
DEFAULT_TEST_QUERY = "최근 1일 반도체 뉴스"
ANNOUNCE_PREVIEW_LIMIT = 10


def _strip_html(value: str) -> str:
    text = html.unescape(str(value or ""))
    text = re.sub(r"<[^>]+>", "", text)
    return " ".join(text.split()).strip()


def _brief_lines(result: Dict[str, Any], *, title: str | None = None) -> List[str]:
    lines: List[str] = []
    heading = title or f"네이버 뉴스 브리핑: {result['query']}"
    suffix = []
    if result.get("exclude_words"):
        suffix.append("제외=" + ", ".join(result["exclude_words"]))
    if result.get("days"):
        suffix.append(f"최근 {result['days']}일")
    meta = f" ({'; '.join(suffix)})" if suffix else ""
    lines.append(heading + meta)
    lines.append(f"- 총 검색 결과: {result.get('total', 0)}")
    lines.append(f"- 출력 기사 수: {result.get('displayed', 0)}")
    if result.get("filtered_out"):
        lines.append(f"- 제외어로 걸러진 수: {result['filtered_out']}")
    if result.get("too_old"):
        lines.append(f"- 기간 조건으로 제외된 수: {result['too_old']}")
    items = result.get("items", [])
    if not items:
        lines.append("- 새로 보여줄 기사가 없습니다.")
        return lines
    for idx, item in enumerate(items, start=1):
        publisher = item.get("publisher", "정보 없음")
        pub_date = item.get("pub_date", "")
        lines.append(f"{idx}. [{publisher}] {item.get('title', '').strip()}")
        if item.get("description"):
            lines.append(f"   - {item['description'].strip()[:180]}")
        if pub_date:
            lines.append(f"   - 발행: {pub_date}")
        if item.get("link"):
            lines.append(f"   - 링크: {item['link']}")
    return lines


def _print_payload(payload: Any, *, as_json: bool, render_text=None) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(payload) if render_text else payload)


def _format_watch_text(rule: Dict[str, Any]) -> str:
    extra = []
    if rule.get("days"):
        extra.append(f"최근 {rule['days']}일")
    if rule.get("exclude_words"):
        extra.append("제외=" + ", ".join(rule["exclude_words"]))
    if rule.get("template"):
        extra.append(f"template={rule['template']}")
    if rule.get("schedule", {}).get("label"):
        extra.append(f"schedule={rule['schedule']['label']}")
    lines = [f"- {rule['name']}: {rule['raw_query']}" + (f" ({'; '.join(extra)})" if extra else "")]
    if rule.get("label"):
        lines.append(f"  label: {rule['label']}")
    if rule.get("tags"):
        lines.append("  tags: " + ", ".join(rule["tags"]))
    if rule.get("context"):
        lines.append(f"  context: {rule['context']}")
    return "\n".join(lines)


def _prompt_required(prompt: str, *, secret: bool = False) -> str:
    while True:
        value = (getpass.getpass(prompt) if secret else input(prompt)).strip()
        if value:
            return value
        print("값이 비어 있습니다. 다시 입력해 주세요.")


def _validate_credential_value(name: str, value: str) -> str:
    cleaned = str(value or "").strip()
    if not cleaned:
        raise ValueError(f"{name} 값이 비어 있습니다.")
    if any(ch.isspace() for ch in cleaned):
        raise ValueError(f"{name} 값에 공백이 포함되어 있습니다. 복사 과정에서 줄바꿈/공백이 들어갔는지 확인해 주세요.")
    if len(cleaned) < 5:
        raise ValueError(f"{name} 값이 너무 짧습니다. 네이버 개발자센터에서 발급받은 값을 다시 확인해 주세요.")
    return cleaned


def _perform_live_check(query: str, *, limit: int = 1) -> Dict[str, Any]:
    client_id, client_secret, timeout, _ = get_runtime_credentials()
    return fetch_news(
        client_id=client_id,
        client_secret=client_secret,
        search_query=query,
        exclude_words=[],
        limit=limit,
        days=None,
        timeout=timeout,
    )


def _render_setup_success(timeout: int, *, live_checked: bool = False, live_query: str | None = None) -> str:
    lines = [
        "네이버 Search API 자격증명을 저장했습니다.",
        "- 저장 위치: data/config.json",
        f"- 요청 타임아웃: {timeout}초",
    ]
    if live_checked:
        lines.append(f"- 라이브 API 확인: 성공 ({live_query or DEFAULT_TEST_QUERY})")
    else:
        lines.append("- 라이브 API 확인: 생략")
    lines.extend(
        [
            "- 다음 단계: python scripts/naver_news_briefing.py check-credentials --json",
            "- 그 다음: python scripts/naver_news_briefing.py search \"최근 3일 반도체 뉴스 브리핑\"",
        ]
    )
    return "\n".join(lines)


def cmd_setup(args: argparse.Namespace) -> int:
    client_id = (args.client_id or "").strip()
    client_secret = (args.client_secret or "").strip()
    if not client_id:
        print("client_id가 없어 대화형 입력으로 전환합니다.")
        client_id = _prompt_required("네이버 client_id: ")
    if not client_secret:
        print("client_secret이 없어 대화형 입력으로 전환합니다.")
        client_secret = _prompt_required("네이버 client_secret: ", secret=True)

    client_id = _validate_credential_value("client_id", client_id)
    client_secret = _validate_credential_value("client_secret", client_secret)
    set_credentials(client_id, client_secret, args.timeout)

    live_checked = False
    live_query = args.test_search or (DEFAULT_TEST_QUERY if args.live_check else None)
    if live_query:
        result = _perform_live_check(live_query, limit=1)
        live_checked = True
        if args.json:
            print(json.dumps({
                "saved": True,
                "timeout": args.timeout,
                "live_check": {
                    "query": live_query,
                    "ok": True,
                    "displayed": result.get("displayed", 0),
                    "total": result.get("total", 0),
                },
            }, ensure_ascii=False, indent=2))
            return 0

    print(_render_setup_success(args.timeout, live_checked=live_checked, live_query=live_query))
    return 0


def _render_check_credentials_text(payload: Dict[str, Any]) -> str:
    lines = [
        "네이버 Search API 자격증명이 설정되어 있습니다." if payload["configured"] else "아직 네이버 Search API 자격증명이 설정되지 않았습니다.",
        f"- client_id 저장 여부: {'예' if payload['client_id_present'] else '아니오'}",
        f"- client_secret 저장 여부: {'예' if payload['client_secret_present'] else '아니오'}",
        f"- 요청 타임아웃: {payload['timeout']}초",
    ]
    live_check = payload.get("live_check")
    if isinstance(live_check, dict):
        if live_check.get("ok"):
            lines.append(f"- 라이브 API 확인: 성공 ({live_check.get('query')})")
            lines.append(f"- 테스트 결과: total={live_check.get('total', 0)}, displayed={live_check.get('displayed', 0)}")
        else:
            lines.append(f"- 라이브 API 확인: 실패 ({live_check.get('query')})")
            if live_check.get("error"):
                lines.append(f"- 오류: {live_check['error']}")
    if payload["configured"]:
        lines.append("- 다음 단계: search / watch / brief-multi / plan-save 를 실행하면 됩니다.")
    else:
        lines.append("- 먼저 실행: python scripts/naver_news_briefing.py setup")
        lines.append("- 확인: python scripts/naver_news_briefing.py check-credentials --json")
    return "\n".join(lines)


def cmd_check_credentials(args: argparse.Namespace) -> int:
    client_id, client_secret, timeout, _ = get_runtime_credentials()
    ok = bool(client_id and client_secret)
    payload: Dict[str, Any] = {"configured": ok, "client_id_present": bool(client_id), "client_secret_present": bool(client_secret), "timeout": timeout}
    if ok and args.live_check:
        query = args.query or DEFAULT_TEST_QUERY
        try:
            result = _perform_live_check(query, limit=1)
            payload["live_check"] = {
                "query": query,
                "ok": True,
                "displayed": result.get("displayed", 0),
                "total": result.get("total", 0),
            }
        except Exception as exc:
            payload["live_check"] = {"query": query, "ok": False, "error": str(exc)}
            ok = False
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else _render_check_credentials_text(payload))
    return 0 if ok else 1


def _render_missing_credentials_guidance() -> str:
    return "\n".join(
        [
            "네이버 Search API 자격증명이 아직 설정되지 않았습니다.",
            "먼저 최초 온보딩(setup)을 완료해 주세요.",
            "",
            "실행 순서:",
            "1) python scripts/naver_news_briefing.py setup --client-id YOUR_ID --client-secret YOUR_SECRET",
            "2) python scripts/naver_news_briefing.py check-credentials --json",
            "3) 그 다음 search / watch / brief-multi / plan-save 명령을 실행",
            "",
            "참고: 자격증명은 data/config.json 에 저장되며 Windows에서는 가능하면 DPAPI로 보호합니다.",
        ]
    )


def _dedupe_preserve_order(values: List[str]) -> List[str]:
    seen = set()
    ordered: List[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def _format_missing_named_resource(resource_label: str, missing_name: str, available_names: List[str]) -> str:
    lines = [f"등록된 {resource_label}을(를) 찾지 못했습니다: {missing_name}"]
    if available_names:
        lines.append("현재 등록된 항목: " + ", ".join(available_names))
    else:
        lines.append("현재 등록된 항목이 없습니다.")
    return "\n".join(lines)


def _format_exception_message(exc: Exception) -> str:
    message = str(exc).strip() or exc.__class__.__name__
    if MISSING_CREDENTIALS_ERROR in message:
        return _render_missing_credentials_guidance()
    if "keyword group not found:" in message:
        missing_name = message.split("keyword group not found:", 1)[1].strip().strip("'")
        available = [group.get("name") for group in list_groups() if group.get("name")]
        return _format_missing_named_resource("키워드 그룹", missing_name, available)
    if "watch rule not found:" in message:
        missing_name = message.split("watch rule not found:", 1)[1].strip().strip("'")
        available = [rule.get("name") for rule in list_rules() if rule.get("name")]
        return _format_missing_named_resource("watch rule", missing_name, available)
    return f"ERROR: {message}"


def run_search(query: str, *, limit: int, days: int | None, as_json: bool) -> int:
    intent = build_intent(query, limit=limit, days=days)
    client_id, client_secret, timeout, _ = get_runtime_credentials()
    result = fetch_news(client_id=client_id, client_secret=client_secret, search_query=intent.search_query, exclude_words=intent.exclude_words, limit=intent.limit, days=intent.days, timeout=timeout)
    result["intent"] = {"db_keyword": intent.db_keyword, "fetch_key": intent.fetch_key, "raw_query": intent.raw_query}
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n".join(_brief_lines(result)))
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    return run_search(args.query, limit=args.limit, days=args.days, as_json=args.json)


def cmd_watch_add(args: argparse.Namespace) -> int:
    intent = build_intent(args.query, limit=args.limit, days=args.days)
    rule = add_rule(
        name=args.name,
        raw_query=intent.raw_query,
        search_query=intent.search_query,
        db_keyword=intent.db_keyword,
        exclude_words=intent.exclude_words,
        fetch_key=intent.fetch_key,
        days=intent.days,
        limit=intent.limit,
        label=args.label,
        tags=args.tag,
        context=args.context,
        template=args.template,
    )
    _print_payload(rule, as_json=args.json, render_text=_format_watch_text)
    return 0


def cmd_watch_list(args: argparse.Namespace) -> int:
    rules = list_rules()
    if args.json:
        print(json.dumps(rules, ensure_ascii=False, indent=2))
        return 0
    if not rules:
        print("등록된 watch rule이 없습니다.")
        return 0
    print("\n\n".join(_format_watch_text(rule) for rule in rules))
    return 0


def cmd_watch_remove(args: argparse.Namespace) -> int:
    deleted = remove_rule(args.name_or_id)
    if deleted:
        print(f"삭제 완료: {args.name_or_id}")
        return 0
    print(f"삭제 대상 없음: {args.name_or_id}")
    return 1


def _run_rule(rule: Dict[str, Any]) -> Dict[str, Any]:
    client_id, client_secret, timeout, _ = get_runtime_credentials()
    result = fetch_news(client_id=client_id, client_secret=client_secret, search_query=rule["search_query"], exclude_words=rule["exclude_words"], limit=rule["limit"], days=rule.get("days"), timeout=timeout)
    new_items = mark_seen(rule["id"], result["items"])
    return {
        "rule": rule,
        "summary": {
            "query": result["query"],
            "total": result["total"],
            "displayed": result["displayed"],
            "new_count": len(new_items),
            "filtered_out": result["filtered_out"],
            "too_old": result["too_old"],
        },
        "new_items": new_items,
        "all_items": result["items"],
    }


def _format_watch_status_lines(entry: Dict[str, Any]) -> List[str]:
    rule = entry["rule"]
    summary = entry["summary"]
    items = entry.get("all_items", [])
    now = datetime.now().strftime("%m월 %d일 %H:%M")
    query = summary.get("query") or rule.get("search_query") or rule.get("name")
    current_top_count = len(items)
    new_count = summary["new_count"]
    lines = [
        f"## {rule['name']}",
        f"- {now} 기준, '{query}' 관련 상위 {current_top_count}건을 확인했고 이번 체크에서 신규 기사 {new_count}건이 추가됐습니다.",
        f"- 전체 검색 결과: {summary.get('total', 0)}건",
        f"- 이번 확인 신규 기사: {new_count}건",
        f"- 현재 검색 상위 기사 수: {current_top_count}건",
    ]
    if items:
        latest_pub = next((item.get("pub_date_iso") or item.get("pub_date") for item in items if item.get("pub_date_iso") or item.get("pub_date")), None)
        if latest_pub:
            lines.append(f"- 현재 기준 최신 기사 시각: {latest_pub}")
    return lines


def cmd_watch_check(args: argparse.Namespace) -> int:
    targets = [get_rule(args.name_or_id)] if args.name_or_id else list_rules()
    payload = [_run_rule(rule) for rule in targets]
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    if not payload:
        print("체크할 watch rule이 없습니다.")
        return 0
    if getattr(args, "announce_text", False):
        if len(payload) != 1:
            print("NO_REPLY")
            return 0
        entry = payload[0]
        new_items = entry.get("new_items", [])
        if not new_items:
            print("NO_REPLY")
            return 0
        summary = entry.get("summary", {})
        new_count = summary.get("new_count", len(new_items))
        latest_iso = new_items[0].get("pub_date_iso")
        latest_text = latest_iso.replace("T", " ")[:16] if latest_iso else "최신 없음"
        preview_items = new_items[:ANNOUNCE_PREVIEW_LIMIT]
        lines = [
            f"확인 요약: 새 뉴스 {new_count}건, 현재 검색 상위 {summary.get('displayed', 0)}건 / 전체 {summary.get('total', 0)}건, 최신 {latest_text}"
        ]
        for item in preview_items:
            title = _strip_html(item.get("title", "제목 없음"))
            publisher = item.get("publisher") or "정보 없음"
            pub_iso = item.get("pub_date_iso")
            pub_text = pub_iso.replace("T", " ")[:16] if pub_iso else item.get("pub_date", "시간 없음")
            link = item.get("link") or item.get("original_link") or ""
            lines.append(f"- {title} / {publisher} / {pub_text} / {link}")
        extra_count = max(0, new_count - len(preview_items))
        if extra_count > 0:
            lines.append(f"- 외 추가 새 뉴스 {extra_count}건")
        print("\n".join(lines))
        return 0
    lines: List[str] = []
    for entry in payload:
        rule = entry["rule"]
        lines.extend(_format_watch_status_lines(entry))
        lines.extend(_brief_lines({
            "query": rule["search_query"],
            "exclude_words": rule["exclude_words"],
            "days": rule.get("days"),
            "total": entry["summary"]["total"],
            "displayed": len(entry["new_items"]),
            "filtered_out": entry["summary"]["filtered_out"],
            "too_old": entry["summary"]["too_old"],
            "items": entry["new_items"],
        }, title=f"watch: {rule['name']} 신규 기사 요약"))
        lines.append("")
    print("\n".join(lines).strip())
    return 0


def _format_group_text(group: Dict[str, Any]) -> str:
    lines = [f"- {group['name']} ({group['query_count']}개 쿼리)"]
    if group.get("label"):
        lines.append(f"  label: {group['label']}")
    if group.get("tags"):
        lines.append("  tags: " + ", ".join(group["tags"]))
    if group.get("template"):
        lines.append(f"  template: {group['template']}")
    if group.get("schedule", {}).get("label"):
        lines.append(f"  schedule: {group['schedule']['label']}")
    if group.get("context"):
        lines.append(f"  context: {group['context']}")
    for idx, query in enumerate(group.get("queries", []), start=1):
        lines.append(f"  {idx}. {query}")
    return "\n".join(lines)


def cmd_group_add(args: argparse.Namespace) -> int:
    group = create_group(name=args.name, queries=args.query, label=args.label, tags=args.tag, context=args.context, template=args.template)
    _print_payload(group, as_json=args.json, render_text=_format_group_text)
    return 0


def cmd_group_list(args: argparse.Namespace) -> int:
    groups = [get_group(args.name_or_id)] if args.name_or_id else list_groups()
    if args.json:
        print(json.dumps(groups if not args.name_or_id else groups[0], ensure_ascii=False, indent=2))
        return 0
    if not groups:
        print("등록된 키워드 그룹이 없습니다.")
        return 0
    print("\n\n".join(_format_group_text(group) for group in groups))
    return 0


def cmd_group_remove(args: argparse.Namespace) -> int:
    deleted = remove_group(args.name_or_id)
    if deleted:
        print(f"삭제 완료: {args.name_or_id}")
        return 0
    print(f"삭제 대상 없음: {args.name_or_id}")
    return 1


def cmd_group_update(args: argparse.Namespace) -> int:
    tags = None
    if args.tag is not None or args.clear_tags:
        tags = [] if args.clear_tags else args.tag
    group = update_group(args.name_or_id, label=args.label, context=args.context, tags=tags, template=args.template, replace_queries=args.set_query, add_queries=args.add_query, remove_queries=args.remove_query)
    _print_payload(group, as_json=args.json, render_text=_format_group_text)
    return 0


def _run_query_entry(query: str, *, limit: int, days: int | None, group: Dict[str, Any] | None = None, label: str | None = None, context: str | None = None) -> Dict[str, Any]:
    intent = build_intent(query, limit=limit, days=days)
    client_id, client_secret, timeout, _ = get_runtime_credentials()
    result = fetch_news(client_id=client_id, client_secret=client_secret, search_query=intent.search_query, exclude_words=intent.exclude_words, limit=intent.limit, days=intent.days, timeout=timeout)
    result["intent"] = {"db_keyword": intent.db_keyword, "fetch_key": intent.fetch_key, "raw_query": intent.raw_query}
    return {
        "query": query,
        "search_query": intent.search_query,
        "exclude_words": intent.exclude_words,
        "days": intent.days,
        "group_name": group["name"] if group else None,
        "label": label or (group.get("label") if group else None),
        "tags": group.get("tags", []) if group else [],
        "context": context or (group.get("context") if group else None),
        "result": result,
    }


def cmd_brief_multi(args: argparse.Namespace) -> int:
    entries: List[Dict[str, Any]] = []
    groups: List[Dict[str, Any]] = []
    template = args.template
    for group_name in args.group or []:
        group = get_group(group_name)
        groups.append(group)
        if not args.template and group.get("template"):
            template = group["template"]
        for query in group["queries"]:
            entries.append(_run_query_entry(query, limit=args.limit, days=args.days, group=group))
    for query in args.query or []:
        entries.append(_run_query_entry(query, limit=args.limit, days=args.days))
    if not entries:
        raise ValueError("brief-multi에는 --query 또는 --group이 최소 1개 이상 필요합니다.")
    payload = build_combined_payload(entries, template=template, source_groups=groups)
    if args.json:
        print(render_combined_json(payload))
    else:
        print(render_combined_text(payload))
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    plan = parse_automation_request(args.request)
    _print_payload(plan_to_dict(plan), as_json=args.json, render_text=lambda _: render_plan_text(plan))
    return 0


def cmd_integration_plan(args: argparse.Namespace) -> int:
    bundle = build_integration_bundle(
        args.request,
        skill_dir=args.skill_dir or str(Path(__file__).resolve().parents[1]),
        assistant_channel=args.channel,
    )
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as fp:
            json.dump(bundle, fp, ensure_ascii=False, indent=2)
    _print_payload(bundle, as_json=args.json, render_text=render_integration_bundle_text)
    return 0


def cmd_plan_save(args: argparse.Namespace) -> int:
    plan = parse_automation_request(args.request)
    created: Dict[str, Any] = {"plan": plan_to_dict(plan), "created": []}
    name = args.name or plan.name_hint
    label = args.label or ("아침 브리핑" if plan.template == "morning-briefing" else None)
    tags = list(args.tag or [])
    if plan.schedule.kind != "manual":
        tags.append(plan.schedule.kind)
    if plan.watch_intent != "none":
        tags.append("watch")
    if plan.query_mode == "group":
        tags.append("group")
    tags = _dedupe_preserve_order(tags)
    if not plan.queries:
        raise ValueError("저장 가능한 주제 키워드를 찾지 못했습니다. 요청에 관심 주제를 포함해 주세요.")

    if args.as_type == "watch" and plan.query_mode == "group":
        raise ValueError("여러 주제를 포함한 그룹형 브리핑 요청입니다. --as group 으로 저장해 주세요.")

    if args.as_type == "group" or plan.query_mode == "group":
        group = create_group(
            name=name,
            queries=plan.queries,
            label=label,
            tags=tags,
            context=plan.raw_request,
            template=plan.template,
            schedule=plan_to_dict(plan)["schedule"],
            operator_hints=plan_to_dict(plan)["operator_hints"],
        )
        created["created"].append({"type": "group", "value": group})
    else:
        intent = build_intent(plan.primary_query or plan.queries[0])
        rule = add_rule(
            name=name,
            raw_query=intent.raw_query,
            search_query=intent.search_query,
            db_keyword=intent.db_keyword,
            exclude_words=intent.exclude_words,
            fetch_key=intent.fetch_key,
            days=intent.days,
            limit=intent.limit,
            label=label,
            tags=tags,
            context=plan.raw_request,
            template=plan.template,
            schedule=plan_to_dict(plan)["schedule"],
            operator_hints=plan_to_dict(plan)["operator_hints"],
        )
        created["created"].append({"type": "watch", "value": rule})

    _print_payload(created, as_json=args.json, render_text=lambda payload: render_plan_text(plan) + "\n- 저장 결과:\n" + "\n".join(f"  - {item['type']}: {item['value']['name']}" for item in payload['created']))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Naver news briefing skill CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("setup", help="네이버 API 자격증명 저장")
    p.add_argument("--client-id")
    p.add_argument("--client-secret")
    p.add_argument("--timeout", type=int, default=15)
    p.add_argument("--live-check", action="store_true", help="저장 직후 실제 API 호출로 자격증명을 확인")
    p.add_argument("--test-search", help="저장 직후 테스트할 검색어 (설정 시 라이브 체크 수행)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_setup)

    p = sub.add_parser("check-credentials", help="자격증명 상태 확인")
    p.add_argument("--json", action="store_true")
    p.add_argument("--live-check", action="store_true", help="실제 API 호출까지 포함해 확인")
    p.add_argument("--query", help="라이브 체크용 검색어")
    p.set_defaults(func=cmd_check_credentials)

    p = sub.add_parser("search", help="원샷 뉴스 검색/브리핑")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--days", type=int)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("watch-add", help="watch rule 추가")
    p.add_argument("name")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--days", type=int)
    p.add_argument("--label")
    p.add_argument("--tag", action="append")
    p.add_argument("--context")
    p.add_argument("--template", choices=supported_templates())
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_watch_add)

    p = sub.add_parser("watch-list", help="watch rule 목록")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_watch_list)

    p = sub.add_parser("watch-remove", help="watch rule 삭제")
    p.add_argument("name_or_id")
    p.set_defaults(func=cmd_watch_remove)

    p = sub.add_parser("watch-check", help="watch rule 신규 기사 체크")
    p.add_argument("name_or_id", nargs="?")
    p.add_argument("--json", action="store_true")
    p.add_argument("--announce-text", action="store_true", help="cron/announce friendly plain text output")
    p.set_defaults(func=cmd_watch_check)

    p = sub.add_parser("group-add", help="키워드 그룹 추가")
    p.add_argument("name")
    p.add_argument("query", nargs="+")
    p.add_argument("--label")
    p.add_argument("--tag", action="append")
    p.add_argument("--context")
    p.add_argument("--template", choices=supported_templates())
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_group_add)

    p = sub.add_parser("group-list", help="키워드 그룹 조회/목록")
    p.add_argument("name_or_id", nargs="?")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_group_list)

    p = sub.add_parser("group-remove", help="키워드 그룹 삭제")
    p.add_argument("name_or_id")
    p.set_defaults(func=cmd_group_remove)

    p = sub.add_parser("group-update", help="키워드 그룹 수정")
    p.add_argument("name_or_id")
    p.add_argument("--label")
    p.add_argument("--context")
    p.add_argument("--template", choices=supported_templates())
    p.add_argument("--tag", action="append")
    p.add_argument("--clear-tags", action="store_true")
    p.add_argument("--set-query", action="append")
    p.add_argument("--add-query", action="append")
    p.add_argument("--remove-query", action="append")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_group_update)

    p = sub.add_parser("brief-multi", help="여러 쿼리/그룹을 묶어 한 번에 브리핑")
    p.add_argument("--query", action="append")
    p.add_argument("--group", action="append")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--days", type=int)
    p.add_argument("--template", choices=supported_templates())
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_brief_multi)

    p = sub.add_parser("plan", help="채팅형 자연어 요청을 자동화 계획으로 변환")
    p.add_argument("request")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_plan)

    p = sub.add_parser("integration-plan", help="자연어 요청을 OpenClaw/cron 연동 번들로 변환")
    p.add_argument("request")
    p.add_argument("--channel", default="telegram")
    p.add_argument("--skill-dir")
    p.add_argument("--output")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_integration_plan)

    p = sub.add_parser("plan-save", help="자연어 요청을 해석해 watch/group 설정으로 저장")
    p.add_argument("request")
    p.add_argument("--name")
    p.add_argument("--as", dest="as_type", choices=["watch", "group"])
    p.add_argument("--label")
    p.add_argument("--tag", action="append")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_plan_save)

    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(_format_exception_message(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
