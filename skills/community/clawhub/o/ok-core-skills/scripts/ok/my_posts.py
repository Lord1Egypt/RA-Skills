"""OK.com My Posts management.

List, filter by status, delete, and get edit URLs for the user's own posts.
Uses browser UI automation on the /biz/{lang}/publish/list page.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from . import selectors as sel
from .client.base import BaseClient
from .errors import OKElementNotFound, OKNotLoggedIn
from .human import medium_delay, short_delay

logger = logging.getLogger("ok-my-posts")

_MY_POSTS_TEMPLATE = "https://{sub}pub.ok.com/biz/{lang}/publish/list"

VALID_STATES = ("active", "pending", "expired", "draft")


@dataclass
class MyPostItem:
    title: str
    url: str | None = None
    price: str | None = None
    image_url: str | None = None
    address: str | None = None
    stats: str | None = None


@dataclass
class MyPostsResult:
    total: int = 0
    state: str = "active"
    items: list[MyPostItem] = field(default_factory=list)
    url: str | None = None


def _navigate_to_my_posts(
    client: BaseClient,
    subdomain: str = "sg",
    lang: str = "en",
) -> str:
    url = _MY_POSTS_TEMPLATE.format(sub=subdomain, lang=lang)
    client.navigate(url)
    client.wait_dom_stable(timeout=15000)
    medium_delay()

    current = client.get_url() or ""
    if "login" in current.lower():
        raise OKNotLoggedIn("Login required to view my posts")

    if not client.has_element(sel.USER_AVATAR):
        raise OKNotLoggedIn(
            f"Not logged in on {subdomain}.ok.com, please login first"
        )
    return current


def list_my_posts(
    client: BaseClient,
    subdomain: str = "sg",
    lang: str = "en",
    state: str = "active",
    max_results: int = 50,
) -> MyPostsResult:
    """List the current user's posts, optionally filtered by state."""
    final_url = _navigate_to_my_posts(client, subdomain, lang)

    if state.lower() != "active":
        _click_state_tab(client, state)

    items = _extract_post_cards(client, max_results)
    logger.info("My posts (%s): found %d", state, len(items))

    return MyPostsResult(
        total=len(items),
        state=state.lower(),
        items=items,
        url=final_url,
    )


def _click_state_tab(client: BaseClient, state: str) -> None:
    state_lower = state.lower()
    if state_lower not in VALID_STATES:
        logger.warning("Invalid state: %s, valid: %s", state, VALID_STATES)
        return

    js = f"""(() => {{
        const tabs = document.querySelectorAll("{sel.MY_POST_STATE_TABS}");
        for (const tab of tabs) {{
            const text = tab.textContent.trim().toLowerCase();
            if (text === '{state_lower}') {{
                tab.click();
                return true;
            }}
        }}
        return false;
    }})()"""

    clicked = client.evaluate(js)
    if clicked:
        client.wait_dom_stable(timeout=10000)
        short_delay()
        logger.info("Switched to state: %s", state)
    else:
        logger.warning("State tab not found: %s", state)


def _extract_post_cards(
    client: BaseClient, max_results: int
) -> list[MyPostItem]:
    has_empty = client.evaluate(
        f'!!document.querySelector("{sel.MY_POST_EMPTY}")'
    )
    if has_empty:
        return []

    js = f"""(() => {{
        const cards = document.querySelectorAll("{sel.MY_POST_CARD}");
        const results = [];
        const limit = Math.min(cards.length, {max_results});
        for (let i = 0; i < limit; i++) {{
            const c = cards[i];
            const titleEl = c.querySelector("{sel.MY_POST_CARD_TITLE}");
            const priceEl = c.querySelector("{sel.MY_POST_CARD_PRICE}");
            const imgEl = c.querySelector("{sel.MY_POST_CARD_IMAGE}");
            const addrEl = c.querySelector("{sel.MY_POST_CARD_ADDRESS}");
            const statsEl = c.querySelector("{sel.MY_POST_CARD_STATS}");
            results.push({{
                title: titleEl ? titleEl.textContent.trim() : '',
                price: priceEl ? priceEl.textContent.trim() : '',
                image: imgEl ? imgEl.src : '',
                address: addrEl ? addrEl.textContent.trim() : '',
                stats: statsEl ? statsEl.textContent.trim() : ''
            }});
        }}
        return results;
    }})()"""

    raw = client.evaluate(js) or []
    items: list[MyPostItem] = []
    for r in raw:
        items.append(
            MyPostItem(
                title=r.get("title", ""),
                price=r.get("price") or None,
                image_url=r.get("image") or None,
                address=r.get("address") or None,
                stats=r.get("stats") or None,
            )
        )
    return items


