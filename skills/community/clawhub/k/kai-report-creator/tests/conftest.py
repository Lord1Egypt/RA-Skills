"""Shared pytest fixtures for kai-report-creator tests."""
import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_export_image_module():
    """Import scripts/export-image.py (hyphen in name requires importlib)."""
    spec = importlib.util.spec_from_file_location(
        "export_image", SCRIPTS_DIR / "export-image.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="session")
def export_image_mod():
    return load_export_image_module()


@pytest.fixture(scope="session")
def browser_instance():
    if importlib.util.find_spec("playwright") is None:
        pytest.skip("playwright is not installed")

    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        b = pw.chromium.launch()
        yield b
        b.close()


@pytest.fixture
def page(browser_instance):
    p = browser_instance.new_page()
    yield p
    p.close()


@pytest.fixture
def report_page(page):
    """Load the minimal report fixture and wait for JS to initialise."""
    url = f"file://{FIXTURES_DIR / 'minimal_report.html'}"
    page.goto(url)
    page.wait_for_load_state("domcontentloaded")
    return page
