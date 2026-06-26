#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path
from typing import Any

HOME = Path.home()
DEFAULT_OPENCLAW_DIR = HOME / '.openclaw'
DEFAULT_WORKSPACE = DEFAULT_OPENCLAW_DIR / 'workspace'
DEFAULT_CONFIG = DEFAULT_OPENCLAW_DIR / 'openclaw.json'

WIKI_EXCLUDE_DIRS = {
    '.openclaw-wiki/cache',
    '.openclaw-wiki/locks',
}
WIKI_EXCLUDE_FILES = {
    '.openclaw-wiki/log.jsonl',
}
DREAMS_EXCLUDE_DIRS = {
    'memory/.dreams/session-corpus',
}


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def get_path(obj: dict[str, Any] | None, path: list[str], default=None):
    cur = obj
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() not in {'', '0', 'false', 'no', 'off', 'null'}
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) > 0
    return True


def expand_path(raw: str | None, base: Path) -> Path | None:
    if not raw:
        return None
    p = Path(os.path.expanduser(raw))
    if not p.is_absolute():
        p = (base / p).resolve()
    return p


def rel_to_workspace(path: Path, workspace: Path) -> str:
    try:
        return str(path.resolve().relative_to(workspace.resolve()))
    except Exception:
        return str(path.resolve())


def candidate(path: Path, workspace: Path, system: str, reason: str) -> dict[str, Any]:
    return {
        'path': str(path.resolve()),
        'displayPath': rel_to_workspace(path, workspace),
        'kind': 'dir' if path.is_dir() else 'file',
        'system': system,
        'reason': reason,
    }


def exclusion(path: str, reason: str) -> dict[str, str]:
    return {'path': path, 'reason': reason}


def list_memory_daily(memory_dir: Path) -> list[str]:
    if not memory_dir.exists():
        return []
    return sorted(str(p.resolve()) for p in memory_dir.glob('*.md') if p.is_file())


def build_candidates(workspace: Path, wiki_path: Path, active_memory_enabled: bool) -> tuple[list[dict[str, Any]], list[dict[str, str]], list[str]]:
    candidates: list[dict[str, Any]] = []
    excluded: list[dict[str, str]] = []
    notes: list[str] = []

    memory_md = workspace / 'MEMORY.md'
    memory_dir = workspace / 'memory'
    dreams_md = workspace / 'DREAMS.md'
    dreams_dir = memory_dir / '.dreams'
    dreaming_dir = memory_dir / 'dreaming'

    if memory_md.exists():
        candidates.append(candidate(memory_md, workspace, 'coreMemory', 'long-term memory'))
    if memory_dir.exists():
        for daily in sorted(memory_dir.glob('*.md')):
            if daily.is_file():
                candidates.append(candidate(daily, workspace, 'coreMemory', 'daily or durable markdown memory'))

    if dreams_md.exists():
        candidates.append(candidate(dreams_md, workspace, 'dreaming', 'human-readable dream diary'))
    if dreams_dir.exists():
        for name in ['short-term-recall.json', 'phase-signals.json', 'daily-ingestion.json', 'session-ingestion.json', 'events.jsonl']:
            p = dreams_dir / name
            if p.exists():
                candidates.append(candidate(p, workspace, 'dreaming', 'dreaming durable machine state'))
        session_corpus = dreams_dir / 'session-corpus'
        if session_corpus.exists():
            excluded.append(exclusion(rel_to_workspace(session_corpus, workspace), 'transcript-derived dreaming corpus excluded by default'))
    if dreaming_dir.exists():
        candidates.append(candidate(dreaming_dir, workspace, 'dreaming', 'phase reports and durable dreaming outputs'))

    if wiki_path.exists():
        for name in ['AGENTS.md', 'WIKI.md', 'index.md', 'inbox.md']:
            p = wiki_path / name
            if p.exists():
                candidates.append(candidate(p, workspace, 'memoryWiki', 'wiki root content'))
        for name in ['entities', 'concepts', 'syntheses', 'sources', 'reports', '_attachments', '_views']:
            p = wiki_path / name
            if p.exists():
                candidates.append(candidate(p, workspace, 'memoryWiki', 'durable wiki vault content'))
        state_file = wiki_path / '.openclaw-wiki' / 'state.json'
        if state_file.exists():
            candidates.append(candidate(state_file, workspace, 'memoryWiki', 'minimal wiki metadata state'))
        for rel in sorted(WIKI_EXCLUDE_DIRS):
            p = wiki_path / rel
            if p.exists():
                excluded.append(exclusion(rel_to_workspace(p, workspace), 'wiki cache/lock data excluded by default'))
        for rel in sorted(WIKI_EXCLUDE_FILES):
            p = wiki_path / rel
            if p.exists():
                excluded.append(exclusion(rel_to_workspace(p, workspace), 'wiki log excluded by default'))

    if active_memory_enabled:
        notes.append('active-memory enabled; no durable active-memory file path auto-detected')

    return candidates, excluded, notes


