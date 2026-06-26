"""Tests for component discovery across user and example paths."""
from pathlib import Path
from glancely.core.registry.discover import discover_components


def test_discovers_user_components(tmp_path: Path):
    """Components in ~/.glancely/components/ should be found."""
    comp_dir = tmp_path / "workout"
    comp_dir.mkdir(parents=True)
    toml = comp_dir / "component.toml"
    toml.write_text(
        "[component]\nname = \"workout\"\n"
        "[panel]\nenabled = true\norder = 10\n"
    )

    components = discover_components(user_root=tmp_path)
    names = [c.name for c in components]
    assert "workout" in names


def test_excludes_scaffold_component(tmp_path: Path):
    """scaffold_component should never appear in dashboard."""
    comp_dir = tmp_path / "scaffold_component"
    comp_dir.mkdir(parents=True)
    toml = comp_dir / "component.toml"
    toml.write_text(
        "[component]\nname = \"scaffold_component\"\n"
        "[panel]\nenabled = true\norder = 0\n"
    )

    components = discover_components(user_root=tmp_path)
    names = [c.name for c in components]
    assert "scaffold_component" not in names


def test_empty_user_dir_returns_empty(tmp_path: Path):
    """No components = empty list, no crash."""
    components = discover_components(user_root=tmp_path)
    assert components == []
