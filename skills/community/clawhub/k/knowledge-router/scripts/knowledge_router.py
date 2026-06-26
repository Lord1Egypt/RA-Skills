#!/usr/bin/env python3
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import os
import re

WORKSPACE = Path.cwd()
SELF_IMPROVING = Path.home() / 'self-improving'

@dataclass
class Source:
    path: str
    source_type: str
    summary: str
    preview: str = ''


def preview_text(path: Path, max_lines: int = 12) -> str:
    try:
        lines = path.read_text(errors='ignore').splitlines()
        return '\n'.join(lines[:max_lines])
    except Exception:
        return ''


def collect_sources(scope: str) -> List[Source]:
    sources: List[Source] = []
    p = WORKSPACE / 'MEMORY.md'
    if p.exists():
        sources.append(Source('MEMORY.md', 'stable-rule', 'Long-term defaults and durable operating rules.', preview_text(p)))

    mem_dir = WORKSPACE / 'memory'
    if mem_dir.exists() and scope in {'default', 'memory-only'}:
        for fp in sorted(mem_dir.glob('*.md'))[-8:]:
            sources.append(Source(str(fp.relative_to(WORKSPACE)), 'daily-fact', 'Dated event log, project progress, and recent factual history.', preview_text(fp)))

    if SELF_IMPROVING.exists() and scope in {'default', 'improvement-only'}:
        for fp in sorted(SELF_IMPROVING.glob('*.md'))[:10]:
            sources.append(Source(str(fp), 'improvement', 'Workflow improvement notes, corrections, and reusable lessons.', preview_text(fp)))

    if scope in {'default', 'skills-only'}:
        for fp in sorted((WORKSPACE / 'skills').glob('*/references/*.md'))[:80]:
            sources.append(Source(str(fp.relative_to(WORKSPACE)), 'method', 'Reusable method/reference knowledge from a skill.', preview_text(fp)))
        for fp in sorted((WORKSPACE / 'skills').glob('*/SKILL.md'))[:80]:
            sources.append(Source(str(fp.relative_to(WORKSPACE)), 'method', 'Skill-level guidance and workflow entry point.', preview_text(fp)))

    if scope in {'default', 'audit-only'}:
        audit = WORKSPACE / 'logs' / 'audit'
        if audit.exists():
            for fp in sorted(audit.glob('*.jsonl'))[-5:]:
                sources.append(Source(str(fp.relative_to(WORKSPACE)), 'evidence', 'Primary operational evidence log with dated high-value actions.', preview_text(fp)))
            for name in ['latest.md', 'index.json', 'by-target.json', 'by-risk.json', 'open-items.json', 'open-items-history.json']:
                fp = audit / name
                if fp.exists():
                    sources.append(Source(str(fp.relative_to(WORKSPACE)), 'evidence', 'Operational evidence or audit index.', preview_text(fp)))
            for fp in sorted(audit.glob('README*.md'))[:10]:
                sources.append(Source(str(fp.relative_to(WORKSPACE)), 'evidence', 'Audit structure or evidence-oriented operational documentation.', preview_text(fp)))
    return sources


def infer_intent(query: str) -> str:
    q = query.lower()
    if any(x in q for x in ['证据', '记录', '有没有做过', '是否做过', '改成 private', '改成 public', '可见性', '发布过', '仓库是不是', 'evidence']):
        return 'evidence'
    if any(x in q for x in ['以后', '减少折腾', '更稳', '避免', '复盘', '改进', '优化', '怎么做更好', 'improve']):
        return 'improvement'
    if any(x in q for x in ['什么时候', '何时', '最近', '状态', '发生了什么', '之前怎么处理', '上次怎么处理', '现在状态', 'when']):
        return 'fact'
    if any(x in q for x in ['怎么做', '流程', '怎么用', '方法', 'workflow', 'how to']):
        return 'method'
    return 'rule'