def summarize_system(enabled: bool, paths: list[str]) -> dict[str, Any]:
    return {'enabled': enabled, 'present': bool(paths), 'paths': paths}


def main() -> int:
    parser = argparse.ArgumentParser(description='Discover OpenClaw memory artifacts suitable for backup.')
    parser.add_argument('--workspace', default=os.environ.get('OPENCLAW_WORKSPACE', str(DEFAULT_WORKSPACE)))
    parser.add_argument('--config', default=os.environ.get('OPENCLAW_CONFIG', str(DEFAULT_CONFIG)))
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    config_path = Path(args.config).expanduser().resolve()
    config = load_json(config_path) if config_path.exists() else None

    plugins = get_path(config, ['plugins', 'entries'], {}) or {}
    active_memory_cfg = plugins.get('active-memory', {}) if isinstance(plugins, dict) else {}
    memory_core_cfg = plugins.get('memory-core', {}) if isinstance(plugins, dict) else {}
    memory_wiki_cfg = plugins.get('memory-wiki', {}) if isinstance(plugins, dict) else {}

    wiki_cfg = memory_wiki_cfg.get('config', {}) if isinstance(memory_wiki_cfg, dict) else {}
    wiki_enabled = truthy(memory_wiki_cfg.get('enabled'))
    wiki_path = expand_path(get_path(wiki_cfg, ['vault', 'path']), DEFAULT_OPENCLAW_DIR / 'wiki' / 'main')
    if wiki_path is None:
        wiki_path = DEFAULT_OPENCLAW_DIR / 'wiki' / 'main'

    dreaming_cfg = get_path(memory_core_cfg, ['config', 'dreaming'], {}) or {}
    active_memory_enabled = truthy(active_memory_cfg.get('enabled'))

    candidates, excluded_by_policy, notes = build_candidates(workspace, wiki_path, active_memory_enabled)
    detected = {
        'coreMemory': summarize_system(True, [c['path'] for c in candidates if c['system'] == 'coreMemory']),
        'dreaming': summarize_system(truthy(dreaming_cfg.get('enabled')), [c['path'] for c in candidates if c['system'] == 'dreaming']),
        'memoryWiki': {
            **summarize_system(wiki_enabled, [c['path'] for c in candidates if c['system'] == 'memoryWiki']),
            'vaultMode': get_path(wiki_cfg, ['vaultMode']),
        },
        'activeMemory': summarize_system(active_memory_enabled, []),
    }

    result = {
        'workspace': str(workspace),
        'configInspected': [str(config_path)] if config_path.exists() else [],
        'detectedSystems': detected,
        'dailyMemoryFiles': list_memory_daily(workspace / 'memory'),
        'candidates': candidates,
        'excludedByDefault': excluded_by_policy,
        'notes': notes,
    }

    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
