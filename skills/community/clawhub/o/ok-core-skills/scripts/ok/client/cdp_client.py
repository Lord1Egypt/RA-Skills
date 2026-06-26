"""OK CDP client: Playwright connect_over_cdp to local Chrome.

No stealth (real user profile). Page selection is in _pick_context_and_page.
"""

from __future__ import annotations

import base64
import logging
from typing import Any

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from .base import BaseClient

logger = logging.getLogger("ok-cdp-client")

# Default URL when opening a new tab (no ok.com tab yet)
_DEFAULT_OK_ENTRY = "https://www.ok.com/"


class CdpConnectionError(Exception):
    """Failed to connect to the browser over CDP."""


class CdpClient(BaseClient):
    """Connect to Chrome via CDP and pick an ok.com page for automation."""

    def __init__(self, cdp_url: str, *, connect_timeout_ms: float = 3000.0) -> None:
        self._cdp_url = cdp_url.rstrip("/")
        self.playwright = sync_playwright().start()
        try:
            self.browser = self.playwright.chromium.connect_over_cdp(
                self._cdp_url,
                timeout=connect_timeout_ms,
            )
        except Exception as e:
            self.playwright.stop()
            raise CdpConnectionError(f"CDP connection failed ({cdp_url}): {e}") from e

        self.context: BrowserContext
        self.page: Page
        self.context, self.page = _pick_context_and_page(self.browser)
        logger.info(
            "CdpClient connected, page url=%s",
            self.page.url[:80] if self.page.url else "(empty)",
        )

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

    def evaluate(self, expression: str) -> Any:
        return self.page.evaluate(expression)

    def send_command(self, method: str, params: dict | None = None) -> Any:
        params = params or {}
        if method == "press_key":
            key = params.get("key")
            self.page.keyboard.press(key)
        elif method == "get_cookies":
            return self.context.cookies()
        elif method == "screenshot_element":
            buf = self.page.screenshot(type="png")
            return {"format": "png", "data": base64.b64encode(buf).decode("ascii")}
        else:
            logger.warning("CdpClient: unhandled command: %s", method)

    def __del__(self) -> None:
        try:
            # connect_over_cdp: browser.close() detaches Playwright; does not kill Chrome
            self.browser.close()
            self.playwright.stop()
        except Exception:
            pass


def _url_is_ok_com(url: str) -> bool:
    if not url:
        return False
    u = url.lower()
    return "ok.com" in u


def _pick_context_and_page(browser: Browser) -> tuple[BrowserContext, Page]:
    """Prefer an open tab with ok.com; else first tab; else new tab to ok.com."""
    for ctx in browser.contexts:
        for page in ctx.pages:
            if _url_is_ok_com(page.url or ""):
                return ctx, page

    for ctx in browser.contexts:
        if ctx.pages:
            return ctx, ctx.pages[0]

    if browser.contexts:
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.goto(_DEFAULT_OK_ENTRY, wait_until="commit")
        return ctx, page

    page = browser.new_page()
    page.goto(_DEFAULT_OK_ENTRY, wait_until="commit")
    # new_page() attaches to default context; use page.context for cookies
    ctx = page.context
    return ctx, page
