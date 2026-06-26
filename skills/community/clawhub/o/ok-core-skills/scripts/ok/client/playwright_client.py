"""OK Playwright Client — headless with persistent context.

Uses ``launch_persistent_context`` so cookies, localStorage, and
sessionStorage survive across runs without manual serialisation.
Profile directory: ``~/.ok-agent/pw-profile/``.
"""

from __future__ import annotations

import base64
import logging
from pathlib import Path
from typing import Any

from playwright.sync_api import BrowserContext, Page, sync_playwright
from playwright_stealth import Stealth

from .base import BaseClient

logger = logging.getLogger("ok-playwright-client")

_PW_PROFILE_DIR = Path.home() / ".ok-agent" / "pw-profile"


class PlaywrightClient(BaseClient):
    """Headless Chromium with a persistent profile on disk."""

    def __init__(self) -> None:
        _PW_PROFILE_DIR.mkdir(parents=True, exist_ok=True)

        self.playwright = sync_playwright().start()
        self.context: BrowserContext = self.playwright.chromium.launch_persistent_context(
            str(_PW_PROFILE_DIR),
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
            ],
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
        )

        if self.context.pages:
            self.page: Page = self.context.pages[0]
        else:
            self.page = self.context.new_page()

        Stealth().apply_stealth_sync(self.page)
        logger.info("Playwright persistent client ready (profile: %s)", _PW_PROFILE_DIR)

    # ── navigation ───────────────────────────────────────────────────────

    def navigate(self, url: str) -> None:
        self.page.goto(url, wait_until="commit")

    def wait_for_load(self, timeout: int = 60000) -> None:
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def get_url(self) -> str:
        return self.page.url

    def wait_dom_stable(self, timeout: int = 10000, interval: int = 500) -> None:
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)

    def wait_for_selector(self, selector: str, timeout: int = 30000) -> None:
        self.page.wait_for_selector(selector, timeout=timeout)

    # ── query ────────────────────────────────────────────────────────────

    def has_element(self, selector: str) -> bool:
        return self.page.locator(selector).count() > 0

    def get_elements_count(self, selector: str) -> int:
        return self.page.locator(selector).count()

    def get_element_text(self, selector: str) -> str | None:
        loc = self.page.locator(selector).first
        if loc.count() > 0:
            return loc.text_content()
        return None

    def get_element_attribute(self, selector: str, attr: str) -> str | None:
        loc = self.page.locator(selector).first
        if loc.count() > 0:
            return loc.get_attribute(attr)
        return None

    # ── interaction ──────────────────────────────────────────────────────

    def click_element(self, selector: str) -> None:
        self.page.locator(selector).first.click()

    def input_text(self, selector: str, text: str) -> None:
        self.page.locator(selector).first.fill(text)

    def scroll_by(self, x: int = 0, y: int = 0) -> None:
        self.page.evaluate(f"window.scrollBy({x}, {y})")

    def scroll_to_bottom(self) -> None:
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_element_into_view(self, selector: str) -> None:
        loc = self.page.locator(selector).first
        if loc.count() > 0:
            loc.scroll_into_view_if_needed()

    # ── eval / commands ──────────────────────────────────────────────────

    def evaluate(self, expression: str) -> Any:
        return self.page.evaluate(expression)

    def send_command(self, method: str, params: dict | None = None) -> Any:
        params = params or {}
        if method == "press_key":
            self.page.keyboard.press(params.get("key", ""))
        elif method == "get_cookies":
            return self.context.cookies()
        elif method == "screenshot_element":
            buf = self.page.screenshot(type="png")
            return {"format": "png", "data": base64.b64encode(buf).decode("ascii")}
        else:
            logger.warning("PlaywrightClient: unhandled command: %s", method)

    # ── cleanup ──────────────────────────────────────────────────────────

    def __del__(self) -> None:
        try:
            self.context.close()
            self.playwright.stop()
        except Exception:
            pass