def delete_post(
    client: BaseClient,
    subdomain: str = "sg",
    lang: str = "en",
    index: int = 0,
) -> dict:
    """Delete the post at *index* via UI: click '...' -> Delete -> confirm."""
    _navigate_to_my_posts(client, subdomain, lang)

    has_empty = client.evaluate(
        f'!!document.querySelector("{sel.MY_POST_EMPTY}")'
    )
    if has_empty:
        return {"success": False, "index": index, "message": "No posts"}

    # Click the '...' action button on the target card
    js = f"""(() => {{
        const cards = document.querySelectorAll("{sel.MY_POST_CARD}");
        if ({index} >= cards.length) return null;
        const card = cards[{index}];
        const title = (
            card.querySelector("{sel.MY_POST_CARD_TITLE}") || {{}}
        ).textContent || '';
        const btn = card.querySelector("{sel.MY_POST_ACTION_BTN}");
        if (btn) {{ btn.click(); return {{title: title}}; }}
        return {{title: title, noBtn: true}};
    }})()"""

    result = client.evaluate(js)
    if not result:
        raise OKElementNotFound(f"Post at index {index} not found")

    title = result.get("title", "")
    if result.get("noBtn"):
        return {
            "success": False,
            "index": index,
            "message": f"No action button: {title}",
        }

    short_delay()

    # Click 'Delete' in the dropdown
    js_del = f"""(() => {{
        const items = document.querySelectorAll(
            "{sel.MY_POST_DROPDOWN} {sel.MY_POST_DROPDOWN_ITEM}"
        );
        for (const item of items) {{
            if (item.textContent.trim().toLowerCase() === 'delete') {{
                item.click();
                return true;
            }}
        }}
        return false;
    }})()"""
    clicked = client.evaluate(js_del)
    if not clicked:
        return {
            "success": False,
            "index": index,
            "message": f"Delete option not found: {title}",
        }

    short_delay()
    _confirm_delete(client)
    medium_delay()

    return {"success": True, "index": index, "message": f"Deleted: {title}"}


def _confirm_delete(client: BaseClient) -> None:
    """Click the confirm button in the delete confirmation dialog."""
    js = """(() => {
        const btns = document.querySelectorAll(
            '[class*="modal"] button, [class*="Modal"] button, ' +
            '[class*="dialog"] button, [class*="Dialog"] button, ' +
            '[class*="confirm"] button, button[class*="confirm"], ' +
            'button[class*="Confirm"], .modal-footer button'
        );
        for (const btn of btns) {
            const text = btn.textContent.trim().toLowerCase();
            if (['delete','confirm','yes','ok'].includes(text)) {
                btn.click();
                return true;
            }
        }
        return false;
    })()"""
    client.evaluate(js)


def get_edit_url(
    client: BaseClient,
    subdomain: str = "sg",
    lang: str = "en",
    index: int = 0,
) -> dict:
    """Click '...' -> Edit on the target post to open the edit form.

    ok.com uses SPA navigation, so clicking Edit may change the page
    content without altering the URL.  We return the final URL (which
    may or may not differ) together with a success flag.
    """
    _navigate_to_my_posts(client, subdomain, lang)

    has_empty = client.evaluate(
        f'!!document.querySelector("{sel.MY_POST_EMPTY}")'
    )
    if has_empty:
        return {
            "success": False,
            "url": None,
            "title": "",
            "index": index,
            "message": "No posts",
        }

    # Click the '...' action button
    js = f"""(() => {{
        const cards = document.querySelectorAll("{sel.MY_POST_CARD}");
        if ({index} >= cards.length) return null;
        const card = cards[{index}];
        const title = (
            card.querySelector("{sel.MY_POST_CARD_TITLE}") || {{}}
        ).textContent || '';
        const btn = card.querySelector("{sel.MY_POST_ACTION_BTN}");
        if (btn) {{ btn.click(); return {{title: title}}; }}
        return {{title: title, noBtn: true}};
    }})()"""

    result = client.evaluate(js)
    if not result:
        raise OKElementNotFound(f"Post at index {index} not found")

    title = result.get("title", "")
    if result.get("noBtn"):
        return {
            "success": False,
            "url": None,
            "title": title,
            "index": index,
            "message": "No action button",
        }

    short_delay()

    # Click 'Edit' in the dropdown
    js_edit = f"""(() => {{
        const items = document.querySelectorAll(
            "{sel.MY_POST_DROPDOWN} {sel.MY_POST_DROPDOWN_ITEM}"
        );
        for (const item of items) {{
            if (item.textContent.trim().toLowerCase() === 'edit') {{
                item.click();
                return true;
            }}
        }}
        return false;
    }})()"""
    clicked = client.evaluate(js_edit)
    if not clicked:
        return {
            "success": False,
            "url": None,
            "title": title,
            "index": index,
            "message": "Edit option not found",
        }

    medium_delay()
    client.wait_dom_stable(timeout=10000)
    edit_url = client.get_url() or ""

    return {
        "success": True,
        "url": edit_url,
        "title": title,
        "index": index,
    }
