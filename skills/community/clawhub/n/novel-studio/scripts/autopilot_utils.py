#!/usr/bin/env python3
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from chapter_progress_utils import build_progress_report, extract_chapter_labels_from_plan, initialize_chapter_tasks
from stage_persistence_utils import now_iso

GOAL_CHAPTER_RE = re.compile(r'(第[0-9零一二三四五六七八九十百千万两]+章)(?:\s*结束)?')
TERMINAL_GOAL_RE = re.compile(r'第[0-9零一二三四五六七八九十百千万两]+章\s*结束')
DIRECT_PLAIN_BOUNDED_GOAL_RE = re.compile(
    r'^\s*(继续到|继续写到|直到)\s*(第[0-9零一二三四五六七八九十百千万两]+章)\s*结束\s*$'
)
DIRECT_REPLACEMENT_BOUNDED_GOAL_RE = re.compile(
    r'^\s*(改成继续到|改为继续到)\s*(第[0-9零一二三四五六七八九十百千万两]+章)\s*结束\s*$'
)
REFERENCE_INTRODUCER_MARKERS = ('这句', '这句话', '文案', '照抄', '删掉', '删除', '原文', '文档', '注释', '写着')
ACK_TOKENS = {'好', '好的', '收到', '继续', '嗯', '行'}
ACK_TRAILING_PARTICLES = '吧呀啊呢啦'
CHINESE_DIGITS = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
CHINESE_UNITS = {'十': 10, '百': 100, '千': 1000, '万': 10000}
PLAN_HEADING_RE = re.compile(r'^\s*###\s+(第[0-9零一二三四五六七八九十百千万两]+章)(?:\s|$|[:：])')
AUTO_APPROVABLE_GATES = {
    'waiting_draft_feedback',
    'waiting_polishing_feedback',
    'waiting_proofreading_feedback',
}
FORMAL_REVISION_BLOCKER_PREFIX = 'Formal revision active:'
AUTO_ACTION_SUMMARIES = {
    'confirm_scope': '已自动确认本轮范围',
    'approve_chapter_plan': '已自动确认本轮章节规划',
}
AUTO_GATE_ACTION_SUMMARIES = {
    'waiting_draft_feedback': '已自动通过初稿审批，进入润色阶段',
    'waiting_polishing_feedback': '已自动通过润色审批，进入校对阶段',
    'waiting_proofreading_feedback': '已自动通过校对审批，进入终审阶段',
}
AUTO_BLOCKING_REASON_SUMMARIES = {
    'final_review_manual': '终审必须人工确认',
    'gate_requires_manual_approval': '当前审批门需要人工确认',
    'formal_revision_active': '正式修订流程进行中',
}


