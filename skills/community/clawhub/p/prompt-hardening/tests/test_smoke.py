"""Smoke test for prompt-hardening skill."""

from pathlib import Path


def test_skill_md_exists():
    skill_dir = Path(__file__).resolve().parents[1]
    assert (skill_dir / "SKILL.md").exists()
