import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def extract_frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, re.MULTILINE)
    assert match, f"missing frontmatter key: {key}"
    return match.group(1).strip()


def test_skill_reference_paths_exist():
    src = read("SKILL.md")
    paths = sorted(set(re.findall(r"`(references/[A-Za-z0-9_./*-]+)`", src)))

    assert paths, "SKILL.md should route through references/"
    for path in paths:
        if "*" in path:
            matches = sorted(ROOT.glob(path))
            assert matches, f"SKILL.md glob has no matches: {path}"
            assert all(match.is_file() for match in matches), f"SKILL.md glob matched non-files: {path}"
        else:
            assert (ROOT / path).is_file(), f"SKILL.md references missing file: {path}"


def test_golden_case_artifact_paths_exist():
    src = read("evals/golden_cases.yaml")
    paths = sorted(
        set(
            re.findall(
                r"^\s+(?:source|ir|context):\s+([A-Za-z0-9_./-]+)\s*$",
                src,
                re.MULTILINE,
            )
        )
    )

    assert paths, "golden_cases.yaml should declare source/ir/context artifacts"
    for path in paths:
        assert (ROOT / path).exists(), f"golden case artifact path is missing: {path}"


def test_builtin_theme_names_stay_consistent():
    skill = read("SKILL.md")
    theme_css = read("references/theme-css.md")
    css_files = sorted(path.stem for path in (ROOT / "templates" / "themes").glob("*.css"))
    css_files = [theme for theme in css_files if theme != "shared"]

    skill_match = re.search(r"Built-ins:\s*`([^`]+)`(.+?)\.", skill)
    assert skill_match, "SKILL.md should list built-in themes in the --theme row"
    skill_themes = re.findall(r"`([^`]+)`", skill_match.group(0))

    theme_css_match = re.search(r"## Built-in Theme Names\n\n(.+?)\n", theme_css)
    assert theme_css_match, "theme-css.md should list built-in theme names"
    theme_css_names = re.findall(r"`([^`]+)`", theme_css_match.group(1))

    assert sorted(skill_themes) == css_files
    assert sorted(theme_css_names) == css_files


def test_failure_map_uses_repo_relative_links():
    src = read("evals/failure-map.md")

    forbidden_patterns = [
        "/D:/",
        "D:/",
        "/Users/",
        "file://",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in src, f"failure-map.md should not contain machine-local path: {pattern}"


def test_skill_head_version_matches_runtime_skill_when_present():
    skill_head = ROOT / "SKILL_HEAD.md"
    if not skill_head.exists():
        return

    runtime_version = extract_frontmatter_value(read("SKILL.md"), "version")
    head_version = extract_frontmatter_value(skill_head.read_text(encoding="utf-8"), "version")

    assert head_version == runtime_version
