#!/usr/bin/env python3
"""Upgrade an existing project to the current project-scaffold baseline."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OPENCLAW_CONFIG_PATH = Path.home() / '.openclaw' / 'openclaw.json'
PROJECT_ROUTING_PATH = ROOT / 'config' / 'project_routing.json'
CURRENT_SKILL_VERSION = '1.1.0'


def get_project_version(project_dir: Path) -> str:
    meta = project_dir / '.skill_version'
    if meta.exists():
        return meta.read_text(encoding='utf-8').strip()
    project_md = project_dir / 'PROJECT.md'
    if project_md.exists():
        for line in project_md.read_text(encoding='utf-8').splitlines():
            if 'Created' in line:
                return 'pre-1.0.0'
    return 'pre-1.0.0'


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8') if path.exists() else ''


def infer_project_name(project_dir: Path, project_key: str) -> str:
    project_md = project_dir / 'PROJECT.md'
    if project_md.exists():
        for line in project_md.read_text(encoding='utf-8').splitlines():
            if line.startswith('# Project: '):
                return line.split(':', 1)[1].strip()
    return project_key


def infer_description(project_dir: Path, project_key: str) -> str:
    project_md = project_dir / 'PROJECT.md'
    if project_md.exists():
        lines = project_md.read_text(encoding='utf-8').splitlines()
        for line in lines:
            if line.startswith('- **Description**: '):
                return line.split(':', 1)[1].strip()
        for idx, line in enumerate(lines):
            if line.strip() in {'## Purpose', '## Overview'} and idx + 1 < len(lines):
                nxt = lines[idx + 1].strip()
                if nxt:
                    return nxt
    return f'{project_key} automation project'


def load_routing() -> dict:
    if PROJECT_ROUTING_PATH.exists():
        return json.loads(PROJECT_ROUTING_PATH.read_text(encoding='utf-8'))
    return {'version': 1, 'routingGroups': {}, 'projects': {}}


def render_project_identity(ctx: dict) -> str:
    return f"""# PROJECT_IDENTITY

## project_id
{ctx['project_key']}

## project_name
{ctx['project_name']}

## what_this_project_is
{ctx['description']}

## what_this_project_is_not
- not a generic cross-project assistant
- not a substitute for other project facts
- not allowed to silently import assumptions from unrelated projects

## authoritative_surfaces
- project-local docs in this directory
- project-local workflows and logs
- routing entry in `config/project_routing.json`

## cross_project_guardrail
If another project has a similar pattern, treat it as analogy only and label it explicitly.
"""


def render_project_policy() -> str:
    return """# PROJECT_POLICY

## answering_rules
- project-scope-first
- use project-local facts before global memory
- do not import another project's facts as if they belong here
- if cross-project comparison is useful, label it as analogy

## routing_rules
- general topic is router-only
- report topic is for status, run results, and operational explanation
- chat topic is for project discussion, debugging, and repair

## escalation_rules
Escalate to main chat only when the issue affects shared layers, multiple projects, or system-wide rules.
"""


def render_group_profile(ctx: dict) -> str:
    return f"""# GROUP_PROFILE

## project_name
{ctx['project_name']}

## project_scope
{ctx['description']}

## my_role
Project-scoped conversation assistant and execution coordination surface

## bot_roster
1. Scheduler Bot: triggers cron workflows
2. Ops/Worker Bot: executes pipeline work
3. Project Assistant: answers inside project scope

## collaboration_entrypoints
Check project status, explain a report, inspect failures, discuss workflow behavior, and coordinate project-local fixes

