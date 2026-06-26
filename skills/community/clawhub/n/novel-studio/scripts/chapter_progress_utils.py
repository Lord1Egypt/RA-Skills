#!/usr/bin/env python3
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import PurePosixPath
from uuid import uuid4

CHAPTER_LABEL_RE = re.compile(r'(第[0-9零一二三四五六七八九十百千万两]+章)')
PLAN_HEADING_RE = re.compile(r'^\s*###\s+(第[0-9零一二三四五六七八九十百千万两]+章)(?:\s|$|[:：])')


def extract_chapter_labels_from_plan(plan_text: str) -> list[str]:
    labels: list[str] = []
    seen: set[str] = set()
    for line in plan_text.splitlines():
        match = PLAN_HEADING_RE.match(line)
        if not match:
            continue
        label = match.group(1)
        if label in seen:
            continue
        seen.add(label)
        labels.append(label)
    return labels


def chapter_label_from_manuscript_path(relpath: str) -> str | None:
    stem = PurePosixPath(relpath).stem
    match = CHAPTER_LABEL_RE.match(stem)
    return match.group(1) if match else None


def resolve_dispatch_chapter_labels(stage: str, batch_plan_text: str, target_files: list[str]) -> list[str]:
    approved_labels = extract_chapter_labels_from_plan(batch_plan_text)
    if not approved_labels:
        raise ValueError('approved chapter plan does not contain any chapter headings')

    if stage == 'proofreading':
        return approved_labels

    if stage not in {'drafting', 'polishing'}:
        raise ValueError(f'unsupported stage for chapter label resolution: {stage}')
    if not target_files:
        raise ValueError(f'{stage} requires target files to resolve chapter labels')

    chapter_labels: list[str] = []
    seen: set[str] = set()
    for relpath in target_files:
        chapter_label = chapter_label_from_manuscript_path(relpath)
        if not chapter_label:
            raise ValueError(f'cannot resolve chapter label from target file: {relpath}')
        if chapter_label not in approved_labels:
            raise ValueError(f'target file chapter label is not in approved plan: {chapter_label} ({relpath})')
        if chapter_label in seen:
            raise ValueError(f'ambiguous target files map to the same chapter label: {chapter_label}')
        seen.add(chapter_label)
        chapter_labels.append(chapter_label)
    return chapter_labels


def default_progress_fields() -> dict:
    return {
        'chapterTasks': [],
        'pendingProgressItems': [],
    }


def chapter_task(label: str, manuscript_path: str | None = None) -> dict:
    return {
        'chapterLabel': label,
        'manuscriptPath': manuscript_path,
        'phase': 'drafting',
        'phaseStatus': 'queued',
        'lastSummary': None,
        'blockers': [],
        'updatedAt': None,
    }


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def progress_event_id(event: dict, index: int) -> str:
    event_id = event.get('eventId')
    if isinstance(event_id, str) and event_id.strip():
        return event_id

    chapter_label = event.get('chapterLabel') or 'unknown'
    phase = event.get('phase') or 'unknown'
    phase_status = event.get('phaseStatus') or 'unknown'
    created_at = event.get('createdAt') or f'index-{index}'
    return f'legacy-{chapter_label}-{phase}-{phase_status}-{created_at}-{index}'


def normalize_progress_batch(batch: dict) -> dict:
    fields = default_progress_fields()
    for key, default_value in fields.items():
        value = batch.get(key)
        batch[key] = list(value) if isinstance(value, list) else list(default_value)
    normalized_tasks: list[dict] = []
    for item in batch['chapterTasks']:
        if not isinstance(item, dict):
            continue
        task = dict(item)
        chapter_label = task.pop('chapterLabel', None)
        if chapter_label is None and 'label' in task:
            chapter_label = task.pop('label')
        else:
            task.pop('label', None)
        if not chapter_label:
            continue
        hydrated_task = chapter_task(chapter_label, task.get('manuscriptPath'))
        hydrated_task.update(task)
        normalized_tasks.append(hydrated_task)
    batch['chapterTasks'] = normalized_tasks
    return batch


def initialize_chapter_tasks(batch: dict, plan_text: str) -> dict:
    batch['chapterTasks'] = [chapter_task(label) for label in extract_chapter_labels_from_plan(plan_text)]
    batch['pendingProgressItems'] = []
    return batch


