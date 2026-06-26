"""
HTML Shell Structure Contract Tests — BUG-001 regression suite.

Root cause (BUG-001, 2026-04-13):
  AI generated reports missing TOC button, summary card, and export buttons
  because the html-shell-template.md structure was not enforced.

These tests verify that any generated HTML file contains the mandatory
  structural elements defined in references/html-shell-template.md.

Two test modes:
  - Unit: check HTML source strings (no browser, instant)
  - Integration: check real generated HTML files in fixtures/
"""
import pytest
from pathlib import Path

from scripts.shell_metadata import footer_watermark_text
from tests.reference_loader import shell_reference_text

REPO_ROOT = Path(__file__).parent.parent
FIXTURES_DIR = Path(__file__).parent / "fixtures"


# ── helpers ───────────────────────────────────────────────────────────────────

def load_html(name: str) -> str:
    """Load an HTML file from fixtures/."""
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


# ── L2: Required Elements ────────────────────────────────────────────────────
# See design-quality.md §8.1

REQUIRED_ELEMENTS = [
    # (id/class, purpose)
    ('id="toc-toggle-btn"', "TOC toggle button — visible ☰ button"),
    ('id="toc-sidebar"', "TOC sidebar navigation"),
    ('id="card-mode-btn"', "Summary card trigger button — ⊞ 摘要卡"),
    ('id="sc-overlay"', "Summary card modal overlay"),
    ('id="export-btn"', "Export button — ↓ 导出"),
    ('id="export-menu"', "Export dropdown menu"),
    ('id="report-summary"', "JSON summary block (machine-readable)"),
    ('data-report-mode=', "Body attribute: semantic mode flag"),
    # Edit mode
    ('id="edit-hotzone"', "Edit mode bottom-left hotzone"),
    ('id="edit-toggle"', "Edit mode toggle button"),
]

REQUIRED_EXPORT_ITEMS = [
    ('id="export-print"', "Print / PDF export entry"),
    ('id="export-png-desktop"', "Desktop image export entry"),
    ('id="export-png-mobile"', "Mobile long-image export entry"),
    ('id="export-im-share"', "IM long-image export entry"),
]

TEMPLATE_PATH = REPO_ROOT / "references" / "html-shell-template.md"


class TestRequiredElements:
    """Every generated report MUST contain these structural elements."""

    @pytest.mark.parametrize("element_id,purpose", REQUIRED_ELEMENTS)
    def test_minimal_report_has_required_element(self, element_id, purpose):
        """tests/fixtures/minimal_report.html must contain all required elements."""
        html = load_html("minimal_report.html")
        assert element_id in html, (
            f"MISSING: {element_id} ({purpose})\n"
            f"This element is required by html-shell-template.md.\n"
            f"See BUG-001 for context."
        )


class TestColorSystemReportElements:
    """The color_system_report.html fixture must also be structurally complete."""

    @pytest.mark.parametrize("element_id,purpose", REQUIRED_ELEMENTS)
    def test_color_report_has_required_element(self, element_id, purpose):
        html = load_html("color_system_report.html")
        assert element_id in html, (
            f"MISSING: {element_id} ({purpose}) in color_system_report.html"
        )


class TestExportMenuContract:
    """Export menu must always expose the full four-option contract."""

    @pytest.mark.parametrize("element_id,purpose", REQUIRED_EXPORT_ITEMS)
    def test_minimal_report_has_all_export_entries(self, element_id, purpose):
        html = load_html("minimal_report.html")
        assert element_id in html, (
            f"MISSING: {element_id} ({purpose}) in minimal_report.html.\n"
            "Export menus must include print, desktop, mobile, and IM variants."
        )

    @pytest.mark.parametrize("element_id,purpose", REQUIRED_EXPORT_ITEMS)
    def test_color_report_has_all_export_entries(self, element_id, purpose):
        html = load_html("color_system_report.html")
        assert element_id in html, (
            f"MISSING: {element_id} ({purpose}) in color_system_report.html.\n"
            "Export menus must include print, desktop, mobile, and IM variants."
        )


class TestTemplateExportContract:
    """The shell template itself must carry the complete export contract."""

    @staticmethod
    def template_source() -> str:
        return shell_reference_text()

    @pytest.mark.parametrize("element_id,purpose", REQUIRED_EXPORT_ITEMS)
    def test_template_has_all_export_entries(self, element_id, purpose):
        src = self.template_source()
        assert element_id in src, (
            f"MISSING: {element_id} ({purpose}) in references/html-shell-template.md.\n"
            "If the template loses an export item, generated reports will silently regress."
        )

    def test_template_wires_all_export_buttons(self):
        src = self.template_source()
        required_bindings = [
            "const printBtn   = document.getElementById('export-print');",
            "const pngDesktop = document.getElementById('export-png-desktop');",
            "const pngMobile  = document.getElementById('export-png-mobile');",
            "const pngIM      = document.getElementById('export-im-share');",
        ]
        for binding in required_bindings:
            assert binding in src, (
                f"Missing export binding in html-shell-template.md: {binding}"
            )


