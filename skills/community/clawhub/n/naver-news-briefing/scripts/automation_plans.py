from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from query_utils import build_intent, clean_natural_query

_MONITOR_WORDS = ["모니터링", "감시", "체크", "알림", "추적", "watch"]
_BRIEF_WORDS = ["브리핑", "요약", "정리", "보고"]
_GROUP_HINTS = ["묶", "그룹", "여러", "같이", "함께", "이랑", "하고", "랑"]
_TEMPLATE_HINTS = {
    "concise": ["간단", "짧게", "핵심만", "한눈에"],
    "analyst": ["분석", "인사이트", "시사점", "깊게"],
    "morning-briefing": ["아침", "출근", "오전 보고", "morning"],
    "watch-alert": ["알림", "alert", "실시간", "바로"],
}
_TIME_OF_DAY_HINTS = {
    "아침": "08:00",
    "오전": "09:00",
    "점심": "12:00",
    "오후": "15:00",
    "저녁": "18:00",
    "밤": "21:00",
    "새벽": "06:00",
}
_DAYS_OF_WEEK = {"월": "mon", "화": "tue", "수": "wed", "목": "thu", "금": "fri", "토": "sat", "일": "sun"}
_DOW_CRON = {"mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6, "sun": 0}


@dataclass(frozen=True)
class SchedulePlan:
    kind: str
    label: str
    cron: str | None = None
    interval_minutes: int | None = None
    time: str | None = None
    days_of_week: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class OperatorHints:
    recommended_runner: str
    recommended_command: str
    delivery_format: str
    storage_target: str
    cadence_summary: str
    cron_examples: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class AutomationPlan:
    raw_request: str
    action: str
    query_mode: str
    queries: List[str]
    primary_query: str | None
    intent: Dict[str, Any] | None
    schedule: SchedulePlan
    name_hint: str
    template: str
    briefing_focus: str
    watch_intent: str
    group_reason: str | None
    rationale: List[str]
    suggested_commands: List[str]
    operator_hints: OperatorHints


def _normalize_request(raw: str) -> str:
    return re.sub(r"\s+", " ", str(raw or "").strip())


def _slugify_korean(text: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z가-힣]+", "-", str(text or "").strip().lower())
    cleaned = re.sub(r"-+", "-", cleaned).strip("-")
    return cleaned or "news-plan"


def _detect_action(raw: str) -> str:
    has_monitor = any(word in raw for word in _MONITOR_WORDS)
    has_brief = any(word in raw for word in _BRIEF_WORDS)
    if has_monitor and not has_brief:
        return "monitor"
    if has_brief and not has_monitor:
        return "briefing"
    if has_monitor and has_brief:
        return "monitor+briefing"
    return "briefing"


def _strip_schedule_and_action_phrases(text: str) -> str:
    patterns = [
        r"\d+\s*시간(?:마다|간격)",
        r"\d+\s*분(?:마다|간격)",
        r"매일",
        r"매주\s*[월화수목금토일]요일?",
        r"(?:아침|오전|점심|오후|저녁|밤|새벽)\s*\d{1,2}(?::|시)?\s*\d{0,2}분?(?:\s*에)?",
        r"\d{1,2}(?::|시)\s*\d{0,2}분?(?:\s*에)?",
        r"실시간",
        r"수시로",
        r"계속",
        r"지속적으로",
        r"주기적으로",
        r"모니터링해줘|모니터링 해줘|모니터링",
        r"감시해줘|감시 해줘|감시",
        r"체크해줘|체크 해줘|체크",
        r"알림해줘|알림 해줘",
        r"브리핑해줘|브리핑 해줘",
        r"정리해줘|정리 해줘",
        r"요약해줘|요약 해줘",
    ]
    stripped = text
    for pattern in patterns:
        stripped = re.sub(pattern, " ", stripped)
    return _normalize_request(stripped)


def _normalize_query_order(query: str) -> str:
    parts = [part for part in str(query or "").split() if part]
    positives = [part for part in parts if not part.startswith("-")]
    negatives = [part for part in parts if part.startswith("-")]
    return " ".join(positives + negatives)


def _extract_queries(raw: str) -> List[str]:
    text = _strip_schedule_and_action_phrases(_normalize_request(raw))
    split_pattern = r"\s*(?:,|/|\+|그리고|및|이랑|와|과|랑|하고)\s*"
    candidates = [part.strip() for part in re.split(split_pattern, text) if part.strip()]
    queries: List[str] = []
    for candidate in candidates:
        cleaned = _normalize_query_order(clean_natural_query(candidate))
        if cleaned:
            queries.append(cleaned)
    deduped: List[str] = []
    seen = set()
    for query in queries:
        key = query.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(query)
    return deduped


def _detect_explicit_time(text: str) -> str | None:
    prefixed = re.search(r"(아침|오전|오후|저녁|밤|새벽)\s*(\d{1,2})(?:[:시]\s*(\d{1,2}))?분?", text)
    if prefixed:
        prefix = prefixed.group(1)
        hour = int(prefixed.group(2))
        minute = int(prefixed.group(3) or 0)
        if prefix in {"오후", "저녁", "밤"} and hour < 12:
            hour += 12
        if prefix == "새벽" and hour == 12:
            hour = 0
        if prefix == "오전" and hour == 12:
            hour = 0
        return f"{hour:02d}:{minute:02d}"

    plain = re.search(r"(\d{1,2})(?:[:시]\s*(\d{1,2}))?분?", text)
    if plain:
        return f"{int(plain.group(1)):02d}:{int(plain.group(2) or 0):02d}"
    return None


def _detect_schedule(raw: str) -> SchedulePlan:
    text = _normalize_request(raw)

    if re.search(r"실시간|수시로|계속|지속적으로", text):
        return SchedulePlan(kind="interval", label="15분마다", cron="*/15 * * * *", interval_minutes=15)

    every_n_hours = re.search(r"(\d+)\s*시간(?:마다|간격)", text)
    if every_n_hours:
        hours = max(1, int(every_n_hours.group(1)))
        minutes = hours * 60
        cron = f"0 */{hours} * * *" if minutes >= 60 and minutes % 60 == 0 else f"*/{minutes} * * * *"
        return SchedulePlan(kind="interval", label=f"{hours}시간마다", cron=cron, interval_minutes=minutes)

    every_n_minutes = re.search(r"(\d+)\s*분(?:마다|간격)", text)
    if every_n_minutes:
        minutes = max(1, int(every_n_minutes.group(1)))
        return SchedulePlan(kind="interval", label=f"{minutes}분마다", cron=f"*/{minutes} * * * *", interval_minutes=minutes)

    weekly = re.search(r"매주\s*([월화수목금토일])요일?", text)
    if weekly:
        day = _DAYS_OF_WEEK[weekly.group(1)]
        time = _detect_explicit_time(text) or next((v for k, v in _TIME_OF_DAY_HINTS.items() if k in text), "08:00")
        hh, mm = time.split(":")
        return SchedulePlan(kind="weekly", label=f"매주 {weekly.group(1)}요일 {time}", cron=f"{int(mm)} {int(hh)} * * {_DOW_CRON[day]}", time=time, days_of_week=[day])

    if "매일" in text:
        time = _detect_explicit_time(text) or next((v for k, v in _TIME_OF_DAY_HINTS.items() if k in text), "08:00")
        hh, mm = time.split(":")
        return SchedulePlan(kind="daily", label=f"매일 {time}", cron=f"{int(mm)} {int(hh)} * * *", time=time)

    return SchedulePlan(kind="manual", label="수동 실행")


def _detect_template(raw: str, action: str, schedule: SchedulePlan) -> str:
    for template, words in _TEMPLATE_HINTS.items():
        if any(word in raw for word in words):
            return template
    if action == "monitor":
        return "watch-alert"
    if schedule.kind == "daily":
        return "morning-briefing"
    return "concise"


def _detect_briefing_focus(raw: str, template: str) -> str:
    if template == "morning-briefing":
        return "아침 브리핑"
    if any(word in raw for word in ["핵심만", "간단", "짧게"]):
        return "핵심 요약"
    if any(word in raw for word in ["분석", "시사점", "인사이트"]):
        return "분석형 정리"
    return "일반 브리핑"


def _detect_watch_intent(raw: str, action: str) -> str:
    if "monitor" not in action:
        return "none"
    if any(word in raw for word in ["계속", "실시간", "수시로", "바로"]):
        return "continuous"
    if any(word in raw for word in ["모니터링", "감시", "체크", "알림"]):
        return "scheduled"
    return "manual"


def _suggest_name(queries: List[str], action: str) -> str:
    base = queries[0] if queries else action
    suffix = "watch" if "monitor" in action else "brief"
    return _slugify_korean(f"{base}-{suffix}")


def _build_commands(plan: AutomationPlan) -> List[str]:
    commands: List[str] = []
    if plan.query_mode == "group":
        quoted_queries = " ".join(f'"{query}"' for query in plan.queries)
        commands.append(
            f'python scripts/naver_news_briefing.py group-add {plan.name_hint} {quoted_queries} --label "자동 생성 그룹" --context "{plan.raw_request}" --template {plan.template}'
        )
        commands.append(f"python scripts/naver_news_briefing.py brief-multi --group {plan.name_hint} --template {plan.template}")
        commands.append(f'python scripts/naver_news_briefing.py plan-save "{plan.raw_request}" --as group --name {plan.name_hint}')
    else:
        query = plan.primary_query or ""
        if "monitor" in plan.action:
            commands.append(f'python scripts/naver_news_briefing.py watch-add {plan.name_hint} "{query}" --template {plan.template}')
            commands.append(f"python scripts/naver_news_briefing.py watch-check {plan.name_hint} --json")
        if "briefing" in plan.action:
            commands.append(f'python scripts/naver_news_briefing.py search "{query}"')
        commands.append(f'python scripts/naver_news_briefing.py plan-save "{plan.raw_request}" --as watch --name {plan.name_hint}')
    return commands


def _build_operator_hints(plan: AutomationPlan) -> OperatorHints:
    storage_target = "group" if plan.query_mode == "group" else "watch"
    recommended_runner = "cron" if plan.schedule.kind != "manual" else "manual"
    if storage_target == "group":
        recommended_command = f"python scripts/naver_news_briefing.py brief-multi --group {plan.name_hint} --template {plan.template}"
        delivery_format = "chat-briefing"
    else:
        recommended_command = f"python scripts/naver_news_briefing.py watch-check {plan.name_hint} --json" if "monitor" in plan.action else f'python scripts/naver_news_briefing.py search "{plan.primary_query or ""}"'
        delivery_format = "watch-json" if "monitor" in plan.action else "chat-briefing"
    notes = [
        "스케줄 실행은 이 스킬이 아니라 외부 cron/작업 스케줄러/OpenClaw cron에서 연결하는 방식이 가장 안정적입니다.",
        "watch는 새 기사 감지용, group은 반복 브리핑용으로 두면 운영이 단순합니다.",
    ]
    cron_examples: List[str] = []
    if plan.schedule.cron:
        cron_examples.append(f'{plan.schedule.cron} {recommended_command}')
        cron_examples.append(f'{plan.schedule.cron} # 위 명령 실행 후 stdout/json을 텔레그램·디스코드 전송')
    return OperatorHints(
        recommended_runner=recommended_runner,
        recommended_command=recommended_command,
        delivery_format=delivery_format,
        storage_target=storage_target,
        cadence_summary=plan.schedule.label,
        cron_examples=cron_examples,
        notes=notes,
    )


def parse_automation_request(raw: str) -> AutomationPlan:
    request = _normalize_request(raw)
    action = _detect_action(request)
    schedule = _detect_schedule(request)
    queries = _extract_queries(request)
    query_mode = "group" if len(queries) > 1 or any(hint in request for hint in _GROUP_HINTS) else "single"
    primary_query = queries[0] if queries else None
    intent = None
    rationale: List[str] = []
    if primary_query:
        built = build_intent(primary_query)
        intent = asdict(built)
        rationale.append(f"핵심 검색어를 '{built.search_query}'로 정규화했습니다.")
        if built.exclude_words:
            rationale.append("제외어를 유지해 watch/search 명령으로 바로 연결할 수 있게 했습니다.")
    else:
        rationale.append("주제 키워드가 없어 저장 가능한 watch/search 명령은 만들지 않았습니다.")
    if schedule.kind != "manual":
        rationale.append(f"일정 표현을 '{schedule.label}' 구조로 해석했습니다.")
    group_reason = None
    if query_mode == "group":
        group_reason = "여러 주제를 한 번에 반복 브리핑하기 좋은 요청입니다."
        rationale.append("여러 주제를 감지해 그룹 기반 브리핑/자동화로 분류했습니다.")

    template = _detect_template(request, action, schedule)
    plan = AutomationPlan(
        raw_request=request,
        action=action,
        query_mode=query_mode,
        queries=queries,
        primary_query=primary_query,
        intent=intent,
        schedule=schedule,
        name_hint=_suggest_name(queries, action),
        template=template,
        briefing_focus=_detect_briefing_focus(request, template),
        watch_intent=_detect_watch_intent(request, action),
        group_reason=group_reason,
        rationale=rationale,
        suggested_commands=[],
        operator_hints=OperatorHints(
            recommended_runner="manual",
            recommended_command="",
            delivery_format="text",
            storage_target="watch" if query_mode == "single" else "group",
            cadence_summary=schedule.label,
        ),
    )
    commands = _build_commands(plan)
    hints = _build_operator_hints(plan)
    return AutomationPlan(**{**asdict(plan), "suggested_commands": commands, "operator_hints": hints, "schedule": plan.schedule})


def render_plan_text(plan: AutomationPlan) -> str:
    lines = ["## 뉴스 자동화 계획", f"- 요청: {plan.raw_request}", f"- 작업 유형: {plan.action}", f"- 일정: {plan.schedule.label}"]
    if plan.queries:
        lines.append("- 해석된 질의: " + ", ".join(plan.queries))
    lines.append(f"- 저장 대상 추천: {plan.operator_hints.storage_target}")
    if plan.name_hint:
        lines.append(f"- 저장 이름 제안: {plan.name_hint}")
    lines.append(f"- 추천 템플릿: {plan.template} ({plan.briefing_focus})")
    lines.append(f"- watch 의도: {plan.watch_intent}")
    if plan.schedule.cron:
        lines.append(f"- cron 힌트: {plan.schedule.cron}")
    if plan.group_reason:
        lines.append(f"- 그룹 판단: {plan.group_reason}")
    if plan.rationale:
        lines.append("- 해석 근거:")
        lines.extend(f"  - {item}" for item in plan.rationale)
    lines.append("- 운영 힌트:")
    lines.append(f"  - 실행 방식: {plan.operator_hints.recommended_runner}")
    lines.append(f"  - 추천 실행 명령: {plan.operator_hints.recommended_command}")
    for note in plan.operator_hints.notes:
        lines.append(f"  - {note}")
    if plan.operator_hints.cron_examples:
        lines.append("- cron 예시:")
        lines.extend(f"  - {item}" for item in plan.operator_hints.cron_examples)
    if plan.suggested_commands:
        lines.append("- 추천 명령:")
        lines.extend(f"  - {cmd}" for cmd in plan.suggested_commands)
    return "\n".join(lines)


def plan_to_dict(plan: AutomationPlan) -> Dict[str, Any]:
    payload = asdict(plan)
    payload["schedule"] = asdict(plan.schedule)
    payload["operator_hints"] = asdict(plan.operator_hints)
    return payload


def build_integration_bundle(raw: str, *, skill_dir: str | Path | None = None, assistant_channel: str = "telegram") -> Dict[str, Any]:
    plan = parse_automation_request(raw)
    skill_root = Path(skill_dir).resolve() if skill_dir else Path(__file__).resolve().parents[1]
    cli_rel = str(skill_root / "scripts" / "naver_news_briefing.py")
    save_as = "group" if plan.query_mode == "group" else "watch"
    save_command = f'python scripts/naver_news_briefing.py plan-save "{plan.raw_request}" --as {save_as} --name {plan.name_hint}'
    run_command = plan.operator_hints.recommended_command
    shell_run = f'cd "{skill_root}" && {run_command}'
    shell_save = f'cd "{skill_root}" && {save_command}'
    schedule_payload = {
        "kind": plan.schedule.kind,
        "label": plan.schedule.label,
        "cron": plan.schedule.cron,
        "time": plan.schedule.time,
        "interval_minutes": plan.schedule.interval_minutes,
        "days_of_week": plan.schedule.days_of_week,
    }
    confirmation = f"'{plan.raw_request}' 요청을 {plan.schedule.label} {plan.operator_hints.storage_target} 자동화로 해석했습니다. 저장 이름은 '{plan.name_hint}'를 추천하고, 저장 뒤에는 '{run_command}'를 스케줄러에 연결하면 됩니다."
    cadence_phrase = plan.schedule.label if plan.schedule.label.endswith("마다") else f"{plan.schedule.label}마다"
    system_event_text = (
        f"{cadence_phrase} {assistant_channel} 채널에 네이버 뉴스 자동화를 실행하세요. "
        f"먼저 {save_command} 로 상태를 저장하고, 이후 {run_command} 결과를 전달합니다."
        if plan.schedule.kind != "manual"
        else f"필요할 때 {run_command} 를 수동 실행하는 네이버 뉴스 브리핑 요청입니다."
    )
    openclaw_prompt = (
        "다음 뉴스 자동화 계획을 기준으로 cron/작업을 생성하세요.\n"
        f"- 사용자 요청: {plan.raw_request}\n"
        f"- 저장 명령: {save_command}\n"
        f"- 실행 명령: {run_command}\n"
        f"- 일정: {json.dumps(schedule_payload, ensure_ascii=False)}\n"
        f"- 전달 포맷: {plan.operator_hints.delivery_format}\n"
        f"- 확인 문구: {confirmation}"
    )
    bundle = {
        "plan": plan_to_dict(plan),
        "storage": {
            "target": save_as,
            "name": plan.name_hint,
            "save_command": save_command,
            "shell_save_command": shell_save,
        },
        "runner": {
            "command": run_command,
            "shell_command": shell_run,
            "delivery_format": plan.operator_hints.delivery_format,
            "assistant_channel": assistant_channel,
        },
        "automation": {
            "schedule": schedule_payload,
            "cron_line": f"{plan.schedule.cron} {shell_run}" if plan.schedule.cron else None,
            "system_event_text": system_event_text,
            "openclaw_prompt": openclaw_prompt,
        },
        "assistant_summary": {
            "confirmation": confirmation,
            "user_summary": confirmation,
            "next_step": "저장 명령을 한 번 실행한 뒤 cron/OpenClaw 작업에서 실행 명령을 연결하세요.",
        },
        "artifacts": {
            "skill_dir": str(skill_root),
            "cli_path": cli_rel,
        },
    }
    return bundle


def render_integration_bundle_text(bundle: Dict[str, Any]) -> str:
    plan = bundle["plan"]
    storage = bundle["storage"]
    runner = bundle["runner"]
    automation = bundle["automation"]
    assistant_summary = bundle["assistant_summary"]
    lines = [
        "## OpenClaw 연동 번들",
        f"- 요청: {plan['raw_request']}",
        f"- 저장 대상: {storage['target']} ({storage['name']})",
        f"- 일정: {automation['schedule']['label']}",
        f"- 저장 명령: {storage['save_command']}",
        f"- 실행 명령: {runner['command']}",
    ]
    if automation.get("cron_line"):
        lines.append(f"- cron 한 줄 예시: {automation['cron_line']}")
    lines.append("- OpenClaw systemEvent 제안:")
    lines.append(f"  {automation['system_event_text']}")
    lines.append("- OpenClaw 작업 생성용 프롬프트:")
    for line in str(automation["openclaw_prompt"]).splitlines():
        lines.append(f"  {line}")
    lines.append("- 사용자 확인 문구:")
    lines.append(f"  {assistant_summary['confirmation']}")
    return "\n".join(lines)
