from __future__ import annotations

import json
from collections import Counter
from typing import Any, Dict, List


TEMPLATES = {
    "concise": "핵심만 빠르게 묶는 짧은 브리핑",
    "analyst": "질문별 핵심 흐름과 시사점을 조금 더 분석적으로 정리",
    "morning-briefing": "아침 보고용으로 전체 동향과 체크포인트를 정리",
    "watch-alert": "감시/알림 용도로 신규 기사 중심으로 짧게 정리",
}


def supported_templates() -> List[str]:
    return list(TEMPLATES.keys())


def build_combined_payload(entries: List[Dict[str, Any]], *, template: str, source_groups: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    publishers = Counter()
    total_items = 0
    total_filtered = 0
    total_too_old = 0
    for entry in entries:
        result = entry["result"]
        total_items += len(result.get("items", []))
        total_filtered += int(result.get("filtered_out", 0) or 0)
        total_too_old += int(result.get("too_old", 0) or 0)
        for item in result.get("items", []):
            publisher = str(item.get("publisher", "") or "").strip()
            if publisher:
                publishers[publisher] += 1
    top_publishers = [{"publisher": name, "count": count} for name, count in publishers.most_common(5)]
    return {
        "template": template,
        "entry_count": len(entries),
        "item_count": total_items,
        "filtered_out": total_filtered,
        "too_old": total_too_old,
        "top_publishers": top_publishers,
        "groups": source_groups or [],
        "entries": entries,
    }


def _header(payload: Dict[str, Any]) -> List[str]:
    lines = [f"네이버 뉴스 멀티 브리핑 · {payload['template']}"]
    lines.append(f"- 쿼리 수: {payload['entry_count']} / 기사 수: {payload['item_count']}")
    if payload.get("filtered_out"):
        lines.append(f"- 제외어 필터링: {payload['filtered_out']}건")
    if payload.get("too_old"):
        lines.append(f"- 기간 제외: {payload['too_old']}건")
    if payload.get("groups"):
        group_names = ", ".join(group["name"] for group in payload["groups"])
        lines.append(f"- 그룹: {group_names}")
    top_publishers = payload.get("top_publishers") or []
    if top_publishers:
        lines.append("- 많이 보인 출처: " + ", ".join(f"{item['publisher']} {item['count']}건" for item in top_publishers[:3]))
    return lines


def _entry_title(entry: Dict[str, Any]) -> str:
    title_bits = []
    if entry.get("group_name"):
        title_bits.append(f"[{entry['group_name']}]")
    title_bits.append(entry["query"])
    if entry.get("label"):
        title_bits.append(f"({entry['label']})")
    return " ".join(title_bits)


def _entry_items(entry: Dict[str, Any], *, limit: int) -> List[str]:
    result = entry["result"]
    items = result.get("items", [])[:limit]
    if not items:
        return ["- 표시할 기사가 없습니다."]
    lines: List[str] = []
    for item in items:
        title = str(item.get("title", "") or "").strip()
        publisher = str(item.get("publisher", "정보 없음") or "정보 없음")
        lines.append(f"- [{publisher}] {title}")
        if item.get("link"):
            lines.append(f"  링크: {item['link']}")
    return lines


def render_combined_text(payload: Dict[str, Any]) -> str:
    template = payload["template"]
    lines = _header(payload)
    lines.append("")
    if template == "concise":
        for entry in payload["entries"]:
            lines.append(f"## {_entry_title(entry)}")
            lines.extend(_entry_items(entry, limit=2))
            lines.append("")
    elif template == "analyst":
        lines.append("관찰 포인트")
        for entry in payload["entries"]:
            result = entry["result"]
            lines.append(f"## {_entry_title(entry)}")
            lines.append(f"- 노출 기사: {result.get('displayed', 0)} / 전체 결과: {result.get('total', 0)}")
            if entry.get("context"):
                lines.append(f"- 맥락: {entry['context']}")
            lines.extend(_entry_items(entry, limit=3))
            lines.append("")
    elif template == "morning-briefing":
        lines.append("오늘 체크할 흐름")
        for entry in payload["entries"]:
            result = entry["result"]
            headline = result.get("items", [{}])[0].get("title") if result.get("items") else "기사 없음"
            lines.append(f"- {_entry_title(entry)}: {headline}")
        lines.append("")
        lines.append("세부 기사")
        for entry in payload["entries"]:
            lines.append(f"## {_entry_title(entry)}")
            lines.extend(_entry_items(entry, limit=2))
            lines.append("")
    elif template == "watch-alert":
        alert_entries = [entry for entry in payload["entries"] if entry["result"].get("displayed", 0)]
        if not alert_entries:
            lines.append("- 신규/표시 가능한 기사가 없습니다.")
        for entry in alert_entries:
            lines.append(f"## ALERT · {_entry_title(entry)}")
            lines.extend(_entry_items(entry, limit=2))
            lines.append("")
    else:
        raise ValueError(f"지원하지 않는 템플릿입니다: {template}")
    return "\n".join(line for line in lines).strip()


def render_combined_json(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)
