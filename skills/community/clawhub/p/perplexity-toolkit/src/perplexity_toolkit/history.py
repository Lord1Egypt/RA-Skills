"""Perplexity history management — list, search, and delete conversations."""

import json
import logging
import time
from typing import Optional, List, TypedDict

from .config import Config, get_config
from .drivers.base import BrowserDriver
from .drivers import create_driver
from .utils import compact_json, _find_by_role, _load_tree
from .utils.antidetect import human_delay, micro_delay

logger = logging.getLogger(__name__)


class Conversation(TypedDict):
    href: str
    title: str


def _make_driver(config: Config, suffix: str = "history") -> BrowserDriver:
    return create_driver(config, suffix)


def _pointer_click(driver, x: int, y: int):
    """Send pointer events — required for Radix UI dropdowns."""
    js = (
        "(() => {"
        "const el = document.elementFromPoint(" + str(x) + "," + str(y) + ");"
        "if (!el) return;"
        "const opts = {bubbles:true, cancelable:true, clientX:" + str(x) + ", clientY:" + str(y) + ", pointerId:1, pointerType:'mouse'};"
        "el.dispatchEvent(new PointerEvent('pointerdown', opts));"
        "el.dispatchEvent(new PointerEvent('pointerup', opts));"
        "el.dispatchEvent(new PointerEvent('click', opts));"
        "})()"
    )
    driver.evaluate(js)


def _hover_conversation(driver, href_fragment: str) -> Optional[tuple]:
    """Hover over a conversation to reveal its menu button. Returns (x, y) of menu button."""
    result = driver.evaluate(f"""(() => {{
        const links = document.querySelectorAll('a[href*="/search/"]');
        for (const a of links) {{
            if (a.href.includes("{href_fragment}")) {{
                const rect = a.getBoundingClientRect();
                return JSON.stringify({{
                    x: Math.round(rect.x + rect.width / 2),
                    y: Math.round(rect.y + rect.height / 2),
                    w: Math.round(rect.width),
                    h: Math.round(rect.height),
                }});
            }}
        }}
        return null;
    }})()""")

    if not result:
        return None

    if isinstance(result, str):
        try:
            pos = json.loads(result)
        except json.JSONDecodeError:
            return None
    else:
        pos = result

    # Hover to reveal menu button
    driver.cdp("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": pos["x"], "y": pos["y"]})
    human_delay(0.5, 1.0)

    # Find the visible "会话操作" button
    result = driver.evaluate("""(() => {
        const btns = document.querySelectorAll('button[aria-label="会话操作"]');
        for (const b of btns) {
            const r = b.getBoundingClientRect();
            if (r.width > 0 && r.x > 0) {
                return JSON.stringify({x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
            }
        }
        return null;
    })()""")

    if not result:
        return None
    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return None
    return result


def _open_conversation_menu(driver, href_fragment: str) -> bool:
    """Open the context menu for a conversation. Returns True if menu opened."""
    pos = _hover_conversation(driver, href_fragment)
    if not pos:
        logger.warning("Could not find conversation: %s", href_fragment)
        return False

    # Click with pointer events (Radix UI requirement)
    _pointer_click(driver, pos["x"], pos["y"])
    human_delay(1.0, 1.5)

    # Verify menu opened
    result = driver.evaluate("""(() => {
        const items = document.querySelectorAll('[role=menuitem]');
        return Array.from(items).map(i => i.innerText.trim()).filter(t => t).join(',');
    })()""")

    if result and "删除" in str(result):
        logger.debug("Menu opened: %s", result)
        return True
    logger.warning("Menu did not open for %s", href_fragment)
    return False


def list_conversations(driver: BrowserDriver, limit: int = 50) -> List[Conversation]:
    """List all visible conversations in the sidebar."""
    result = driver.evaluate(f"""(() => {{
        const links = document.querySelectorAll('a[href*="/search/"]');
        const seen = new Set();
        const convos = [];
        for (const a of links) {{
            const href = a.href;
            if (seen.has(href)) continue;
            seen.add(href);
            convos.push({{
                href: href.split('/search/')[1] || href,
                title: a.getAttribute('aria-label') || '',
            }});
            if (convos.length >= {limit}) break;
        }}
        return JSON.stringify(convos);
    }})()""")

    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return []
    return result if isinstance(result, list) else []


