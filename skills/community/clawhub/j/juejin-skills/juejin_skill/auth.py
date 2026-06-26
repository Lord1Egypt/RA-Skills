"""Playwright-based browser authentication for Juejin."""

from __future__ import annotations

import json
import os
from typing import Any

from juejin_skill.config import JUEJIN_WEB_URL, COOKIE_FILE_PATH
from juejin_skill.utils import save_json_file, load_json_file


class JuejinAuth:
    """Handle login via Playwright and cookie persistence.

    Workflow
    --------
    1. Call :meth:`login_with_browser` – opens a Chromium window pointing to
       the Juejin login page, waits for the user to complete login manually
       (scan QR, password, etc.), then captures cookies.
    2. Cookies are persisted to ``~/.juejin_cookie.json``.
    3. Later runs can call :meth:`load_cookie` to read the saved cookie.
    """

    def __init__(self, cookie_path: str = COOKIE_FILE_PATH) -> None:
        self._cookie_path = cookie_path
        self._cookie: str = ""

    # ------------------------------------------------------------------ #
    #  Browser login
    # ------------------------------------------------------------------ #

    def login_with_browser(self, headless: bool = False) -> str:
        """Open a browser window for the user to log in and return the cookie string.

        Parameters
        ----------
        headless : bool
            Whether to run the browser in headless mode (default ``False``
            so the user can interact with the login UI).

        Returns
        -------
        str
            A cookie string suitable for the ``Cookie`` HTTP header.
        """
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError(
                "Playwright is required for browser login. "
                "Install it with: pip install playwright && playwright install chromium"
            ) from exc

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=headless)
            context = browser.new_context()
            page = context.new_page()

            # Navigate to the Juejin login page
            page.goto(f"{JUEJIN_WEB_URL}/login")
            print("[JuejinAuth] Browser opened. Please log in to Juejin...")
            print("[JuejinAuth] The browser will close automatically after login is detected.")

            # Poll for the session cookie that indicates a successful login.
            # Juejin sets 'sessionid' or 'sessionid_ss' after authentication.
            import time
            max_wait = 300  # 5 minutes
            poll_interval = 2  # seconds
            elapsed = 0
            logged_in = False

            while elapsed < max_wait:
                time.sleep(poll_interval)
                elapsed += poll_interval
                cookies = context.cookies()
                cookie_names = {c["name"] for c in cookies}
                # Check for session cookies that prove the user is logged in
                if "sessionid" in cookie_names or "sessionid_ss" in cookie_names:
                    # Give a bit more time for all cookies to settle
                    page.wait_for_timeout(2000)
                    cookies = context.cookies()
                    logged_in = True
                    break

            if not logged_in:
                print("[JuejinAuth] Timed out waiting for login (5 minutes).")
                browser.close()
                return ""

            browser.close()

        cookie_str = self._cookies_to_string(cookies)
        self._cookie = cookie_str

        # Persist to disk
        self._save_cookies(cookies)
        print(f"[JuejinAuth] Login successful. Cookie saved to {self._cookie_path}")
        return cookie_str

    # ------------------------------------------------------------------ #
    #  Cookie I/O
    # ------------------------------------------------------------------ #

    def load_cookie(self) -> str:
        """Load cookie string from the saved file, or return empty string."""
        data = load_json_file(self._cookie_path)
        if data and isinstance(data, list):
            self._cookie = self._cookies_to_string(data)
            return self._cookie
        return ""

    def get_cookie(self) -> str:
        """Return the current cookie string (from login or loaded)."""
        return self._cookie

    def clear_cookie(self) -> None:
        """Delete the saved cookie file."""
        if os.path.exists(self._cookie_path):
            os.remove(self._cookie_path)
            print(f"[JuejinAuth] Cookie file removed: {self._cookie_path}")
        self._cookie = ""

    # ------------------------------------------------------------------ #
    #  Internal helpers
    # ------------------------------------------------------------------ #

    def _save_cookies(self, cookies: list[dict[str, Any]]) -> None:
        save_json_file(self._cookie_path, cookies)
        # Restrict the cookie file to the current user (0600) so that other
        # local users cannot read the Juejin session credential. This is a
        # best-effort hardening – on POSIX only.
        try:
            os.chmod(self._cookie_path, 0o600)
        except OSError:
            pass
        print(
            "[JuejinAuth] ⚠️  A Juejin session cookie has been stored at "
            f"{self._cookie_path}. Anyone with read access to this file can act "
            "as you on Juejin. Delete it when you no longer need authenticated "
            "access: rm " + self._cookie_path
        )

    @staticmethod
    def _cookies_to_string(cookies: list[dict[str, Any]]) -> str:
        """Convert Playwright cookie list to a ``Cookie`` header string."""
        return "; ".join(f"{c['name']}={c['value']}" for c in cookies)
