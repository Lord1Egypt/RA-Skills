"""
Playwright tests for Print/PDF export behavior.

Covers:
  - Print export must enter a print-preparation state before calling window.print()
  - The resolved report background must be concrete, not transparent/empty
  - Export UI must be closed/hidden before the print snapshot is taken
  - Print media must force animated/data components visible
"""
from tests.test_screenshot_behavior import reset_log


def trigger_print_export(page):
    """Open the export menu, click Print/PDF, wait for the print stub."""
    page.evaluate("document.getElementById('export-btn').click()")
    page.evaluate("document.getElementById('export-print').click()")
    page.wait_for_timeout(300)


def last_print(page) -> dict:
    """Return the most recent print log entry."""
    log = page.evaluate("window._printLog")
    assert log, "No print export was triggered — check the print button wiring in the fixture"
    return log[-1]


class TestPrintExportPreparation:
    """Print/PDF export must preserve the report background before printing."""

    def test_print_export_prepares_non_transparent_background(self, report_page):
        reset_log(report_page)
        trigger_print_export(report_page)
        entry = last_print(report_page)

        assert entry["printBgColor"] not in ("", None, "transparent", "rgba(0, 0, 0, 0)", "rgba(0,0,0,0)"), (
            "Print/PDF export entered print mode without a concrete background color. "
            "Dark-theme reports will print with a white background."
        )

    def test_print_export_enters_print_mode_before_window_print(self, report_page):
        reset_log(report_page)
        trigger_print_export(report_page)
        entry = last_print(report_page)

        assert entry["printModeActive"] is True, (
            "Print/PDF export called window.print() before entering the print-preparation state."
        )

    def test_print_export_closes_menu_and_hides_button_before_window_print(self, report_page):
        reset_log(report_page)
        trigger_print_export(report_page)
        entry = last_print(report_page)

        assert entry["exportMenuOpen"] is False, (
            "Export menu was still open when window.print() fired."
        )
        assert entry["exportBtnVisibility"] == "hidden", (
            "Export button was still visible when window.print() fired."
        )


class TestPrintMediaVisibility:
    """Print CSS must neutralize animation-hidden component states."""

    def test_fade_in_blocks_are_visible_in_print_media(self, report_page):
        report_page.emulate_media(media="print")
        opacity = report_page.evaluate(
            "getComputedStyle(document.querySelector('.fade-in-up')).opacity"
        )

        assert opacity == "1", (
            "Print media left .fade-in-up content hidden. "
            "Report sections disappear in exported PDFs."
        )

    def test_kpi_cards_are_visible_in_print_media(self, report_page):
        report_page.emulate_media(media="print")
        opacity = report_page.evaluate(
            "getComputedStyle(document.querySelector('.kpi-card')).opacity"
        )

        assert opacity == "1", (
            "Print media left staggered KPI cards hidden. "
            "KPI/data blocks disappear in exported PDFs."
        )