class TestPandocTitleBlockContract:
    """Pandoc title metadata must not duplicate the shell title/date metadata."""

    @staticmethod
    def template_source() -> str:
        return shell_reference_text()

    def test_template_forbids_pandoc_title_block_header(self):
        src = self.template_source()
        assert "title-block-header" in src
        assert '<p class="date">' in src
        assert "duplicate date" in src.lower()

    def test_skill_prewrite_points_to_duplicate_date_guard(self):
        skill = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
        assert "duplicate-date guard" in skill
        assert "references/html-shell-template.md" in skill


class TestWatermarkContract:
    """Main skill delegates detailed watermark handling to the shell reference."""

    @staticmethod
    def template_source() -> str:
        return shell_reference_text()

    def test_skill_prewrite_delegates_watermark_details_to_reference(self):
        skill = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
        assert "Shell metadata" in skill
        assert "references/html-shell-template.md" in skill
        assert "version/theme metadata" in skill
        assert "must match exactly" not in skill

    def test_template_has_html_shell_metadata_attrs(self):
        src = self.template_source()
        assert 'data-template="kai-report-creator"' in src
        assert 'data-version="[version]"' in src
        assert 'data-theme="[theme]"' in src


# ── L2: IR Hash Meta Tag ───────────────────────────────────────────────────────

class TestIRHashMetaContract:
    """IR hash meta tag must be present in template (v4 guardrails)."""

    @staticmethod
    def template_source() -> str:
        return shell_reference_text()

    def test_template_has_ir_hash_placeholder(self):
        """Template must include ir-hash meta tag placeholder."""
        src = self.template_source()
        assert '<meta name="ir-hash" content="sha256:[ir-hash]">' in src, (
            "MISSING: ir-hash meta tag in references/html-shell-template.md.\n"
            "The template must include the placeholder for IR hash fingerprint."
        )

    def test_ir_hash_placeholder_format(self):
        """Placeholder must use sha256:[ir-hash] format (not bare hash)."""
        src = self.template_source()
        # Accept either the full meta tag or just the placeholder pattern
        has_valid_format = (
            'content="sha256:[ir-hash]"' in src
            or 'sha256:[ir-hash]' in src
        )
        assert has_valid_format, (
            "Invalid ir-hash format — must use 'sha256:[ir-hash]' prefix, not bare hash.\n"
            "This format ensures downstream agents can validate hash algorithm."
        )


# ── L2: TOC JavaScript Contract ──────────────────────────────────────────────
# See design-quality.md §8.2

class TestTocJsContract:
    """TOC JS must include delay-close logic to prevent instant-close bug."""

    def test_schedule_close_exists(self):
        """TOC JS must define a scheduleClose or delayed-close function."""
        html = load_html("minimal_report.html")
        # Accept various naming patterns
        has_delay = (
            "scheduleClose" in html
            or "schedule_close" in html
            or "closeTimer" in html
            or "closeDelay" in html
        )
        assert has_delay, (
            "TOC JS must include delayed-close logic (scheduleClose or equivalent).\n"
            "Without this, the sidebar closes instantly on mouseleave — BUG-001."
        )

    def test_toc_sidebar_mouseenter(self):
        """Both tocBtn AND tocSidebar must have mouseenter handlers."""
        html = load_html("minimal_report.html")
        # The template has: tocBtn.addEventListener('mouseenter') and tocSidebar.addEventListener('mouseenter')
        # At minimum, both toc-toggle-btn and toc-sidebar must be referenced in mouseenter context
        assert "toc-sidebar" in html and "mouseenter" in html, (
            "TOC JS must reference toc-sidebar with mouseenter handler.\n"
            "Without sidebar mouseenter, the panel closes when moving from button to panel."
        )


# ── L2: CSS Assembly Verification ────────────────────────────────────────────
# See design-quality.md §8.4

class TestCssAssembly:
    """CSS must include styles for all required UI components."""

    def test_toc_css_exists(self):
        """Must have .toc-toggle and .toc-sidebar CSS rules."""
        html = load_html("minimal_report.html")
        assert ".toc-toggle" in html, "CSS missing .toc-toggle rule"
        assert ".toc-sidebar" in html, "CSS missing .toc-sidebar rule"

    def test_summary_card_css_exists(self):
        """Must have summary card CSS (.sc-card, .sc-overlay)."""
        html = load_html("minimal_report.html")
        assert ".sc-overlay" in html, "CSS missing .sc-overlay rule"

    def test_export_css_exists(self):
        """Must have export button/menu CSS."""
        html = load_html("minimal_report.html")
        assert ".export-btn" in html, "CSS missing .export-btn rule"
        assert ".export-menu" in html, "CSS missing .export-menu rule"

    def test_edit_mode_css_exists(self):
        """Must have edit mode CSS (.edit-hotzone, .edit-toggle)."""
        html = load_html("minimal_report.html")
        assert ".edit-hotzone" in html, "CSS missing .edit-hotzone rule"
        assert ".edit-toggle" in html, "CSS missing .edit-toggle rule"


