from pathlib import Path
import re

from tests.reference_loader import rendering_reference_text, shell_reference_text


ROOT = Path(__file__).resolve().parent.parent


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def test_summary_card_poster_mode_requires_explicit_fields():
    shell = shell_reference_text()
    skill = read("SKILL.md")
    checklist = read("references/review-checklist.md")

    assert "poster_title" in shell
    assert "poster_subtitle" in shell
    assert "const explicitTitle = (d.poster_title || '').trim();" in shell
    assert "const explicitSubtitle = (d.poster_subtitle || '').trim();" in shell
    assert "return { main: explicitTitle || raw, sub: explicitTitle ? explicitSubtitle : '' };" in shell
    assert "raw.match(/^(.{2,24}?)[：:|-]\\s*(.+)$/)" not in shell

    assert "Poster summary mode is opt-in" in skill
    assert "Do not infer `poster_title` or `poster_subtitle` from punctuation in `title`." in skill
    assert "Only use `poster_title` / `poster_subtitle` when the report truly needs a stronger poster headline than the document title." in checklist


def test_summary_card_stays_poster_like_not_metadata_panel():
    shell = shell_reference_text()
    design = read("references/design-quality.md")
    checklist = read("references/review-checklist.md")

    assert ".summary-chip-row" not in shell
    assert ".sc-bottom-note" not in shell
    assert "sectionSummaries[0]?.text" not in shell
    assert ".sc-abstract" not in shell
    assert ".sc-note" in shell
    assert "function posterNoteText(d)" in shell
    assert "margin-top: auto;" in shell
    assert "max-width: 13ch;" not in shell
    assert "max-width: 20ch;" not in shell
    assert "font-size: clamp(4rem, 8vw, 6.2rem);" not in shell
    assert "REPORT SUMMARY" not in shell
    assert "报告摘要" in shell
    assert "Summary cards should read like posters, not metadata panels." in design
    assert "Remove chips, bottom notes, and metadata filler if they weaken the poster read." in checklist
    assert "On the left panel, keep only the title hierarchy and one short closing sentence near the bottom." in design
    assert "Do not artificially squeeze the subtitle or closing sentence into a narrow column that wastes available width." in design
    assert "If the left panel reads like a paragraph block instead of a poster, compress it to one short sentence at the bottom." in checklist
    assert "If the left panel shows broken line wraps or wasted width, reduce title size and widen subtitle/note measure before changing content." in checklist


def test_narrative_cadence_blocks_are_optional_upgrades_with_strict_gates():
    skill = read("SKILL.md")
    rendering = rendering_reference_text()
    design = read("references/design-quality.md")
    checklist = read("references/review-checklist.md")

    for text in [
        "These are optional prose upgrades, not default required blocks.",
        "If uncertain, keep normal paragraphs and add one clearer scan anchor instead of forcing a cadence block.",
        "Do not add more than one of `lead-block` / `section-quote` / `action-grid` by default inside the same section unless the source material clearly warrants it.",
    ]:
        assert text in skill

    for text in [
        "Use them only when the surrounding prose clearly supports them.",
        "If uncertain, stay with plain prose plus one callout/list/timeline rather than forcing a rhythm block.",
    ]:
        assert text in rendering

    for text in [
        "Narrative cadence blocks are optional upgrades, not a quota.",
        "Never use them just to break up a page visually.",
    ]:
        assert text in design

    assert "When unsure, prefer paragraph splits or one ordinary scan anchor over decorative cadence blocks." in checklist


def test_regular_lumen_periodic_reports_do_not_force_placeholder_kpis():
    regular_rules = read("references/regular-report-content-rules.md")

    assert "强制 3-4 个" not in regular_rules
    assert "Missing → `[数据待填写]`" not in regular_rules
    assert "有真实指标才渲染" in regular_rules
    assert "日期、周数、版本号、章节序号不算 KPI" in regular_rules
    assert "`report-summary.kpis` 使用空数组" in regular_rules
    assert "本周期概览 (callout/prose；有真实指标时才是 KPI)" in regular_rules


def test_review_checklist_overview_count_matches_categories():
    checklist = read("references/review-checklist.md")
    category_counts = [int(match) for match in re.findall(r"\*\*Category \d: .*?\((\d+)\)\*\*", checklist)]
    overview_match = re.search(r"The system has \*\*(\d+) checkpoints\*\*", checklist)

    assert overview_match, "review-checklist overview count missing"
    assert category_counts, "review-checklist category counts missing"
    assert int(overview_match.group(1)) == sum(category_counts), (
        f"overview count {overview_match.group(1)} does not match category total {sum(category_counts)}"
    )
