from pathlib import Path

import pytest

from validation import validate_recipe


FIXTURES = Path(__file__).parent / "fixtures" / "recipes"


def _write(tmp_path, content):
    path = tmp_path / "r.md"
    path.write_text(content)
    return path


def test_valid_recipe_passes(tmp_path):
    errors = validate_recipe(FIXTURES / "simple-beef-dinner.md")
    assert errors == []


def test_invalid_status_caught(tmp_path):
    base = (FIXTURES / "simple-beef-dinner.md").read_text()
    path = _write(tmp_path, base.replace("**Status:** trusted", "**Status:** mega-trusted"))
    errors = validate_recipe(path)
    assert any("invalid status" in e for e in errors)


def test_invalid_cooking_effort_caught(tmp_path):
    base = (FIXTURES / "simple-beef-dinner.md").read_text()
    path = _write(tmp_path, base.replace("**Cooking Effort:** easy", "**Cooking Effort:** lightning"))
    errors = validate_recipe(path)
    assert any("invalid cooking_effort" in e for e in errors)


def test_invalid_composition_caught(tmp_path):
    base = (FIXTURES / "simple-beef-dinner.md").read_text()
    path = _write(tmp_path, base.replace("**Composition:** self-contained", "**Composition:** vibes"))
    errors = validate_recipe(path)
    assert any("invalid Composition" in e for e in errors)


def test_missing_required_field_caught(tmp_path):
    base = (FIXTURES / "simple-beef-dinner.md").read_text()
    path = _write(tmp_path, base.replace("**Serves:** 4", "**Serves:**"))
    errors = validate_recipe(path)
    assert any("required field is empty: serves" in e for e in errors)


def test_missing_section_caught(tmp_path):
    base = (FIXTURES / "simple-beef-dinner.md").read_text()
    path = _write(tmp_path, base.replace("## Instructions\n1. Brown beef.\n", ""))
    errors = validate_recipe(path)
    assert any("missing section: ## Instructions" in e for e in errors)


def test_missing_title_caught(tmp_path):
    base = (FIXTURES / "simple-beef-dinner.md").read_text()
    path = _write(tmp_path, base.replace("# Simple Beef Dinner", "No title here"))
    errors = validate_recipe(path)
    assert any("level-1 markdown title" in e for e in errors)


def test_invalid_pair_with_prefix_caught(tmp_path):
    base = (FIXTURES / "baked-chicken.md").read_text()
    path = _write(tmp_path, base.replace("side: roasted vegetables", "entree: roasted vegetables"))
    errors = validate_recipe(path)
    assert any("invalid Pair With prefix" in e for e in errors)
