from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REVIEW_CHECKLIST = ROOT / "references" / "review-checklist.md"


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def test_review_checklist_exists():
    assert REVIEW_CHECKLIST.exists(), "references/review-checklist.md should exist"


def test_review_checklist_contains_expected_rule_sections():
    src = REVIEW_CHECKLIST.read_text(encoding="utf-8")
    assert "### 1.1 BLUF Opening" in src
    assert "### 1.2 Heading Stack Logic" in src
    assert "### 1.3 Anti-Template Section Headings" in src
    assert "### 1.4 Prose Wall Detection" in src
    assert "### 1.5 Takeaway After Data" in src
    assert "### 2.1 Insight Over Data" in src
    assert "### 2.2 Scan-Anchor Coverage" in src
    assert "### 2.3 Conditional Reader Guidance" in src
    assert "## Rejected Candidates" in src


def test_skill_documents_review_mode_and_generate_review_pass():
    src = read("SKILL.md")
    assert "--review [file]" in src
    assert "references/review-checklist.md" in src
    assert "silent final review pass" in src
    assert "one-pass automatic refinement" in src


def test_readmes_expose_review_mode_consistently():
    readme_en = read("README.md")
    readme_zh = read("README.zh-CN.md")

    assert "/report --review" in readme_en
    assert "13-checkpoint" in readme_en
    assert "silent final review" in readme_en
    assert "review-report-template.md" in readme_en

    assert "/report --review" in readme_zh
    assert "13 项检查点" in readme_zh
    assert "静默终审" in readme_zh
    assert "review-report-template.md" in readme_zh


def test_design_quality_links_l0_and_l1_review_layers():
    src = read("references/design-quality.md")
    assert "## L1 Content Review" in src
    assert "review-checklist.md" in src
    assert "L0 (Visual)" in src
    assert "L1 (Content)" in src


def test_review_report_template_exists_and_is_documented():
    src = read("references/review-report-template.md")
    assert "# Review Report Template" in src
    assert "## Triggered Checkpoints" in src
    assert "## Files" in src

    skill = read("SKILL.md")
    assert "review-report-template.md" in skill