## conversation_policy
- this group defaults to {ctx['project_key']} scope
- general topic routes, project topics answer
- project questions must not silently drift into another project's facts
"""


def write_if_missing(path: Path, content: str, changes: list[str], dry_run: bool) -> None:
    if path.exists():
        return
    changes.append(f'create {path.name}')
    if not dry_run:
        path.write_text(content, encoding='utf-8')


def ensure_project_files(project_dir: Path, ctx: dict, changes: list[str], dry_run: bool) -> None:
    write_if_missing(project_dir / 'PROJECT_IDENTITY.md', render_project_identity(ctx), changes, dry_run)
    write_if_missing(project_dir / 'PROJECT_POLICY.md', render_project_policy(), changes, dry_run)
    write_if_missing(project_dir / 'GROUP_PROFILE.md', render_group_profile(ctx), changes, dry_run)


def upgrade_routing(ctx: dict, changes: list[str], dry_run: bool) -> tuple[dict, bool]:
    data = load_routing()
    projects = data.setdefault('projects', {})
    groups = data.setdefault('routingGroups', {})
    project_cfg = projects.setdefault(ctx['project_key'], {})
    routing_group = project_cfg.get('routingGroup') or ctx['routing_group']
    group_cfg = groups.setdefault(routing_group, {})

    project_updates = {
        'routingGroup': routing_group,
        'syncToMain': project_cfg.get('syncToMain', 'exception-only'),
        'conversationScope': 'project-only',
        'primaryAssistant': ctx['assistant_id'],
        'generalAssistantMode': 'router-only',
    }
    group_updates = {
        'channel': group_cfg.get('channel', 'telegram'),
        'defaultTarget': group_cfg.get('defaultTarget', ctx['project_name']),
        'chatId': group_cfg.get('chatId', ctx['chat_id']),
        'threadId': group_cfg.get('threadId', ctx['report_thread_id']),
        'reportThreadId': group_cfg.get('reportThreadId', ctx['report_thread_id']),
        'chatThreadId': group_cfg.get('chatThreadId', ctx['chat_thread_id']),
        'generalThreadId': group_cfg.get('generalThreadId', ctx['general_thread_id']),
        'source': group_cfg.get('source', 'upgrade_project.py'),
        'projectId': ctx['project_key'],
        'contextGate': True,
        'routeMode': 'project-scoped',
        'assistantMap': {
            'general': 'main',
            'report': ctx['assistant_id'],
            'chat': ctx['assistant_id'],
        },
        'topicOwnership': {
            'general': {
                'ownerAgent': 'main',
                'projectScope': ctx['project_key'],
                'mode': 'router-only',
            },
            'report': {
                'ownerAgent': ctx['assistant_id'],
                'projectScope': ctx['project_key'],
                'mode': 'answering',
            },
            'chat': {
                'ownerAgent': ctx['assistant_id'],
                'projectScope': ctx['project_key'],
                'mode': 'answering',
            },
        },
    }
    changed = False
    for key, value in project_updates.items():
        if project_cfg.get(key) != value:
            project_cfg[key] = value
            changed = True
    for key, value in group_updates.items():
        if group_cfg.get(key) != value:
            group_cfg[key] = value
            changed = True
    if changed:
        changes.append('update config/project_routing.json with project-scoped conversation routing')
        if not dry_run:
            data['updatedAt'] = '2026-03-25T22:30:00+08:00'
            PROJECT_ROUTING_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return data, changed


def ensure_project_agent(ctx: dict, changes: list[str], dry_run: bool) -> None:
    if not OPENCLAW_CONFIG_PATH.exists():
        changes.append('skip project assistant registration: ~/.openclaw/openclaw.json missing')
        return
    agent_dir = Path.home() / '.openclaw' / 'agents' / ctx['assistant_id'] / 'agent'
    sessions_dir = Path.home() / '.openclaw' / 'agents' / ctx['assistant_id'] / 'sessions'
    main_agent_dir = Path.home() / '.openclaw' / 'agents' / 'main' / 'agent'

    for filename in ['auth-profiles.json', 'models.json']:
        dst = agent_dir / filename
        if not dst.exists() and (main_agent_dir / filename).exists():
            changes.append(f'create assistant runtime file {dst}')
            if not dry_run:
                agent_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(main_agent_dir / filename, dst)

    sessions_json = sessions_dir / 'sessions.json'
    if not sessions_json.exists():
        changes.append(f'create assistant session registry {sessions_json}')
        if not dry_run:
            sessions_dir.mkdir(parents=True, exist_ok=True)
            sessions_json.write_text('{"version":1,"sessions":[]}\n', encoding='utf-8')

    data = json.loads(OPENCLAW_CONFIG_PATH.read_text(encoding='utf-8'))
    agents = data.setdefault('agents', {}).setdefault('list', [])
    if not any(a.get('id') == ctx['assistant_id'] for a in agents):
        agents.append({
            'id': ctx['assistant_id'],
            'name': ctx['assistant_id'],
            'workspace': str(ctx['project_dir']),
            'agentDir': str(agent_dir),
            'model': 'minimax-portal/MiniMax-M2.5',
            'identity': {
                'name': f"{ctx['project_name']} Chat",
                'emoji': '🧭',
            },
        })
        changes.append(f'register project assistant {ctx["assistant_id"]} in ~/.openclaw/openclaw.json')
        if not dry_run:
            OPENCLAW_CONFIG_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def upgrade_openclaw_group(ctx: dict, routing: dict, changes: list[str], dry_run: bool) -> None:
    if not OPENCLAW_CONFIG_PATH.exists() or not ctx['chat_id']:
        changes.append('skip Telegram group upgrade: missing openclaw config or chat_id')
        return

    shared_projects = [k for k, v in routing.get('projects', {}).items() if v.get('routingGroup') == ctx['routing_group']]
    if len(shared_projects) > 1:
        changes.append(f'skip topic rebinding for shared routing group {ctx["routing_group"]}: manual upgrade required ({", ".join(shared_projects)})')
        return

    data = json.loads(OPENCLAW_CONFIG_PATH.read_text(encoding='utf-8'))
    group = data.setdefault('channels', {}).setdefault('telegram', {}).setdefault('groups', {}).setdefault(ctx['chat_id'], {})
    desired = {
        'requireMention': False,
        'projectId': ctx['project_key'],
        'contextGate': True,
        'assistantRoutingMode': 'project-scoped',
        'topics': {
            ctx['general_thread_id']: {
                'requireMention': True,
                'systemPrompt': (
                    f"This is the general topic for the {ctx['project_key']} project. "
                    "You are acting as a router only. Do not answer project facts directly unless the user asks a pure routing question. "
                    "For project questions, direct the user to the project chat topic and keep the answer short."
                ),
                'agentId': 'main',
            },
            ctx['report_thread_id']: {
                'requireMention': False,
                'systemPrompt': (
                    f"This is the report topic for the {ctx['project_key']} project. "
                    "Answer inside project scope only. Apply a context gate before answering: use project-local documents, workflows, and logs first. "
                    "If a similar pattern exists in another project, label it explicitly as analogy instead of fact."
                ),
                'agentId': ctx['assistant_id'],
            },
            ctx['chat_thread_id']: {
                'requireMention': False,
                'systemPrompt': (
                    f"This is the chat topic for the {ctx['project_key']} project. "
                    "Answer as the dedicated project assistant. Use project-local facts, workflows, logs, and policies first. "
                    "Do not substitute facts from another project. If cross-project experience is useful, label it as analogy."
                ),
                'agentId': ctx['assistant_id'],
            },
        },
    }

    changed = False
    for key, value in desired.items():
        if group.get(key) != value:
            group[key] = value
            changed = True
    if changed:
        changes.append(f'update ~/.openclaw/openclaw.json group routing for {ctx["project_key"]}')
        if not dry_run:
            OPENCLAW_CONFIG_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def build_context(project_dir: Path) -> dict:
    project_key = project_dir.name
    routing = load_routing()
    project_cfg = routing.get('projects', {}).get(project_key, {})
    routing_group = project_cfg.get('routingGroup', f'{project_key}-group')
    group_cfg = routing.get('routingGroups', {}).get(routing_group, {})
    return {
        'project_dir': project_dir,
        'project_key': project_key,
        'project_name': infer_project_name(project_dir, project_key),
        'description': infer_description(project_dir, project_key),
        'routing_group': routing_group,
        'chat_id': str(group_cfg.get('chatId', '')),
        'general_thread_id': str(group_cfg.get('generalThreadId', '1')),
        'report_thread_id': str(group_cfg.get('reportThreadId', group_cfg.get('threadId', '2'))),
        'chat_thread_id': str(group_cfg.get('chatThreadId', '3')),
        'assistant_id': project_cfg.get('primaryAssistant', f'{project_key}-chat'),
    }


def apply_upgrade(project_dir: Path, from_version: str, dry_run: bool = False) -> list[str]:
    changes: list[str] = []
    ctx = build_context(project_dir)
    ensure_project_files(project_dir, ctx, changes, dry_run)
    routing, _ = upgrade_routing(ctx, changes, dry_run)
    ensure_project_agent(ctx, changes, dry_run)
    upgrade_openclaw_group(ctx, routing, changes, dry_run)
    if not dry_run:
        (project_dir / '.skill_version').write_text(CURRENT_SKILL_VERSION, encoding='utf-8')
    changes.append(f'set .skill_version -> {CURRENT_SKILL_VERSION}')
    return changes


def main() -> None:
    parser = argparse.ArgumentParser(description='Upgrade project to current skill version')
    parser.add_argument('--project-key', default=None, help='Project to upgrade (default: this project)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would change without applying')
    args = parser.parse_args()

    if args.project_key:
        project_dir = ROOT / 'projects' / args.project_key
    else:
        project_dir = Path(__file__).resolve().parents[2]

    project_key = project_dir.name
    print(f'=== Upgrade Check: {project_key} ===')

    if not project_dir.exists():
        print(f'ERROR: Project not found: {project_dir}')
        sys.exit(1)

    current_version = get_project_version(project_dir)
    print(f'  Project version: {current_version}')
    print(f'  Current skill version: {CURRENT_SKILL_VERSION}')

    if current_version == CURRENT_SKILL_VERSION:
        print('  ✅ Already up to date')
        sys.exit(0)

    print(f'\n  Upgrading {current_version} → {CURRENT_SKILL_VERSION}...')
    changes = apply_upgrade(project_dir, current_version, dry_run=args.dry_run)

    if args.dry_run:
        print(f'\n  [DRY RUN] Would apply {len(changes)} change(s):')
    else:
        print(f'\n  ✅ Applied {len(changes)} change(s):')
    for c in changes:
        print(f'    - {c}')


if __name__ == '__main__':
    main()