def find_conversation(driver: BrowserDriver, query: str) -> List[Conversation]:
    """Search conversations by title substring."""
    all_convos = list_conversations(driver)
    query_lower = query.lower()
    return [c for c in all_convos if query_lower in c["title"].lower()]


def delete_conversation(
    driver: BrowserDriver,
    href_fragment: str,
    config: Optional[Config] = None,
) -> bool:
    """Delete a single conversation by its URL fragment (UUID).

    Flow: hover → open menu → click 删除 → confirm 删除.
    Returns True if deletion succeeded.
    """
    # Open menu
    if not _open_conversation_menu(driver, href_fragment):
        return False

    # Find and click "删除" menuitem via snapshot
    snap = driver.snapshot()
    tree = compact_json(snap.get("data", {}).get("tree", ""))
    parsed = _load_tree(tree)
    if not parsed:
        logger.error("Could not parse snapshot tree")
        return False

    def _find_all(node, role, name="", results=None):
        if results is None:
            results = []
        if isinstance(node, dict):
            if node.get("role") == role:
                n = node.get("name") or ""
                if not name or name in n:
                    results.append({"ref": node.get("ref"), "name": n})
            for v in node.values():
                _find_all(v, role, name, results)
        elif isinstance(node, list):
            for item in node:
                _find_all(item, role, name, results)
        return results

    # Click "删除" menuitem
    delete_items = _find_all(parsed, "menuitem", "删除")
    if not delete_items:
        logger.error("Could not find '删除' menuitem")
        return False

    driver.click(delete_items[0]["ref"])
    human_delay(1.0, 1.5)

    # Click confirm button in dialog
    snap = driver.snapshot()
    tree = compact_json(snap.get("data", {}).get("tree", ""))
    parsed = _load_tree(tree)
    if parsed:
        confirm_btns = _find_all(parsed, "button", "删除")
        if confirm_btns:
            driver.click(confirm_btns[-1]["ref"])
            human_delay(1.0, 1.5)
            logger.info("Deleted conversation: %s", href_fragment)
            return True

    logger.error("Could not find confirm button")
    return False


def delete_conversations(
    config: Optional[Config] = None,
    driver: Optional[BrowserDriver] = None,
    query: Optional[str] = None,
    hrefs: Optional[List[str]] = None,
    limit: int = 100,
    dry_run: bool = False,
) -> dict:
    """Delete multiple conversations matching query or href list.

    Args:
        config: Configuration.
        driver: Browser driver.
        query: Delete conversations matching this title substring.
        hrefs: Delete specific conversations by URL fragment (UUID).
        limit: Max conversations to check.
        dry_run: If True, only list what would be deleted.

    Returns:
        {deleted: int, failed: int, skipped: int, conversations: list}
    """
    cfg = config or get_config()
    drv = driver or _make_driver(cfg)

    # Navigate to home to ensure sidebar is visible
    drv.navigate(cfg.base_url, new_tab=False)
    time.sleep(cfg.page_load_wait)

    if hrefs:
        targets = [{"href": h, "title": ""} for h in hrefs]
    elif query:
        targets = find_conversation(drv, query)
        if not targets:
            logger.info("No conversations matching %r", query)
            return {"deleted": 0, "failed": 0, "skipped": 0, "conversations": []}
    else:
        targets = list_conversations(drv, limit)

    logger.info("Found %d conversations to delete%s",
                len(targets), " (DRY RUN)" if dry_run else "")

    deleted = 0
    failed = 0
    for t in targets:
        href = t["href"]
        title = t.get("title", "")
        if dry_run:
            logger.info("  [DRY RUN] Would delete: %s (%s)", title[:60], href[:20])
            continue

        success = delete_conversation(drv, href, cfg)
        if success:
            deleted += 1
            # Re-navigate to reset sidebar state
            drv.navigate(cfg.base_url, new_tab=False)
            time.sleep(2)
        else:
            failed += 1
            logger.warning("Failed to delete: %s (%s)", title[:60], href[:20])

        human_delay(1.0, 2.0)

    result = {"deleted": deleted, "failed": failed,
              "skipped": len(targets) - deleted - failed,
              "conversations": targets}
    logger.info("Delete complete: %d deleted, %d failed", deleted, failed)
    return result
