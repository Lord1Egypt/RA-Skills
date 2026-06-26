"""
Tests for screenshot.py

Run: python -m pytest tests/test_screenshot.py -v
     python tests/run_tests.py
"""

import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image

FIXTURES = Path(__file__).parent / "fixtures"
SCRIPT = Path(__file__).parent.parent / "scripts" / "screenshot.py"


def run_screenshot(args: list) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT)] + args,
        capture_output=True, text=True
    )


# ─── Happy path ──────────────────────────────────────────────────────────────

class TestScreenshot:

    def test_creates_png_file(self, tmp_path):
        """Basic run → PNG output file is created."""
        out = tmp_path / "out.png"
        r = run_screenshot([str(FIXTURES / "report.html"), str(out)])
        assert r.returncode == 0, f"Script failed:\n{r.stderr}"
        assert out.exists(), "PNG not created"

    def test_default_width_is_1440(self, tmp_path):
        """Default viewport (scale=2) → PNG width should be 2880px (1440 × 2)."""
        out = tmp_path / "out.png"
        run_screenshot([str(FIXTURES / "report.html"), str(out)])
        img = Image.open(out)
        assert img.width == 2880, f"Expected width 2880, got {img.width}"

    def test_file_has_content(self, tmp_path):
        """Output PNG should be larger than 5 KB."""
        out = tmp_path / "out.png"
        run_screenshot([str(FIXTURES / "report.html"), str(out)])
        assert out.stat().st_size > 5_000, "PNG is suspiciously small"

    def test_default_output_path(self, tmp_path):
        """No output arg → PNG saved alongside HTML with same stem."""
        import shutil
        html = tmp_path / "my_report.html"
        shutil.copy(FIXTURES / "report.html", html)
        r = run_screenshot([str(html)])
        assert r.returncode == 0, f"Script failed:\n{r.stderr}"
        png = tmp_path / "my_report.png"
        assert png.exists(), f"Expected {png} to be created"

    def test_custom_width(self, tmp_path):
        """--width 800 → PNG width should be 1600px (800 × default scale 2)."""
        out = tmp_path / "out.png"
        r = run_screenshot([str(FIXTURES / "report.html"), str(out), "--width", "800"])
        assert r.returncode == 0, f"Script failed:\n{r.stderr}"
        img = Image.open(out)
        assert img.width == 1600, f"Expected width 1600, got {img.width}"

    def test_scale_2x_doubles_width(self, tmp_path):
        """--scale 2 → PNG width should be 2 × viewport width (2880 at default 1440)."""
        out = tmp_path / "out.png"
        r = run_screenshot([str(FIXTURES / "report.html"), str(out), "--scale", "2"])
        assert r.returncode == 0, f"Script failed:\n{r.stderr}"
        img = Image.open(out)
        assert img.width == 2880, f"Expected width 2880, got {img.width}"

    def test_scale_2x_doubles_height(self, tmp_path):
        """--scale 2 → PNG height should be 2× the --scale 1 height."""
        out_1x = tmp_path / "out_1x.png"
        out_2x = tmp_path / "out_2x.png"
        run_screenshot([str(FIXTURES / "report.html"), str(out_1x), "--scale", "1"])
        run_screenshot([str(FIXTURES / "report.html"), str(out_2x), "--scale", "2"])
        h1 = Image.open(out_1x).height
        h2 = Image.open(out_2x).height
        assert h2 == h1 * 2, f"Expected {h1 * 2}, got {h2}"

    def test_custom_width_with_scale(self, tmp_path):
        """--width 800 --scale 2 → PNG width should be 1600px."""
        out = tmp_path / "out.png"
        r = run_screenshot([
            str(FIXTURES / "report.html"), str(out),
            "--width", "800", "--scale", "2"
        ])
        assert r.returncode == 0, f"Script failed:\n{r.stderr}"
        img = Image.open(out)
        assert img.width == 1600, f"Expected width 1600, got {img.width}"

    def test_captures_full_page(self, tmp_path):
        """Full-page screenshot → height should be taller than a normal viewport."""
        out = tmp_path / "out.png"
        run_screenshot([str(FIXTURES / "report.html"), str(out)])
        img = Image.open(out)
        # A scrollable report page should be taller than a single 900px viewport
        assert img.height > 900, f"Expected full-page height > 900px, got {img.height}"

    def test_works_with_slides_html(self, tmp_path):
        """Screenshot works on a slides HTML (not just reports)."""
        out = tmp_path / "out.png"
        r = run_screenshot([str(FIXTURES / "simple_slides.html"), str(out)])
        assert r.returncode == 0, f"Script failed:\n{r.stderr}"
        assert out.exists()


# ─── Error cases ─────────────────────────────────────────────────────────────

class TestScreenshotErrorCases:

    def test_missing_file_exits_nonzero(self, tmp_path):
        """Nonexistent input file → non-zero exit code."""
        out = tmp_path / "out.png"
        r = run_screenshot([str(tmp_path / "ghost.html"), str(out)])
        assert r.returncode != 0, "Expected non-zero exit for missing file"
