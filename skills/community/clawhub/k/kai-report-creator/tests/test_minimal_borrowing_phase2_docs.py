from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPEC_LOADING_MATRIX = ROOT / "references" / "spec-loading-matrix.md"


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def test_phase2_reference_file_exists():
    assert SPEC_LOADING_MATRIX.exists(), "references/spec-loading-matrix.md should exist"


def test_spec_loading_matrix_covers_four_minimal_archetypes():
    src = SPEC_LOADING_MATRIX.read_text(encoding="utf-8")

    for marker in [
        "`brief`",
        "`research`",
        "`comparison`",
        "`update`",
        "Primary emphasis",
        "Load first",
        "Load only if needed",
        "First-screen structure",
        "Component preference",
    ]:
        assert marker in src, f"spec-loading-matrix.md missing marker: {marker}"


def test_skill_declares_silent_classify_and_optional_archetype():
    src = read("SKILL.md")

    assert "references/spec-loading-matrix.md" in src
    assert "Load `references/spec-loading-matrix.md` before `--plan` and `--generate` as a silent classifier." in src
    assert "archetype: research" in src
    assert "Optional lightweight archetype hint for silent classification." in src
    assert "`brief`, `research`, `comparison`, `update`" in src
