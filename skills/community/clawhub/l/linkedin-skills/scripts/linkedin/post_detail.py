"""LinkedIn post detail and comments."""

from __future__ import annotations

import json
import logging

from .bridge import BridgePage
from .errors import NoPostDetailError
from .human import sleep_random
from .types import Author, Comment, Post, PostDetail
from .urls import make_post_url

logger = logging.getLogger(__name__)

_EXTRACT_POST_DETAIL_JS = """
(() => {
    // Get the main post element
    const postEl = document.querySelector(
        '.occludable-update[data-urn], .feed-shared-update-v2'
    );
    let postData = {};
    if (postEl) {
        const urn = postEl.getAttribute('data-urn') || '';
        const nameEl = postEl.querySelector(
            '.update-components-actor__title .t-bold span[aria-hidden="true"],' +
            '.update-components-actor__name'
        );
        const name = nameEl ? nameEl.textContent.trim() : '';

        const profileLinkEl = postEl.querySelector(
            '.update-components-actor__meta-link, .update-components-actor__image-link'
        );
        const profileUrl = profileLinkEl
            ? (profileLinkEl.getAttribute('href') || '').split('?')[0]
            : '';

        const textEl = postEl.querySelector(
            '.feed-shared-update-v2__description .update-components-text,' +
            '.update-components-text'
        );
        const text = textEl ? textEl.innerText.trim() : '';

        const reactEl = postEl.querySelector(
            '.social-details-social-counts__reactions-count'
        );
        const reactions = reactEl
            ? parseInt(reactEl.textContent.replace(/[^0-9]/g, '') || '0', 10)
            : 0;

        postData = {
            urn,
            url: window.location.href,
            author: { name, profileUrl, headline: '' },
            text,
            stats: { reactions, comments: 0, reposts: 0 },
        };
    }

    // Collect visible comments
    const comments = [];
    document.querySelectorAll('.comments-comment-item').forEach(el => {
        try {
            const authorEl = el.querySelector(
                '.comments-post-meta__name-text span[aria-hidden="true"]'
            );
            const author = authorEl ? authorEl.textContent.trim() : '';
            const textEl = el.querySelector('.comments-comment-item__main-content');
            const text = textEl ? textEl.textContent.trim() : '';
            const timeEl = el.querySelector('.comments-comment-item__timestamp');
            const createdAt = timeEl ? timeEl.textContent.trim() : '';
            if (text) comments.push({ author: { name: author }, text, createdAt });
        } catch (e) {}
    });

    return JSON.stringify({ post: postData, comments });
})()
"""


def get_post_detail(page: BridgePage, post_url: str) -> PostDetail:
    """Get a LinkedIn post's content and top-level comments."""
    url = make_post_url(post_url)
    page.navigate(url)
    page.wait_for_load()
    page.wait_dom_stable()
    sleep_random(500, 1000)

    result = page.evaluate(_EXTRACT_POST_DETAIL_JS)
    data = json.loads(result or "{}")

    post_data = data.get("post", {})
    if not post_data:
        raise NoPostDetailError()

    post = Post.from_dict(post_data)

    comments = []
    for c in data.get("comments", []):
        author_info = c.get("author", {})
        author = Author(name=author_info.get("name", "") if isinstance(author_info, dict) else "")
        comments.append(
            Comment(
                author=author,
                text=c.get("text", ""),
                created_at=c.get("createdAt", ""),
            )
        )

    return PostDetail(post=post, comments=comments)
