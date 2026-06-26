"""Tests for quick-fix commands."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from engram.fix import fix_type, fix_name, add_fact, remove_fact


@pytest.fixture
def entity_dir(tmp_path):
    entities = tmp_path / "entities"
    entities.mkdir()
    
    (entities / "Greptile.md").write_text(
        "# Greptile\n**Type:** person\n\n"
        "## Facts\n- Code review bot\n\n"
        "## Timeline\n\n### [[2026-02-16]]\n- Reviewed PR\n"
    )
    (entities / "OpenClaw.md").write_text(
        "# OpenClaw\n**Type:** project\n\n"
        "## Facts\n- 195k stars\n- TypeScript\n\n"
        "## Timeline\n"
    )
    return entities


class TestFixType:
    def test_change_type(self, entity_dir):
        result = fix_type(entity_dir, "Greptile", "tool")
        assert "Updated" in result
        assert "**Type:** tool" in (entity_dir / "Greptile.md").read_text()
    
    def test_fuzzy_match(self, entity_dir):
        result = fix_type(entity_dir, "greptile", "tool")
        assert "Updated" in result
    
    def test_not_found(self, entity_dir):
        result = fix_type(entity_dir, "NonExistent", "tool")
        assert "not found" in result


class TestFixName:
    def test_rename(self, entity_dir):
        result = fix_name(entity_dir, "Greptile", "Greptile Bot")
        assert "Renamed" in result
        assert (entity_dir / "Greptile-Bot.md").exists()
        assert not (entity_dir / "Greptile.md").exists()
        assert "# Greptile Bot" in (entity_dir / "Greptile-Bot.md").read_text()
    
    def test_name_conflict(self, entity_dir):
        result = fix_name(entity_dir, "Greptile", "OpenClaw")
        assert "already exists" in result


class TestAddFact:
    def test_add_new_fact(self, entity_dir):
        result = add_fact(entity_dir, "Greptile", "AI-powered code reviewer")
        assert "Added" in result
        content = (entity_dir / "Greptile.md").read_text()
        assert "AI-powered code reviewer" in content
    
    def test_duplicate_fact(self, entity_dir):
        result = add_fact(entity_dir, "Greptile", "Code review bot")
        assert "already exists" in result
    
    def test_add_to_entity_without_facts(self, entity_dir):
        (entity_dir / "NoFacts.md").write_text("# NoFacts\n**Type:** test\n\n## Timeline\n")
        result = add_fact(entity_dir, "NoFacts", "New fact")
        assert "Added" in result
        content = (entity_dir / "NoFacts.md").read_text()
        assert "## Facts" in content
        assert "New fact" in content


class TestRemoveFact:
    def test_remove_fact(self, entity_dir):
        result = remove_fact(entity_dir, "OpenClaw", "TypeScript")
        assert "Removed" in result
        content = (entity_dir / "OpenClaw.md").read_text()
        assert "TypeScript" not in content
        assert "195k stars" in content  # Other facts preserved
    
    def test_remove_nonexistent(self, entity_dir):
        result = remove_fact(entity_dir, "OpenClaw", "does not exist")
        assert "No fact matching" in result
