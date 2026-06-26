#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from pathlib import Path

from autopilot_utils import stop_autopilot_with_blockers
from narrative_intelligence_utils import (
    CONSISTENCY_ARTIFACT,
    FORESHADOW_TRIPLES_ARTIFACT,
    ensure_narrative_artifacts,
)
from revision_utils import default_narrative_intelligence

CHAPTER_PLAN_ARTIFACT = '05_本轮章节规划.md'


def _normalized_text(value: object) -> str | None:
    text = str(value).strip() if value is not None else ''
    return text or None


def _parse_inline_fields(line: str) -> dict[str, str]:
    payload = line.strip()
    if payload.startswith('- '):
        payload = payload[2:].strip()

    fields: dict[str, str] = {}
    for chunk in payload.split('|'):
        key, separator, value = chunk.partition(':')
        if not separator:
            continue
        normalized_key = key.strip()
        normalized_value = value.strip()
        if normalized_key:
            fields[normalized_key] = normalized_value
    return fields


def load_foreshadow_triples(project: Path, state: dict) -> list[dict[str, str | None]]:
    narrative_intelligence = state.setdefault('narrativeIntelligence', default_narrative_intelligence())
    cfpg = narrative_intelligence.setdefault('cfpg', default_narrative_intelligence()['cfpg'])
    artifact = Path(project) / FORESHADOW_TRIPLES_ARTIFACT

    triples = list(cfpg.get('foreshadowTriples') or [])
    if artifact.exists() and artifact.is_file():
        parsed_triples: list[dict[str, str | None]] = []
        for raw_line in artifact.read_text(encoding='utf-8').splitlines():
            line = raw_line.strip()
            if not line.startswith('- id:'):
                continue
            fields = _parse_inline_fields(line)
            parsed_triples.append(
                {
                    'id': _normalized_text(fields.get('id')),
                    'status': _normalized_text(fields.get('status')),
                    'cause': _normalized_text(fields.get('cause')),
                    'promise': _normalized_text(fields.get('promise')),
                    'payoff': _normalized_text(fields.get('payoff')),
                }
            )
        if parsed_triples:
            triples = parsed_triples

    cfpg['foreshadowTriples'] = triples
    status_counts = {
        'pending': 0,
        'fulfilled': 0,
        'broken': 0,
        'expired': 0,
    }
    for triple in triples:
        status = (triple.get('status') or '').strip().lower()
        if status in status_counts:
            status_counts[status] += 1
    cfpg['tripleCounts'] = {
        'total': len(triples),
        **status_counts,
    }
    return triples


def _issue_summary(triple: dict[str, str | None]) -> str:
    triple_id = triple.get('id') or 'unknown'
    payoff = (triple.get('payoff') or '').strip()
    promise = (triple.get('promise') or '').strip()
    status = (triple.get('status') or '').strip().lower()
    suffix = '已过期' if status == 'expired' else '已断裂'

    if payoff in {'', '无'}:
        detail = '缺少 payoff 证据链'
    elif promise:
        detail = promise
    else:
        detail = '关键伏笔未闭环'
    return f'伏笔 {triple_id} {suffix}：{detail}'


def _extract_plan_points(project: Path, prefix: str) -> list[str]:
    artifact = Path(project) / CHAPTER_PLAN_ARTIFACT
    if not artifact.exists() or not artifact.is_file():
        return []

    values: list[str] = []
    for raw_line in artifact.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line.startswith(prefix):
            continue
        value = _normalized_text(line.partition('：')[2])
        if value is not None:
            values.append(value)
    return values


def build_cliche_findings(project: Path) -> list[str]:
    findings: list[str] = []
    duplicate_groups = (
        ('- 本章吸引点：', '重复吸引点'),
        ('- 高潮点：', '重复高潮点'),
    )

    for prefix, label in duplicate_groups:
        counts = Counter(_extract_plan_points(project, prefix))
        for value in counts:
            if counts[value] > 1:
                findings.append(f'{label}：{value}')
    return findings