def normalize_bool(value, *, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return bool(value)

    normalized = str(value).strip().lower()
    if normalized in {'true', '1', 'yes', 'y', 'on'}:
        return True
    if normalized in {'false', '0', 'no', 'n', 'off', ''}:
        return False
    return default


def normalize_goal_chapter(goal_chapter) -> str | None:
    if goal_chapter is None:
        return None
    if isinstance(goal_chapter, int):
        return f'第{goal_chapter}章'

    normalized = str(goal_chapter).strip()
    if not normalized or normalized == '无':
        return None
    if normalized.endswith('结束'):
        normalized = normalized[:-2].strip()
    chapter_number = parse_chapter_number(normalized)
    if chapter_number is not None:
        return f'第{chapter_number}章'
    return normalized


def default_autopilot() -> dict:
    return {
        'active': False,
        'goalChapter': None,
        'goalCondition': 'proofreading_completed',
        'startedAt': None,
        'startedBy': None,
        'lastProgressAt': None,
        'lastProgressSummary': None,
        'stopReason': None,
        'stoppedAt': None,
        'awaitingManualResume': False,
    }


def normalize_autopilot(data: dict | None) -> dict:
    normalized = default_autopilot()
    if isinstance(data, dict):
        normalized.update(data)

    normalized['active'] = normalize_bool(normalized.get('active'), default=False)
    normalized['goalChapter'] = normalize_goal_chapter(normalized.get('goalChapter'))
    normalized['awaitingManualResume'] = normalize_bool(
        normalized.get('awaitingManualResume'),
        default=False,
    )
    return normalized


def extract_goal_chapter(message: str) -> str | None:
    normalized = strip_quoted_segments(message or '')
    bounded_goal = resolve_explicit_autopilot_goal(normalized, active=True)
    if bounded_goal:
        return bounded_goal

    terminal_matches = TERMINAL_GOAL_RE.findall(normalized)
    if terminal_matches:
        return normalize_goal_chapter(terminal_matches[-1].replace(' ', ''))

    match = GOAL_CHAPTER_RE.search(normalized)
    if match:
        return normalize_goal_chapter(match.group(1))
    return None


def has_terminal_goal(message: str) -> bool:
    return extract_goal_chapter(message) is not None and bool(TERMINAL_GOAL_RE.search(message or ''))


def is_explicit_autopilot_request(message: str, *, active: bool = False) -> bool:
    return resolve_explicit_autopilot_goal(message, active=active) is not None


def _normalize_short_message(message: str) -> str:
    return (message or '').strip().strip('。！!，,？?~～.…')


def is_acknowledgement_message(message: str) -> bool:
    normalized = _normalize_short_message(message)
    if not normalized:
        return False

    parts = re.split(r'[\s，,。！!？?；;、.…]+', normalized)
    ack_parts = []
    for part in parts:
        token = part.strip()
        if not token:
            continue
        token = token.rstrip(ACK_TRAILING_PARTICLES)
        if not token:
            continue
        ack_parts.append(token)

    return bool(ack_parts) and all(is_ack_token_sequence(part) for part in ack_parts)


def is_non_substantive_user_message(message: str) -> bool:
    normalized = (message or '').strip()
    if not normalized:
        return True

    for char in normalized:
        category = unicodedata.category(char)
        if category[0] not in {'P', 'Z', 'C'}:
            return False

    return True


def parse_chapter_number(value: str) -> int | None:
    normalized = str(value).strip()
    if not normalized:
        return None
    if normalized.startswith('第') and normalized.endswith('章'):
        normalized = normalized[1:-1].strip()
    if not normalized:
        return None
    if normalized.isdigit():
        return int(normalized)
    return chinese_numeral_to_int(normalized)


def extract_bounded_goal_chapter(message: str) -> str | None:
    return resolve_explicit_autopilot_goal(message, active=True)


def strip_quoted_segments(message: str) -> str:
    normalized = message or ''
    return re.sub(r'[\"“”\'‘’][^\"“”\'‘’]*[\"“”\'‘’]', '', normalized)


def split_message_clauses(message: str) -> list[tuple[str, bool]]:
    normalized = message or ''
    pieces = re.split(r'([\n，,。！？!?；;、：:]+)', normalized)
    clauses = []
    pending_separator = ''
    previous_clause = ''

    for piece in pieces:
        if not piece:
            continue
        if re.fullmatch(r'[\n，,。！？!?；;、：:]+', piece):
            pending_separator = piece
            continue

        clause = piece.strip()
        if not clause:
            continue

        carries_reference = bool(pending_separator) and is_reference_introducer_clause(previous_clause)
        clauses.append((clause, carries_reference))
        previous_clause = clause
        pending_separator = ''

    return clauses


def is_reference_introducer_clause(clause: str) -> bool:
    return any(marker in (clause or '') for marker in REFERENCE_INTRODUCER_MARKERS)


def extract_plain_bounded_goal_from_clause(clause: str) -> str | None:
    match = DIRECT_PLAIN_BOUNDED_GOAL_RE.fullmatch(clause)
    if not match:
        return None
    return normalize_goal_chapter(match.group(2))


def extract_replacement_goal_from_clause(clause: str) -> str | None:
    match = DIRECT_REPLACEMENT_BOUNDED_GOAL_RE.fullmatch(clause)
    if not match:
        return None
    return normalize_goal_chapter(match.group(2))


def resolve_explicit_autopilot_goal(message: str, *, active: bool = False) -> str | None:
    stripped = strip_quoted_segments((message or '').strip())
    if not stripped:
        return None

    for clause, inherited_reference in split_message_clauses(stripped):
        replacement_goal = extract_replacement_goal_from_clause(clause)
        if replacement_goal:
            if active and not inherited_reference:
                return replacement_goal
            continue

        plain_goal = extract_plain_bounded_goal_from_clause(clause)
        if plain_goal:
            if not inherited_reference:
                return plain_goal

    return None


def is_ack_token_sequence(token: str) -> bool:
    if token in ACK_TOKENS:
        return True
    for ack_token in sorted(ACK_TOKENS, key=len, reverse=True):
        if token.startswith(ack_token) and token != ack_token:
            remainder = token[len(ack_token):]
            if remainder and is_ack_token_sequence(remainder):
                return True
    return False


def chinese_numeral_to_int(value: str) -> int | None:
    total = 0
    section = 0
    number = 0

    for char in value:
        if char in CHINESE_DIGITS:
            number = CHINESE_DIGITS[char]
            continue
        unit = CHINESE_UNITS.get(char)
        if unit is None:
            return None
        if unit == 10000:
            section += number
            total = (total + section) * unit
            section = 0
            number = 0
            continue
        if number == 0:
            number = 1
        section += number * unit
        number = 0

    return total + section + number


def start_autopilot(state: dict, message: str) -> dict:
    return start_autopilot_with_goal(state, message, goal_chapter=extract_goal_chapter(message))


def start_autopilot_with_goal(state: dict, message: str, *, goal_chapter: str | None) -> dict:
    auto_pilot = normalize_autopilot(state.get('autoPilot'))
    auto_pilot.update(
        {
            'active': True,
            'goalChapter': normalize_goal_chapter(goal_chapter),
            'goalCondition': 'proofreading_completed',
            'startedAt': now_iso(),
            'startedBy': (message or '').strip() or None,
            'lastProgressAt': None,
            'lastProgressSummary': None,
            'stopReason': None,
            'stoppedAt': None,
            'awaitingManualResume': False,
        }
    )
    state['autoPilot'] = auto_pilot
    return auto_pilot


def stop_autopilot(state: dict, reason: str) -> dict:
    auto_pilot = normalize_autopilot(state.get('autoPilot'))
    auto_pilot.update(
        {
            'active': False,
            'stopReason': reason,
            'stoppedAt': now_iso(),
            'awaitingManualResume': True,
        }
    )
    state['autoPilot'] = auto_pilot
    return auto_pilot


def record_autopilot_progress(state: dict, summary: str | None) -> dict:
    auto_pilot = normalize_autopilot(state.get('autoPilot'))
    state['autoPilot'] = auto_pilot
    normalized_summary = (summary or '').strip() or None
    if not auto_pilot.get('active') or normalized_summary is None:
        return auto_pilot

    auto_pilot['lastProgressAt'] = now_iso()
    auto_pilot['lastProgressSummary'] = normalized_summary
    return auto_pilot


def stop_autopilot_with_blockers(
    state: dict,
    *,
    blocked_reasons: list[str] | None = None,
    summary: str | None = None,
) -> dict:
    auto_pilot = normalize_autopilot(state.get('autoPilot'))
    state['autoPilot'] = auto_pilot
    if not auto_pilot.get('active'):
        return auto_pilot

    reasons = [str(item).strip() for item in (blocked_reasons or []) if str(item).strip()]
    explicit_reason = reasons[0] if reasons else ((summary or '').strip() or 'execution blocked')
    return stop_autopilot(state, f'blocked: {explicit_reason}')


def summarize_chapter_progress(batch: dict, chapter_labels: list[str]) -> str | None:
    if not isinstance(batch, dict):
        return None

    tasks = list(batch.get('chapterTasks') or [])
    summaries: list[str] = []
    seen: set[str] = set()
    for chapter_label in chapter_labels:
        if not chapter_label or chapter_label in seen:
            continue
        seen.add(chapter_label)
        for task in tasks:
            if task.get('chapterLabel') != chapter_label:
                continue
            summary = (task.get('lastSummary') or '').strip()
            if summary:
                summaries.append(summary)
            break

    if not summaries:
        return None
    return '；'.join(summaries)


def is_goal_chapter_proofreading_completed(state: dict) -> bool:
    auto_pilot = normalize_autopilot(state.get('autoPilot'))
    if not auto_pilot.get('active'):
        return False
    if auto_pilot.get('goalCondition') != 'proofreading_completed':
        return False

    goal_chapter = auto_pilot.get('goalChapter')
    if not goal_chapter:
        return False

    batch = state.get('batch')
    if not isinstance(batch, dict):
        return False
    if not batch.get('proofreadingComplete'):
        return False

    for task in batch.get('chapterTasks') or []:
        if not isinstance(task, dict):
            continue
        if task.get('chapterLabel') != goal_chapter:
            continue
        if task.get('phase') != 'proofreading':
            continue
        if task.get('phaseStatus') == 'completed':
            return True
    return False


def load_auto_approvable_chapter_plan(project_path: Path) -> str | None:
    plan_path = Path(project_path) / '05_本轮章节规划.md'
    if not plan_path.exists() or not plan_path.is_file():
        return None
    plan_text = plan_path.read_text(encoding='utf-8')
    if not plan_text.strip():
        return None

    raw_labels: list[str] = []
    for line in plan_text.splitlines():
        match = PLAN_HEADING_RE.match(line)
        if match:
            raw_labels.append(match.group(1))
    if not raw_labels:
        return None
    if len(raw_labels) != len(set(raw_labels)):
        return None
    if not extract_chapter_labels_from_plan(plan_text):
        return None
    return plan_text


def has_active_formal_revision(state: dict) -> bool:
    revision = state.get('revision') if isinstance(state.get('revision'), dict) else {}
    if revision.get('currentRevisionGate'):
        return True

    blocking_issues = state.get('blockingIssues')
    if not isinstance(blocking_issues, list):
        return False
    return any(
        isinstance(item, str) and item.startswith(FORMAL_REVISION_BLOCKER_PREFIX)
        for item in blocking_issues
    )


def resolve_next_autopilot_action(state: dict, *, project_path: Path, eligible_gate: str | None = None) -> dict:
    auto_pilot = normalize_autopilot(state.get('autoPilot'))
    state['autoPilot'] = auto_pilot
    if not auto_pilot.get('active'):
        return {'action': 'noop', 'reason': 'autopilot_inactive'}
    if has_active_formal_revision(state):
        return {'action': 'noop', 'reason': 'formal_revision_active'}

    review = state.get('review') if isinstance(state.get('review'), dict) else {}
    current_gate = review.get('currentGate')
    if current_gate == 'waiting_final_review_feedback':
        return {'action': 'noop', 'reason': 'final_review_manual'}
    if current_gate:
        if current_gate == eligible_gate and current_gate in AUTO_APPROVABLE_GATES:
            return {'action': 'approve_gate', 'gate': current_gate}
        return {'action': 'noop', 'reason': 'gate_requires_manual_approval'}

    workflow = state.get('workflow') if isinstance(state.get('workflow'), dict) else {}
    batch = state.get('batch') if isinstance(state.get('batch'), dict) else {}
    if workflow.get('currentStage') != 'drafting' or not normalize_bool(batch.get('active'), default=False):
        return {'action': 'noop', 'reason': 'no_safe_autopilot_action'}

    if not normalize_bool(batch.get('scopeConfirmed'), default=False):
        batch['scopeConfirmed'] = True
        return {'action': 'confirm_scope'}

    plan_text = load_auto_approvable_chapter_plan(project_path)
    if not normalize_bool(batch.get('chapterPlanApproved'), default=False) and plan_text is not None:
        batch['chapterPlanApproved'] = True
        initialize_chapter_tasks(batch, plan_text)
        return {'action': 'approve_chapter_plan'}

    return {'action': 'noop', 'reason': 'no_safe_autopilot_action'}


def autopilot_runtime_status(auto_pilot: dict) -> str:
    if auto_pilot.get('active'):
        return 'running'
    if auto_pilot.get('awaitingManualResume'):
        return 'waiting_manual_resume'
    return 'inactive'


def summarize_autopilot_action(action_payload: dict) -> str | None:
    action = action_payload.get('action')
    if action in AUTO_ACTION_SUMMARIES:
        return AUTO_ACTION_SUMMARIES[action]
    if action == 'approve_gate':
        return AUTO_GATE_ACTION_SUMMARIES.get(action_payload.get('gate'))
    return None


def summarize_autopilot_blocking_reason(action_payload: dict) -> str | None:
    if action_payload.get('action') != 'noop':
        return None
    return AUTO_BLOCKING_REASON_SUMMARIES.get(action_payload.get('reason'))


def humanize_autopilot_stop_reason(reason: str | None) -> str | None:
    normalized = (reason or '').strip()
    if not normalized:
        return None
    if normalized == 'goal_reached':
        return '已达到目标章节（goal_reached）'
    if normalized == 'user_interruption':
        return '收到新的用户指令（user_interruption）'
    if normalized == 'superseded_by_new_user_goal':
        return '已切换到新的自动目标（superseded_by_new_user_goal）'
    if normalized.startswith('blocked:'):
        detail = normalized.split(':', 1)[1].strip()
        return f'阻塞：{detail}' if detail else '阻塞'
    return normalized


def render_autopilot_user_facing_message(
    *,
    pending_progress_summary: str | None,
    last_progress_summary: str | None,
    stop_reason: str | None,
    awaiting_manual_resume: bool,
    action_summary: str | None,
    blocking_reason: str | None,
) -> str | None:
    parts: list[str] = []
    if action_summary:
        parts.append(f'自动流程进展：{action_summary}')
    if pending_progress_summary:
        parts.append(f'章节进度：{pending_progress_summary}')

    if stop_reason is not None or awaiting_manual_resume:
        stop_text = humanize_autopilot_stop_reason(stop_reason) or '等待人工继续'
        parts.append(f'自动流程已停止：{stop_text}')
        if last_progress_summary and last_progress_summary != pending_progress_summary:
            parts.append(f'最近进度：{last_progress_summary}')
        return '；'.join(parts) if parts else None

    if blocking_reason:
        parts.append(f'自动流程暂停：{blocking_reason}')
        if last_progress_summary and last_progress_summary != pending_progress_summary:
            parts.append(f'最近进度：{last_progress_summary}')

    return '；'.join(parts) if parts else None


def build_autopilot_report(state: dict, action_payload: dict) -> dict:
    auto_pilot = normalize_autopilot(state.get('autoPilot'))
    batch = state.get('batch') if isinstance(state.get('batch'), dict) else {}
    progress_report = build_progress_report(batch.get('pendingProgressItems', []))
    pending_progress_summary = (progress_report.get('summary') or '').strip() or None
    last_progress_summary = (auto_pilot.get('lastProgressSummary') or '').strip() or None
    stop_reason = (auto_pilot.get('stopReason') or '').strip() or None
    action_summary = summarize_autopilot_action(action_payload)
    blocking_reason = summarize_autopilot_blocking_reason(action_payload)
    awaiting_manual_resume = normalize_bool(auto_pilot.get('awaitingManualResume'), default=False)

    should_notify = any(
        [
            pending_progress_summary,
            stop_reason,
            awaiting_manual_resume,
            action_summary,
            blocking_reason,
        ]
    )

    return {
        'status': autopilot_runtime_status(auto_pilot),
        'autopilotActive': normalize_bool(auto_pilot.get('active'), default=False),
        'awaitingManualResume': awaiting_manual_resume,
        'goalChapter': auto_pilot.get('goalChapter'),
        'lastProgressSummary': last_progress_summary,
        'pendingProgressSummary': pending_progress_summary,
        'pendingEventIds': list(progress_report.get('eventIds') or []),
        'stopReason': stop_reason,
        'actionSummary': action_summary,
        'blockingReason': blocking_reason,
        'shouldNotify': should_notify,
        'userFacingMessage': render_autopilot_user_facing_message(
            pending_progress_summary=pending_progress_summary,
            last_progress_summary=last_progress_summary,
            stop_reason=stop_reason,
            awaiting_manual_resume=awaiting_manual_resume,
            action_summary=action_summary,
            blocking_reason=blocking_reason,
        ),
    }