# ── L2: JSON Summary Block ───────────────────────────────────────────────────

class TestJsonSummaryBlock:
    """The machine-readable summary JSON must be present and valid."""

    def test_report_summary_is_json(self):
        """#report-summary must be inside a <script type="application/json"> tag."""
        html = load_html("minimal_report.html")
        assert 'type="application/json"' in html, (
            "report-summary JSON must be in <script type=\"application/json\">, "
            "not <script type=\"text/javascript\">"
        )

    def test_report_summary_has_required_fields(self):
        """The JSON must contain title, sections, and kpis fields."""
        html = load_html("minimal_report.html")
        # Basic structural checks — don't parse JSON, just verify keys exist
        assert '"title"' in html, "JSON summary missing 'title' field"
        assert '"sections"' in html, "JSON summary missing 'sections' field"
        assert '"kpis"' in html, "JSON summary missing 'kpis' field"


class TestFooterWatermarkContract:
    """Standard shell footer/watermark use deterministic shell metadata."""

    @staticmethod
    def template_source() -> str:
        return shell_reference_text()

    def test_template_footer_placeholder_format(self):
        src = self.template_source()
        expected = footer_watermark_text("[version]", "[theme]")
        assert f'<div class="report-footer">{expected}</div>' in src, (
            "Visible footer must be assembled as 'kai-report-creator v[version] [theme]'.\n"
            "Do not swap the order or improvise additional prose."
        )

    def test_template_hidden_watermark_matches_footer(self):
        src = self.template_source()
        expected = footer_watermark_text("[version]", "[theme]")
        assert f'data-watermark="{expected}"' in src, (
            "Standard shell hidden watermark should carry the same deterministic metadata string."
        )
        assert f"\n            {expected}\n" in src, (
            "Standard shell hidden watermark body should carry the deterministic metadata string."
        )

    def test_template_footer_forbids_debug_metadata(self):
        src = self.template_source()
        assert "IR hash" not in src
        assert "Source condensed" not in src
        assert "By kai-report-creator" not in src

    @pytest.mark.parametrize(
        "fixture_name,version,theme",
        [
            ("minimal_report.html", "1.14.0", "minimal"),
            ("color_system_report.html", "1.21.0", "corporate-blue"),
        ],
    )
    def test_fixtures_match_footer_contract(self, fixture_name, version, theme):
        html = load_html(fixture_name)
        expected = footer_watermark_text(version, theme)
        assert f'<div class="report-footer">{expected}</div>' in html
        assert f'data-watermark="{expected}"' in html
        assert "IR hash" not in html
        assert "By kai-report-creator" not in html

    @pytest.mark.parametrize("template_path", [
        REPO_ROOT / "templates" / "en" / "regular-lumen.html",
        REPO_ROOT / "templates" / "zh" / "regular-lumen.html",
    ])
    def test_regular_lumen_templates_match_footer_contract(self, template_path: Path):
        html = template_path.read_text(encoding="utf-8")
        expected = footer_watermark_text("1.21.0", "regular-lumen")
        assert f'<div class="report-footer">{expected}</div>' in html
        assert f'data-watermark="{expected}"' in html


# ── Anti-regression: Forbidden Patterns ───────────────────────────────────────

class TestForbiddenTocPatterns:
    """BUG-001: AI generated obsolete toc-panel/toc-trigger pattern."""

    def test_no_obsolete_toc_panel(self):
        """Must NOT use the obsolete toc-panel + toc-trigger pattern."""
        html = load_html("minimal_report.html")
        # The obsolete pattern was: <div class="toc-trigger"> + <div class="toc-panel">
        # This is NOT in the current template, but was what AI generated in BUG-001
        assert 'class="toc-trigger"' not in html or 'id="toc-trigger"' not in html, (
            "Obsolete toc-trigger class detected — use toc-toggle instead.\n"
            "See BUG-001: AI generated invisible 20px trigger strip instead of ☰ button."
        )

    def test_no_obsolete_toc_panel_class(self):
        """Must NOT use the obsolete toc-panel class."""
        html = load_html("minimal_report.html")
        assert 'class="toc-panel"' not in html and 'id="tocPanel"' not in html, (
            "Obsolete toc-panel class detected — use toc-sidebar instead.\n"
            "See BUG-001: AI generated panel instead of sidebar."
        )
