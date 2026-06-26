"""Tests for midos-self-improver skill."""

import json
import re
import pytest
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
SKILL_MD = SKILL_DIR / 'SKILL.md'
SKILL_JSON = SKILL_DIR / 'skill.json'


# ═══════════════════════════════════════════════════════════════
# BASE TESTS (7)
# ═══════════════════════════════════════════════════════════════

def test_skill_md_exists():
    assert SKILL_MD.exists(), 'SKILL.md missing'


def test_skill_json_exists():
    assert SKILL_JSON.exists(), 'skill.json missing'


def test_skill_md_has_frontmatter():
    content = SKILL_MD.read_text(encoding='utf-8')
    assert content.startswith('---'), 'SKILL.md must start with YAML frontmatter'
    assert content.count('---') >= 2, 'SKILL.md must have closing frontmatter'


def test_skill_md_has_footer():
    content = SKILL_MD.read_text(encoding='utf-8')
    assert 'midos.dev' in content, 'SKILL.md must include MidOS footer'


def test_skill_md_no_secrets():
    content = SKILL_MD.read_text(encoding='utf-8')
    patterns = [r'sk-[a-zA-Z0-9]{20}', r'ghp_[a-zA-Z0-9]{36}',
                r'AIza[a-zA-Z0-9_-]{35}', r'glpat-[a-zA-Z0-9-]{20}']
    for p in patterns:
        assert not re.search(p, content), f'Secret pattern found: {p}'


def test_skill_md_no_internal_paths():
    content = SKILL_MD.read_text(encoding='utf-8')
    internal = ['D:\\\\Proyectos', '1midos/', 'modules/', '.orchestra/',
                'knowledge/chunks/', 'hive_commons/']
    for ref in internal:
        assert ref not in content, f'Internal path leaked: {ref}'


def test_skill_md_size():
    content = SKILL_MD.read_text(encoding='utf-8')
    size_kb = len(content.encode('utf-8')) / 1024
    assert size_kb <= 25, f'SKILL.md too large: {size_kb:.1f}KB (max 25KB)'
    assert size_kb >= 1, f'SKILL.md too small: {size_kb:.1f}KB (min 1KB)'


# ═══════════════════════════════════════════════════════════════
# CUSTOM TESTS — Architecture claims validation
# ═══════════════════════════════════════════════════════════════

def _load_content():
    return SKILL_MD.read_text(encoding='utf-8')


def _load_meta():
    return json.loads(SKILL_JSON.read_text(encoding='utf-8'))


def test_documents_all_5_detection_triggers():
    """Must document all 5 detection types."""
    content = _load_content().lower()
    triggers = ['correction', 'error', 'knowledge gap', 'best practice', 'pattern']
    for trigger in triggers:
        assert trigger in content, f'Detection trigger "{trigger}" not documented'


def test_documents_quality_gate():
    """Core differentiator: deterministic quality gate before staging."""
    content = _load_content().lower()
    assert 'quality gate' in content, 'Must document quality gate'
    assert 'deterministic' in content or 'no llm' in content, \
        'Must state quality gate is deterministic (no LLM)'


def test_documents_deduplication():
    """Must explain dedup mechanism (SHA-256 + similarity)."""
    content = _load_content().lower()
    assert 'sha-256' in content or 'sha256' in content, 'Must document SHA-256 hashing for dedup'
    assert 'dedup' in content or 'duplicat' in content, 'Must explain deduplication'


def test_documents_4_axis_scoring():
    """Must document all 4 scoring axes with weights."""
    content = _load_content().lower()
    axes = ['recurrence', 'freshness', 'specificity', 'impact']
    for axis in axes:
        assert axis in content, f'Scoring axis "{axis}" not documented'
    # Check weights are documented
    assert '0.35' in content, 'Recurrence weight (0.35) not documented'
    assert '0.25' in content, 'Freshness weight (0.25) not documented'
    assert '0.20' in content or '0.2' in content, 'Specificity/Impact weight (0.20) not documented'


def test_documents_promotion_thresholds():
    """Must document promotion thresholds (promote >= 0.7, prune < 0.3)."""
    content = _load_content()
    assert '0.7' in content, 'Promotion threshold (0.7) not documented'
    assert '0.3' in content, 'Prune threshold (0.3) not documented'


def test_documents_standalone_mode():
    """Must work without MidOS — standalone instructions for any agent."""
    content = _load_content().lower()
    assert 'standalone' in content, 'Must document standalone mode'
    assert 'claude.md' in content or 'agent instructions' in content, \
        'Must show how to add to agent instructions'


def test_documents_comparison_table():
    """Must have comparison table vs self-improving-agent (101K)."""
    content = _load_content()
    meta = _load_meta()
    assert 'self-improving-agent' in content, \
        'Must compare against self-improving-agent (101K downloads)'
    for comp in meta.get('competitors', []):
        assert comp['slug'] in content, f'Competitor {comp["slug"]} not in comparison'


def test_documents_noise_rejection():
    """Must show how noise gets rejected (key differentiator vs competitors)."""
    content = _load_content().lower()
    assert 'noise' in content or 'reject' in content, \
        'Must document noise rejection capability'


def test_skill_json_version_matches_frontmatter():
    """Version in skill.json must match SKILL.md frontmatter."""
    meta = _load_meta()
    content = _load_content()
    fm_match = re.search(r'version:\s*([\d.]+)', content[:200])
    assert fm_match, 'Version not found in SKILL.md frontmatter'
    assert fm_match.group(1) == meta['version'], \
        f'Version mismatch: skill.json={meta["version"]} vs SKILL.md={fm_match.group(1)}'


def test_no_todo_or_placeholder():
    """No TODOs or placeholders in a release-ready skill."""
    content = _load_content()
    assert 'TODO' not in content, 'SKILL.md contains TODO placeholder'
    assert 'FIXME' not in content, 'SKILL.md contains FIXME placeholder'
    assert 'TBD' not in content, 'SKILL.md contains TBD placeholder'
