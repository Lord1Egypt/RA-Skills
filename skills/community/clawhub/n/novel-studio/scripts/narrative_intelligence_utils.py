#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from revision_utils import default_narrative_intelligence

TIMELINE_ARTIFACT = '05F_时间与事件图谱.md'
FORESHADOW_TRIPLES_ARTIFACT = '05G_伏笔三元组账本.md'
THEORY_OF_MIND_ARTIFACT = '05H_角色认知与误判表.md'
CONSISTENCY_ARTIFACT = '05I_证据链与矛盾对照表.md'

NARRATIVE_ARTIFACT_TEMPLATES = {
    TIMELINE_ARTIFACT: """# 05F_时间与事件图谱

## 使用说明
- 记录关键事件、发生时间、视角差与顺序依赖

## 事件表
| 事件 | 时间锚点 | 涉及章节 | 备注 |
| --- | --- | --- | --- |
""",
    FORESHADOW_TRIPLES_ARTIFACT: """# 05G_伏笔三元组账本

## 使用说明
- 按“埋设-触发-回收”跟踪伏笔闭环

## 三元组表
| 埋设 | 触发条件 | 回收 | 状态 |
| --- | --- | --- | --- |
""",
    THEORY_OF_MIND_ARTIFACT: """# 05H_角色认知与误判表

## 使用说明
- 记录角色所知、误判来源与认知差带来的剧情压力

## 认知表
| 角色 | 当前认知 | 误判/盲区 | 对应章节 |
| --- | --- | --- | --- |
""",
    CONSISTENCY_ARTIFACT: """# 05I_证据链与矛盾对照表

## 使用说明
- 对照主张、证据、矛盾点与待核查风险

## 对照表
| 主张/事实 | 证据链 | 潜在矛盾 | 处理状态 |
| --- | --- | --- | --- |
""",
}


def ensure_narrative_artifacts(project: Path) -> list[str]:
    project = Path(project).expanduser()
    created: list[str] = []

    for filename, template in NARRATIVE_ARTIFACT_TEMPLATES.items():
        artifact = project / filename
        if artifact.exists() and artifact.is_file() and artifact.read_text(encoding='utf-8').strip():
            continue
        artifact.write_text(template, encoding='utf-8')
        created.append(filename)

    return created


def sync_narrative_intelligence(project: Path, state: dict, *, stage: str, chapter_labels: list[str]) -> dict:
    ensure_narrative_artifacts(project)

    narrative_intelligence = state.setdefault('narrativeIntelligence', default_narrative_intelligence())
    timeline = narrative_intelligence.setdefault('timeline', default_narrative_intelligence()['timeline'])
    cfpg = narrative_intelligence.setdefault('cfpg', default_narrative_intelligence()['cfpg'])
    theory_of_mind = narrative_intelligence.setdefault(
        'theoryOfMind',
        default_narrative_intelligence()['theoryOfMind'],
    )
    consistency = narrative_intelligence.setdefault('consistency', default_narrative_intelligence()['consistency'])

    batch_range = state.get('batch', {}).get('lastDelegatedScope') or state.get('batch', {}).get('chapterRange')
    normalized_chapter_labels = list(chapter_labels)

    timeline['enabled'] = True
    timeline['lastUpdatedBatch'] = batch_range
    timeline['lastTouchedChapters'] = normalized_chapter_labels
    cfpg['lastUpdatedBatch'] = batch_range
    theory_of_mind['lastUpdatedBatch'] = batch_range

    if stage == 'proofreading':
        consistency['lastCheckStage'] = 'proofreading'

    return state