def source_score(query: str, intent: str, source: Source) -> int:
    q = query.lower()
    p = source.path.lower()
    score = 0
    if intent == 'rule' and source.source_type == 'stable-rule':
        score += 100
    if intent == 'fact' and source.source_type == 'daily-fact':
        score += 100
    if intent == 'method' and source.source_type == 'method':
        score += 100
    if intent == 'evidence' and source.source_type == 'evidence':
        score += 100
    if intent == 'improvement' and source.source_type == 'improvement':
        score += 100

    keywords = [k for k in re.split(r'[^\w\u4e00-\u9fff-]+', q) if len(k) >= 2]
    score += sum(8 for k in keywords if k in p)
    preview_lower = source.preview.lower()
    score += sum(5 for k in keywords if k in preview_lower)

    if intent == 'evidence':
        if p.endswith('.jsonl'):
            score += 30
        if 'latest.md' in p or 'by-target.json' in p:
            score += 15
        if 'readme' in p:
            score -= 10
    if intent == 'fact':
        if re.search(r'2026-03-1[01]', p):
            score += 10
    return score


def rank_sources(intent: str, sources: List[Source], query: str) -> Tuple[List[Source], List[Source], List[str]]:
    primary_types = {
        'rule': ['stable-rule'],
        'fact': ['daily-fact'],
        'method': ['method'],
        'evidence': ['evidence'],
        'improvement': ['improvement'],
    }[intent]
    secondary_types = {
        'rule': ['improvement', 'method'],
        'fact': ['evidence'],
        'method': ['stable-rule'],
        'evidence': ['daily-fact'],
        'improvement': ['stable-rule', 'method'],
    }[intent]
    primary = sorted([s for s in sources if s.source_type in primary_types], key=lambda s: source_score(query, intent, s), reverse=True)[:5]
    secondary = sorted([s for s in sources if s.source_type in secondary_types], key=lambda s: source_score(query, intent, s), reverse=True)[:5]
    why = [
        f'Primary sources match the `{intent}` intent most directly.',
        'Ranking prefers more query-relevant files within the right source type before broader supporting material.'
    ]
    return primary, secondary, why


def promotion_hints(query: str, sources: List[Source]) -> List[str]:
    hints = []
    daily = [s for s in sources if s.source_type == 'daily-fact']
    methods = [s for s in sources if s.source_type == 'method']
    if len(daily) >= 3 and re.search(r'publish|发布|workflow|流程|clawhub', query, re.I):
        hints.append('This topic appears suited for extraction into a reusable publishing reference if it keeps recurring in daily memory.')
    if len(methods) == 0:
        hints.append('No reusable method source was found in the current scope; consider extracting one if this topic is recurring.')
    return hints


def render(query: str, intent: str, primary: List[Source], secondary: List[Source], why: List[str], hints: List[str]) -> str:
    lines = [
        'Knowledge Router Report',
        f'Query: {query}',
        f'Intent: {intent}',
        '',
        'Primary sources',
    ]
    lines.extend([f'- {s.path} [{s.source_type}] — {s.summary}' for s in primary] or ['- None found.'])
    lines += ['', 'Secondary sources']
    lines.extend([f'- {s.path} [{s.source_type}] — {s.summary}' for s in secondary] or ['- None found.'])
    lines += ['', 'Why']
    lines.extend([f'- {x}' for x in why])
    lines += ['', 'Promotion hints']
    lines.extend([f'- {x}' for x in hints] or ['- None.'])
    return '\n'.join(lines) + '\n'


def main() -> int:
    ap = argparse.ArgumentParser(description='Route a query to the right knowledge layer.')
    ap.add_argument('query')
    ap.add_argument('--scope', choices=['default', 'memory-only', 'skills-only', 'audit-only', 'improvement-only'], default='default')
    ap.add_argument('--output')
    args = ap.parse_args()

    sources = collect_sources(args.scope)
    intent = infer_intent(args.query)
    primary, secondary, why = rank_sources(intent, sources, args.query)
    hints = promotion_hints(args.query, sources)
    report = render(args.query, intent, primary, secondary, why, hints)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report)
    print(report, end='')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