def build_consistency_findings(project: Path, state: dict) -> dict[str, list[object]]:
    findings: dict[str, list[object]] = {
        'contradictionCandidates': [],
        'evidenceChains': [],
        'openCriticalIssues': [],
    }
    for triple in load_foreshadow_triples(project, state):
        status = (triple.get('status') or '').strip().lower()
        if status not in {'broken', 'expired'}:
            continue

        issue = _issue_summary(triple)
        triple_id = triple.get('id') or 'unknown'
        findings['contradictionCandidates'].append(
            {
                'id': triple_id,
                'type': 'cfpg',
                'severity': 'critical',
                'summary': issue,
            }
        )
        findings['evidenceChains'].append(
            {
                'id': f'chain-{triple_id}',
                'summary': issue,
                'evidence': [
                    f"cause={triple.get('cause') or '无'}",
                    f"promise={triple.get('promise') or '无'}",
                    f"payoff={triple.get('payoff') or '无'}",
                ],
            }
        )
        findings['openCriticalIssues'].append(issue)

    return findings


def render_consistency_report(findings: dict[str, list[object]]) -> str:
    contradiction_lines = findings['contradictionCandidates']
    evidence_chains = findings['evidenceChains']
    critical_issues = findings['openCriticalIssues']

    contradiction_block = (
        ''.join(f"- [{item['severity']}] {item['summary']}\n" for item in contradiction_lines)
        if contradiction_lines
        else '- 无\n'
    )
    evidence_block = (
        ''.join(
            '- {summary}\n  - {evidence}\n'.format(
                summary=item['summary'],
                evidence='; '.join(item['evidence']),
            )
            for item in evidence_chains
        )
        if evidence_chains
        else '- 无\n'
    )
    issue_block = ''.join(f'- {item}\n' for item in critical_issues) if critical_issues else '- 无\n'

    return (
        '# 05I_证据链与矛盾对照表\n\n'
        '## 当前矛盾配对\n'
        f'{contradiction_block}\n'
        '## 当前证据链\n'
        f'{evidence_block}\n'
        '## 当前关键问题\n'
        f'{issue_block}'
    )


def refresh_consistency_findings(project: Path, state: dict) -> dict[str, list[object]]:
    ensure_narrative_artifacts(project)
    findings = build_consistency_findings(project, state)
    narrative_intelligence = state.setdefault('narrativeIntelligence', default_narrative_intelligence())
    consistency = narrative_intelligence.setdefault('consistency', default_narrative_intelligence()['consistency'])
    consistency.update(findings)
    consistency['lastCheckStage'] = 'proofreading'

    (Path(project) / CONSISTENCY_ARTIFACT).write_text(
        render_consistency_report(findings),
        encoding='utf-8',
    )

    if findings['openCriticalIssues']:
        stop_autopilot_with_blockers(
            state,
            blocked_reasons=[str(item) for item in findings['openCriticalIssues']],
            summary='narrative consistency critical issue',
        )

    return findings


def refresh_cliche_findings(project: Path, state: dict) -> list[str]:
    narrative_intelligence = state.setdefault('narrativeIntelligence', default_narrative_intelligence())
    style_risk = narrative_intelligence.setdefault('styleRisk', default_narrative_intelligence()['styleRisk'])
    style_risk['clichePatterns'] = build_cliche_findings(project)
    style_risk['lastClicheScanStage'] = 'proofreading'
    return list(style_risk['clichePatterns'])


def build_revision_actions(state: dict) -> list[dict[str, str]]:
    actions: list[dict[str, str]] = []
    for issue in state.get('narrativeIntelligence', {}).get('consistency', {}).get('openCriticalIssues', []):
        summary = str(issue).strip()
        if not summary:
            continue
        actions.append(
            {
                'summary': summary,
                'action': f'先修 {summary} 对应正文，再回填 05I_证据链与矛盾对照表.md',
                'targetFile': CONSISTENCY_ARTIFACT,
            }
        )
    return actions
