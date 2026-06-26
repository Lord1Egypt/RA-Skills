from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ANTI_PATTERNS = ROOT / "references" / "anti-patterns.md"
DIAGRAM_DECISION_RULES = ROOT / "references" / "diagram-decision-rules.md"


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def read_reference(path: Path) -> str:
    assert path.exists(), f"{path.relative_to(ROOT)} should exist"
    return path.read_text(encoding="utf-8")


def test_phase1_reference_files_exist():
    assert ANTI_PATTERNS.exists(), "references/anti-patterns.md should exist"
    assert DIAGRAM_DECISION_RULES.exists(), "references/diagram-decision-rules.md should exist"


def test_anti_patterns_doc_covers_report_specific_failure_modes():
    src = read_reference(ANTI_PATTERNS)

    for marker in [
        "`fake-kpi`",
        "`decorative-chart`",
        "`pseudo-timeline`",
        "`template-heading`",
        "`badge-quota-thinking`",
        "`color-flood`",
        "`summary-without-judgment`",
        "`action-without-decision-context`",
    ]:
        assert marker in src, f"anti-patterns.md missing marker: {marker}"

    for marker in [
        "## Symptom",
        "## Why It Hurts",
        "## Preferred Replacement",
        "## Rewrite Rule",
    ]:
        assert marker in src, f"anti-patterns.md missing contract section: {marker}"


def test_diagram_decision_rules_doc_defines_go_no_go_checks():
    src = read_reference(DIAGRAM_DECISION_RULES)

    for marker in [
        "Only draw a diagram when it materially reduces comprehension cost.",
        "Parallel points should stay as prose or list.",
        "Three to five principles should stay as prose or list.",
        "If prose explains it clearly, do not draw a diagram.",
        "`directionality`",
        "`dependency`",
        "`branching`",
        "Preferred downgrade: `callout` or `list`.",
    ]:
        assert marker in src, f"diagram-decision-rules.md missing marker: {marker}"


def test_skill_declares_when_to_load_phase1_reference_docs():
    src = read("SKILL.md")

    assert "references/anti-patterns.md" in src
    assert "references/diagram-decision-rules.md" in src
    assert "Always load `references/anti-patterns.md` before `--generate`." in src
    assert (
        "Load `references/diagram-decision-rules.md` whenever a diagram or diagram-like structure is being considered."
        in src
    )
