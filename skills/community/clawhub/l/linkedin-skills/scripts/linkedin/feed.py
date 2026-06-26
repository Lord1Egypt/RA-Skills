"""LinkedIn home feed."""

from __future__ import annotations

import json
import logging
import time

from .bridge import BridgePage
from .errors import NoPostsError
from .human import sleep_random
from .selectors import FEED_POST
from .types import Post
from .urls import HOME_URL

logger = logging.getLogger(__name__)

_EXTRACT_FEED_JS = """
(() => {
    const posts = [];
    // LinkedIn 2025+: stable anchor = "Open control menu for post by X" button
    const menuBtns = document.querySelectorAll('button[aria-label^="Open control menu for post by"]');
    menuBtns.forEach(btn => {
        try {
            const authorName = btn.getAttribute('aria-label')
                .replace('Open control menu for post by ', '').trim();

            // Walk up to the post root container
            let root = btn;
            for (let i = 0; i < 12; i++) {
                root = root.parentElement;
                if (!root) break;
                if (root.offsetHeight > 150) break;
            }
            if (!root) return;

            const profileLink = root.querySelector('a[href*="/in/"], a[href*="/company/"]');
            const profileUrl = profileLink ? profileLink.href.split('?')[0] : '';

            // Extract post text: skip header lines, take body
            const lines = (root.innerText || '').split('\\n')
                .map(l => l.trim())
                .filter(l => l && l !== 'Feed post' && !l.startsWith('•'));
            const authorIdx = lines.findIndex(l => l === authorName);
            const textLines = authorIdx >= 0 ? lines.slice(authorIdx + 3) : lines.slice(3);
            const text = textLines.join('\\n').substring(0, 600);

            // Reaction count from aria-label like "1,234 reactions"
            const reactBtn = root.querySelector('button[aria-label*="reaction"]');
            const reactMatch = reactBtn
                ? reactBtn.getAttribute('aria-label').match(/([\\d,]+)/)
                : null;
            const reactions = reactMatch
                ? parseInt(reactMatch[1].replace(',', ''), 10)
                : 0;

            posts.push({
                urn: '',
                url: profileUrl,
                author: { name: authorName, profileUrl, headline: '' },
                text,
                createdAt: '',
                stats: { reactions, comments: 0, reposts: 0 },
            });
        } catch (e) {}
    });
    return JSON.stringify(posts);
})()
"""


def home_feed(page: BridgePage) -> list[Post]:
    """Get posts from the LinkedIn home feed."""
    page.navigate(HOME_URL)
    page.wait_for_load()
    page.wait_dom_stable()
    sleep_random(500, 1000)
    # Scroll to trigger lazy-loaded posts
    page.evaluate("window.scrollBy(0, 500)")
    sleep_random(2000, 3000)
    return _extract_posts(page)


def _extract_posts(page: BridgePage) -> list[Post]:
    _wait_for_posts(page)

    result = page.evaluate(_EXTRACT_FEED_JS)
    if not result:
        raise NoPostsError()

    posts_data = json.loads(result)
    if not posts_data:
        raise NoPostsError()

    return [Post.from_dict(p) for p in posts_data]


def _wait_for_posts(page: BridgePage, timeout: float = 15.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        count = page.get_elements_count(FEED_POST)
        if count > 0:
            return
        time.sleep(0.5)
    logger.warning("Timeout waiting for feed posts to load")
