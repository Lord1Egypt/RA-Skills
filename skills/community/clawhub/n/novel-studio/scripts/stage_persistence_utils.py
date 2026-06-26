from __future__ import annotations

from datetime import datetime, timezone

PROOFREADING_REPORT = '05A_本轮校对报告.md'
WORKFLOW_STATUSES = {
    'collecting_inputs',
    'producing_artifact',
    'awaiting_user_approval',
    'brainstorming',
    'blocked',
}
STAGE_REVIEW_GATES = {
    'discovery': 'waiting_discovery_feedback',
    'story-planning': 'waiting_planning_feedback',
    'character-system': 'waiting_character_feedback',
    'drafting': 'waiting_draft_feedback',
    'polishing': 'waiting_polishing_feedback',
    'proofreading': 'waiting_proofreading_feedback',
    'final-review': 'waiting_final_review_feedback',
}
DOCUMENT_STAGE_ARTIFACTS = {
    'discovery': {
        '00A_热点扫描.md',
        '00B_用户偏好.md',
        '00C_底盘与切口决策.md',
        '00_选题报告.md',
    },
    'story-planning': {
        '01_想法.md',
        '02_大纲.md',
        '04_章节骨架.md',
    },
    'character-system': {'03_人物小传.md'},
    'final-review': {'07_终审报告.md'},
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def gate_for_stage(stage: str, substage: str | None = None) -> str:
    if stage == 'drafting' and substage in {'opening-design', 'opening-review'}:
        return 'waiting_opening_feedback'
    return STAGE_REVIEW_GATES[stage]


def normalize_path_list(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    normalized = []
    for value in values:
        if isinstance(value, str) and value.strip():
            normalized.append(value.strip())
    return normalized


def document_stage_targets(stage: str, substage: str | None = None) -> set[str]:
    if stage == 'drafting' and substage in {'opening-design', 'opening-review'}:
        return {'04A_开篇设计.md', '05_本轮章节规划.md'}
    return DOCUMENT_STAGE_ARTIFACTS.get(stage, set())


def allow_character_file(stage: str, relpath: str) -> bool:
    return stage == 'character-system' and relpath.startswith('characters/') and relpath.endswith('.md')


def validate_artifact_updates(stage: str, artifact_updates: dict[str, str], substage: str | None = None) -> dict[str, str]:
    if not isinstance(artifact_updates, dict):
        raise ValueError('artifactUpdates must be an object')

    allowed = document_stage_targets(stage, substage)
    normalized = {}
    for relpath, text in artifact_updates.items():
        if not isinstance(relpath, str) or not relpath.strip():
            raise ValueError('artifact path must be a non-empty string')
        if relpath not in allowed and not allow_character_file(stage, relpath):
            raise ValueError(f'out-of-scope artifact for {stage}: {relpath}')
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f'artifact content cannot be empty: {relpath}')
        normalized[relpath] = text
    return normalized


def branch_state_key(stage: str, branch_id: str) -> str:
    return f'{stage}/{branch_id}'
