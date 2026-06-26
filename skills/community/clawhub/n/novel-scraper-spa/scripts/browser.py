#!/usr/bin/env python3.11
"""
Playwright browser module for novel-scraper-spa

Browser instance singleton with content loading support.
"""

import logging
from typing import Optional
from playwright.sync_api import (
    sync_playwright,
    Page,
    TimeoutError as PlaywrightTimeout,
    Playwright,
)

logger = logging.getLogger(__name__)


class BrowserManager:
    """Singleton browser manager using Playwright."""

    _instance: Optional["BrowserManager"] = None
    _playwright: Optional[Playwright] = None
    _browser: Optional[object] = None
    _context: Optional[object] = None
    _page: Optional[Page] = None

    def __new__(cls) -> "BrowserManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._browser is None:
            pw = sync_playwright().start()
            assert pw is not None
            self._playwright = pw
            self._browser = pw.chromium.launch(headless=True)
            assert self._browser is not None
            self._context = self._browser.new_context(
                viewport={"width": 1920, "height": 1080}
            )
            self._page = self._context.new_page()
            logger.info("Browser instance created (singleton)")

    def get_page(self) -> Page:
        """Get the current page instance."""
        assert self._page is not None
        return self._page

    def goto(self, url: str, timeout: int = 30000) -> bool:
        """Navigate to URL and wait for content."""
        assert self._page is not None
        assert self._browser is not None
        try:
            logger.info(f"Navigating to: {url}")
            self._page.goto(url, timeout=timeout, wait_until="networkidle")
            return True
        except PlaywrightTimeout:
            logger.error(f"Timeout loading: {url}")
            return False

    def wait_for_selector(self, selector: str, timeout: int = 10000) -> bool:
        """Wait for element to appear."""
        assert self._page is not None
        try:
            self._page.wait_for_selector(selector, timeout=timeout)
            return True
        except PlaywrightTimeout:
            logger.warning(f"Element not found: {selector}")
            return False

    def get_content(self) -> str:
        """Get page HTML content."""
        assert self._page is not None
        return self._page.content()

    def close(self):
        """Close browser and cleanup."""
        if self._browser and self._playwright:
            self._browser.close()
            self._playwright.stop()
            logger.info("Browser instance closed")


def get_html(url: str, wait_selector: Optional[str] = None) -> Optional[str]:
    """
    Get HTML content from URL using Playwright.

    Args:
        url: Target URL
        wait_selector: Optional selector to wait for before extracting content

    Returns:
        HTML content or None if failed
    """
    browser = BrowserManager()

    if not browser.goto(url):
        return None

    if wait_selector:
        if not browser.wait_for_selector(wait_selector):
            logger.warning(f"Content selector not found: {wait_selector}")

    content = browser.get_content()
    logger.debug(f"Retrieved {len(content)} bytes from {url}")

    return content


def cleanup():
    """Cleanup browser resources."""
    browser = BrowserManager()
    browser.close()