def human_summary(chapter_label: str, phase: str, phase_status: str, blockers: list[str] | None = None) -> str:
    blockers = list(blockers or [])
    if phase == 'blocked' or phase_status == 'blocked':
        if blockers:
            return f'{chapter_label}阻塞：{blockers[0]}'
        return f'{chapter_label}阻塞'
    if phase == 'proofreading' and phase_status == 'awaiting_user_review' and blockers:
        return f'{chapter_label}审核中：{blockers[0]}'

    summaries = {
        ('drafting', 'queued'): f'{chapter_label}待写',
        ('drafting', 'in_progress'): f'{chapter_label}初稿中',
        ('drafting', 'awaiting_user_review'): f'{chapter_label}初稿待审核',
        ('polishing', 'queued'): f'{chapter_label}待润色',
        ('polishing', 'in_progress'): f'{chapter_label}润色中',
        ('polishing', 'awaiting_user_review'): f'{chapter_label}润色待审核',
        ('proofreading', 'queued'): f'{chapter_label}待校对',
        ('proofreading', 'in_progress'): f'{chapter_label}校对中',
        ('proofreading', 'awaiting_user_review'): f'{chapter_label}审核中',
        ('proofreading', 'completed'): f'{chapter_label}已完成',
    }
    try:
        return summaries[(phase, phase_status)]
    except KeyError as exc:
        raise ValueError(f'unsupported summary state: {phase}/{phase_status}') from exc


def ensure_chapter_task(batch: dict, chapter_label: str) -> dict:
    normalize_progress_batch(batch)
    for task in batch['chapterTasks']:
        if task.get('chapterLabel') == chapter_label:
            return task
    task = chapter_task(chapter_label)
    batch['chapterTasks'].append(task)
    return task


def append_progress_event(
    batch: dict,
    chapter_label: str,
    phase: str,
    phase_status: str,
    summary: str,
    blockers: list[str] | None = None,
) -> dict:
    normalize_progress_batch(batch)
    created_at = now_iso()
    event = {
        'eventId': f'{phase}-{chapter_label}-{uuid4().hex}',
        'chapterLabel': chapter_label,
        'phase': phase,
        'phaseStatus': phase_status,
        'summary': summary,
        'blockers': list(blockers or []),
        'createdAt': created_at,
        'reportedAt': None,
    }
    batch['pendingProgressItems'].append(event)
    return event


def drop_pending_progress_for_chapter(batch: dict, chapter_label: str) -> dict:
    normalize_progress_batch(batch)
    batch['pendingProgressItems'] = [
        item
        for item in batch['pendingProgressItems']
        if not isinstance(item, dict) or item.get('chapterLabel') != chapter_label
    ]
    return batch


def has_pending_progress_event(
    batch: dict,
    chapter_label: str,
    phase: str,
    phase_status: str,
    summary: str,
    blockers: list[str] | None = None,
) -> bool:
    normalize_progress_batch(batch)
    expected_blockers = list(blockers or [])
    for item in batch['pendingProgressItems']:
        if not isinstance(item, dict):
            continue
        if item.get('chapterLabel') != chapter_label:
            continue
        if item.get('phase') != phase or item.get('phaseStatus') != phase_status:
            continue
        if item.get('summary') != summary:
            continue
        if list(item.get('blockers') or []) != expected_blockers:
            continue
        return True
    return False


def build_progress_report(events: list[dict]) -> dict:
    latest_by_chapter: dict[str, tuple[int, dict]] = {}

    for index, item in enumerate(events):
        if not isinstance(item, dict):
            continue
        if item.get('reportedAt') is not None:
            continue
        chapter_label = item.get('chapterLabel')
        if not chapter_label:
            continue
        latest_by_chapter[chapter_label] = (index, item)

    latest_events = sorted(
        latest_by_chapter.values(),
        key=lambda pair: ((pair[1].get('createdAt') or ''), pair[0]),
    )
    selected_events = [item for _, item in latest_events]

    return {
        'eventIds': [progress_event_id(item, index) for index, item in latest_events],
        'summary': '；'.join(item.get('summary') or '' for item in selected_events if item.get('summary')),
    }


def mark_progress_items_reported(batch: dict, event_ids: list[str]) -> list[str]:
    normalize_progress_batch(batch)
    requested = {event_id for event_id in event_ids if event_id}
    if not requested:
        return []

    reported_at = now_iso()
    marked: list[str] = []
    for index, item in enumerate(batch['pendingProgressItems']):
        if not isinstance(item, dict):
            continue
        event_id = progress_event_id(item, index)
        if event_id not in requested:
            continue
        if item.get('reportedAt') is not None:
            continue
        if not item.get('eventId'):
            item['eventId'] = event_id
        item['reportedAt'] = reported_at
        marked.append(event_id)
    return marked


