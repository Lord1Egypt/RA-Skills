"""LinkedIn login management."""

from __future__ import annotations

import logging
import time

from .bridge import BridgePage
from .human import sleep_random
from .selectors import LOGGED_IN_NAV, NOT_LOGGED_IN
from .urls import HOME_URL, LOGOUT_URL

logger = logging.getLogger(__name__)


def check_login_status(page: BridgePage) -> bool:
    """Check if user is logged in to LinkedIn.

    Returns:
        True if logged in, False otherwise.
    """
    current_url = page.evaluate("location.href") or ""
    if "linkedin.com" not in current_url:
        page.navigate(HOME_URL)
        page.wait_for_load()

    page.wait_dom_stable(timeout=5.0)

    deadline = time.monotonic() + 10.0
    while time.monotonic() < deadline:
        if page.has_element(LOGGED_IN_NAV):
            return True
        if page.has_element(NOT_LOGGED_IN):
            return False
        time.sleep(0.3)

    return page.has_element(LOGGED_IN_NAV)


def get_current_username(page: BridgePage) -> str:
    """Get the currently logged-in user's profile slug or display name.

    Returns:
        Profile slug or display name, or empty string if not logged in.
    """
    try:
        if not check_login_status(page):
            return ""

        username = page.evaluate(
            """
            (() => {
                // Try to extract profile slug from the "Me" nav link
                const meLink = document.querySelector(
                    '.global-nav__me > a[href*="/in/"], ' +
                    '.global-nav__primary-link[href*="/in/"]'
                );
                if (meLink) {
                    const href = meLink.getAttribute('href') || '';
                    const m = href.match(/\\/in\\/([^/?#]+)/);
                    if (m && m[1]) return m[1];
                }
                // Fallback: profile photo alt text (display name)
                const photo = document.querySelector('.global-nav__me-photo');
                if (photo) {
                    const alt = photo.getAttribute('alt') || '';
                    if (alt) return alt;
                }
                return '';
            })()
            """
        )
        return username or ""
    except Exception:
        logger.warning("Failed to get username")
        return ""


def logout(page: BridgePage) -> bool:
    """Log out of LinkedIn.

    Tries the UI dropdown first, falls back to the direct logout URL.

    Returns:
        True if logged out (or was not logged in).
    """
    page.navigate(HOME_URL)
    page.wait_for_load()
    sleep_random(800, 1500)

    if not check_login_status(page):
        logger.info("Not logged in")
        return False

    # Try UI dropdown sign-out
    me_btn = (
        ".global-nav__me-content, "
        ".nav-settings__dropdown-trigger, "
        "#nav-settings__dropdown-trigger"
    )
    try:
        page.click_element(me_btn)
        sleep_random(600, 1000)
        sign_out = (
            'a[href*="/logout"], '
            'a[data-control-name="nav.settings_sign_out"]'
        )
        page.click_element(sign_out)
        sleep_random(1000, 2000)
        logger.info("Logged out via UI")
        return True
    except Exception as e:
        logger.warning("UI logout failed: %s. Trying direct logout URL.", e)

    # Fallback: direct logout URL
    try:
        page.navigate(LOGOUT_URL)
        page.wait_for_load()
        return True
    except Exception as e2:
        logger.error("Direct logout failed: %s", e2)
        return False
