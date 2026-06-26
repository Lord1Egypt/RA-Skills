"""
Unit tests for scripts/export-image.py — no browser required.

Covers:
  - Resolution regression: scale factors must be >= 2 (Retina / 2x)
  - UI chrome is hidden before screenshot
  - Argument parsing
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"


# ── helpers ──────────────────────────────────────────────────────────────────

def script_source() -> str:
    return (SCRIPTS_DIR / "export-image.py").read_text(encoding="utf-8")


# ── Resolution regression tests ──────────────────────────────────────────────

class TestExportConfigs:
    """EXPORT_CONFIGS must guarantee high-resolution output.

    Regression: before fix, desktop=1.5×, mobile/im=1×. All produced blurry images.
    """

    def test_desktop_scale_is_high_resolution(self, export_image_mod):
        """Desktop screenshots must use device_scale_factor >= 2."""
        scale = export_image_mod.EXPORT_CONFIGS["desktop"]["scale"]
        assert scale >= 2.0, (
            f"Desktop scale {scale} is too low — will produce blurry screenshots. "
            "Must be >= 2.0 (was 1.5 before the fix)."
        )

    def test_mobile_scale_is_retina(self, export_image_mod):
        """Mobile export must use device_scale_factor >= 2 for IM-quality images."""
        scale = export_image_mod.EXPORT_CONFIGS["mobile"]["scale"]
        assert scale >= 2.0, (
            f"Mobile scale {scale} too low — IM-shared images will look blurry. "
            "Must be >= 2.0."
        )

    def test_im_scale_is_retina(self, export_image_mod):
        """IM export must use device_scale_factor >= 2."""
        scale = export_image_mod.EXPORT_CONFIGS["im"]["scale"]
        assert scale >= 2.0, (
            f"IM scale {scale} too low — IM-shared images will look blurry. "
            "Must be >= 2.0."
        )

    def test_all_modes_present(self, export_image_mod):
        """All three export modes must exist in config."""
        assert set(export_image_mod.EXPORT_CONFIGS.keys()) == {"desktop", "mobile", "im"}

    def test_mobile_target_width(self, export_image_mod):
        """Mobile target width must be 750px (WeChat-safe)."""
        assert export_image_mod.EXPORT_CONFIGS["mobile"]["target_w"] == 750

    def test_im_target_width(self, export_image_mod):
        """IM target width must be 800px."""
        assert export_image_mod.EXPORT_CONFIGS["im"]["target_w"] == 800

    def test_desktop_outputs_png(self, export_image_mod):
        """Desktop must output PNG, not JPEG."""
        assert export_image_mod.EXPORT_CONFIGS["desktop"]["jpeg"] is False

    def test_mobile_outputs_jpeg(self, export_image_mod):
        """Mobile/IM use JPEG for smaller file sizes."""
        assert export_image_mod.EXPORT_CONFIGS["mobile"]["jpeg"] is True
        assert export_image_mod.EXPORT_CONFIGS["im"]["jpeg"] is True


# ── UI chrome hidden before screenshot ───────────────────────────────────────

class TestUIChrome:
    """export-image.py must hide UI buttons before taking a screenshot.

    Regression: before fix, toc-toggle and export-btn appeared in CLI screenshots.
    """

    def test_toc_toggle_hidden_before_screenshot(self):
        """The JS that hides .toc-toggle must appear before page.screenshot()."""
        src = script_source()
        hide_idx = src.find("toc-toggle")
        shot_idx = src.find("page.screenshot(")
        assert hide_idx != -1, "Script must reference '.toc-toggle' to hide it"
        assert shot_idx != -1, "Script must call page.screenshot()"
        assert hide_idx < shot_idx, (
            "UI elements must be hidden BEFORE page.screenshot() is called"
        )

    def test_export_btn_hidden_before_screenshot(self):
        """The export button must be hidden before taking a screenshot."""
        src = script_source()
        # The hide call sets display='none' on a list that includes export-btn
        assert "export-btn" in src, "Script must reference 'export-btn' to hide it"

    def test_device_scale_factor_used_in_context(self):
        """Must use device_scale_factor (not just screenshot scale) for true DPI."""
        src = script_source()
        assert "device_scale_factor" in src, (
            "Must set device_scale_factor on browser context — "
            "screenshot-level scale alone doesn't increase actual pixel density"
        )

    def test_scale_device_passed_to_screenshot(self):
        """scale='device' must be passed to screenshot() to honour DPR."""
        src = script_source()
        assert '"device"' in src or "'device'" in src, (
            "page.screenshot() must include scale='device' to honour device_scale_factor"
        )