def advance_chapters_after_gate(batch: dict, gate: str) -> dict:
    normalize_progress_batch(batch)
    transitions = {
        'waiting_draft_feedback': ('drafting', 'polishing', 'queued'),
        'waiting_polishing_feedback': ('polishing', 'proofreading', 'queued'),
        'waiting_proofreading_feedback': ('proofreading', 'proofreading', 'completed'),
    }
    transition = transitions.get(gate)
    if not transition:
        return batch

    current_phase, next_phase, next_status = transition
    timestamp = now_iso()
    for task in batch['chapterTasks']:
        if task.get('phase') != current_phase:
            continue
        if task.get('phaseStatus') != 'awaiting_user_review':
            continue
        chapter_label = task.get('chapterLabel')
        if not chapter_label:
            continue
        summary = human_summary(chapter_label, next_phase, next_status)
        task['phase'] = next_phase
        task['phaseStatus'] = next_status
        task['blockers'] = []
        task['lastSummary'] = summary
        task['updatedAt'] = timestamp
        append_progress_event(batch, chapter_label, next_phase, next_status, summary)
    return batch


def render_chapter_progress(batch: dict) -> str:
    normalize_progress_batch(batch)
    summaries = [task.get('lastSummary') for task in batch['chapterTasks'] if task.get('lastSummary')]
    return '；'.join(summaries) if summaries else '无'


def mark_dispatch_started(batch: dict, phase: str, chapter_labels: list[str], target_files: list[str]) -> dict:
    normalize_progress_batch(batch)
    timestamp = now_iso()

    manuscript_paths_by_label: dict[str, str] = {}
    if phase in {'drafting', 'polishing'}:
        if len(chapter_labels) != len(target_files):
            raise ValueError(f'{phase} dispatch target files must align 1:1 with chapter labels')
        for chapter_label, relpath in zip(chapter_labels, target_files):
            derived_label = chapter_label_from_manuscript_path(relpath)
            if derived_label and derived_label != chapter_label:
                raise ValueError(
                    f'target file chapter label mismatch for {relpath}: expected {chapter_label}, got {derived_label}'
                )
            manuscript_paths_by_label[chapter_label] = relpath

    for chapter_label in chapter_labels:
        task = ensure_chapter_task(batch, chapter_label)
        summary = human_summary(chapter_label, phase, 'in_progress')
        expected_manuscript_path = manuscript_paths_by_label.get(chapter_label, task.get('manuscriptPath'))
        task_needs_update = (
            task.get('phase') != phase
            or task.get('phaseStatus') != 'in_progress'
            or task.get('manuscriptPath') != expected_manuscript_path
            or task.get('lastSummary') != summary
            or list(task.get('blockers') or []) != []
        )
        if task_needs_update:
            task['phase'] = phase
            task['phaseStatus'] = 'in_progress'
            task['manuscriptPath'] = expected_manuscript_path
            task['lastSummary'] = summary
            task['blockers'] = []
            task['updatedAt'] = timestamp
        if not has_pending_progress_event(batch, chapter_label, phase, 'in_progress', summary):
            append_progress_event(batch, chapter_label, phase, 'in_progress', summary)

    return batch


def apply_result_to_chapters(
    batch: dict,
    phase: str,
    chapter_labels: list[str],
    target_files: list[str],
    result: dict,
) -> dict:
    normalize_progress_batch(batch)
    timestamp = now_iso()
    status = result.get('status')

    manuscript_paths_by_label: dict[str, str] = {}
    if phase in {'drafting', 'polishing'} and len(chapter_labels) == len(target_files):
        for chapter_label, relpath in zip(chapter_labels, target_files):
            derived_label = chapter_label_from_manuscript_path(relpath)
            if derived_label and derived_label != chapter_label:
                raise ValueError(
                    f'target file chapter label mismatch for {relpath}: expected {chapter_label}, got {derived_label}'
                )
            manuscript_paths_by_label[chapter_label] = relpath

    if status == 'completed':
        phase_status = 'awaiting_user_review'
        if phase == 'proofreading':
            blockers = list(result.get('blockers') or [])
        else:
            blockers = []
    elif status in {'blocked', 'needs_clarification'}:
        phase_status = 'blocked'
        blockers = list(result.get('blockedReasons') or [])
    else:
        raise ValueError(f'unsupported result status for chapter progress update: {status}')

    for chapter_label in chapter_labels:
        task = ensure_chapter_task(batch, chapter_label)
        manuscript_path = manuscript_paths_by_label.get(chapter_label, task.get('manuscriptPath'))
        summary = human_summary(chapter_label, phase, phase_status, blockers)
        task['phase'] = phase
        task['phaseStatus'] = phase_status
        task['manuscriptPath'] = manuscript_path
        task['blockers'] = list(blockers)
        task['lastSummary'] = summary
        task['updatedAt'] = timestamp
        drop_pending_progress_for_chapter(batch, chapter_label)
        if not has_pending_progress_event(batch, chapter_label, phase, phase_status, summary, blockers):
            append_progress_event(batch, chapter_label, phase, phase_status, summary, blockers)

    return batch
