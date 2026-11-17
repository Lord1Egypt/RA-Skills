"""DOM parsing and interaction utilities for Perplexity."""

import json
import logging
import random
import re
import time
from typing import Optional

logger = logging.getLogger(__name__)


def compact_json(tree) -> str:
    """Convert accessibility tree to compact JSON string (no spaces)."""
    return json.dumps(tree, ensure_ascii=False, separators=(",", ":"))


def _find_by_role(node, target_role: str, name_contains: str = "") -> Optional[str]:
    """Recursively find the first node with a matching role (and optionally a
    name containing name_contains), returning its ref (e.g. "@e42").

    Walks the parsed JSON tree, so it is immune to field ordering changes in
    the WebBridge accessibility-tree output.
    """
    if isinstance(node, dict):
        if node.get("role") == target_role:
            name = node.get("name") or ""
            if not name_contains or name_contains in name:
                return node.get("ref")
        for v in node.values():
            result = _find_by_role(v, target_role, name_contains)
            if result:
                return result
    elif isinstance(node, list):
        for item in node:
            result = _find_by_role(item, target_role, name_contains)
            if result:
                return result
    return None


def _load_tree(s):
    """Parse the compact JSON accessibility tree.

    Already-parsed trees (dict/list input) pass through unchanged. Returns
    None when s is not valid JSON.
    """
    if not isinstance(s, str):
        return s
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return None


# --- Regex fallbacks (used only when json.loads fails) ---

def _find_ref_by_role_regex(s: str, role: str, name_pattern: str = "") -> Optional[str]:
    """Old order-dependent regex fallback for find_ref_by_role."""
    if name_pattern:
        pat = rf'"role":"{role}","name":"[^"]*{re.escape(name_pattern)}[^"]*","ref":"(@e\d+)"'
    else:
        pat = rf'"role":"{role}"[^}}]*"ref":"(@e\d+)"'
    for m in re.finditer(pat, s):
        return m.group(1)
    return None


def _find_textbox_regex(s: str) -> Optional[str]:
    """Old order-dependent regex fallback for find_textbox."""
    # Primary: textbox with value field
    for m in re.finditer(
        r'"role":"textbox","name":"[^"]*","value":"[^"]*","ref":"(@e\d+)"', s
    ):
        return m.group(1)
    # Fallback: any textbox
    return _find_ref_by_role_regex(s, "textbox")


def _find_menuitem_regex(s: str, text: str) -> Optional[str]:
    """Old order-dependent regex fallback for find_menuitem."""
    for m in re.finditer(
        rf'"role":"menuitem","name":"([^"]*{re.escape(text)}[^"]*)","ref":"(@e\d+)"',
        s,
    ):
        return m.group(2)
    return None


# --- Public lookups: JSON tree traversal first, regex fallback ---

def find_ref_by_role(s: str, role: str, name_pattern: str = "") -> Optional[str]:
    """Find an @e ref by role and optional name pattern in compact JSON."""
    tree = _load_tree(s)
    if tree is not None:
        return _find_by_role(tree, role, name_pattern)
    return _find_ref_by_role_regex(s, role, name_pattern)


def find_textbox(s: str) -> Optional[str]:
    """Find the Perplexity search textbox @e ref."""
    tree = _load_tree(s)
    if tree is not None:
        return _find_by_role(tree, "textbox")
    return _find_textbox_regex(s)


def find_menuitem(s: str, text: str) -> Optional[str]:
    """Find a menuitem @e ref by partial text match."""
    tree = _load_tree(s)
    if tree is not None:
        return _find_by_role(tree, "menuitem", text)
    return _find_menuitem_regex(s, text)


def _press_enter(driver) -> None:
    """Send a trusted Enter keypress via CDP.

    CDP Input.dispatchKeyEvent follows the real keyboard input path, so the
    page receives isTrusted=true keydown/keyup events — indistinguishable
    from a physical Enter key. Unlike dispatchEvent() (isTrusted=false),
    this is invisible to Perplexity's bot detection.
    """
    driver.cdp("Input.dispatchKeyEvent", {
        "type": "keyDown", "key": "Enter", "code": "Enter",
        "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13,
    })
    driver.cdp("Input.dispatchKeyEvent", {
        "type": "keyUp", "key": "Enter", "code": "Enter",
        "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13,
    })


def _submit_started(driver) -> bool:
    """Check whether the page started processing the query.

    Signals: input cleared (Perplexity clears it on submit), a
    stop-generating button, a loading spinner, or thinking/loading text.
    """
    result = driver.evaluate("""(() => {
        const el = document.querySelector("[contenteditable]");
        const inputCleared = !el || el.innerText.trim().length === 0;
        const stopBtn = Array.from(document.querySelectorAll("button"))
            .some(b => /停止|stop generating|^stop$/i.test(b.innerText.trim()));
        const loader = !!document.querySelector(
            "[data-testid*=loading], [class*=spinner], [class*=thinking], [class*=loader]");
        const thinking = /正在思考|思考中|searching|generating|loading/i
            .test(document.body.textContent || "");
        return JSON.stringify({started: inputCleared || stopBtn || loader || thinking});
    })()""")
    if isinstance(result, str):
        try:
            return bool(json.loads(result).get("started"))
        except json.JSONDecodeError:
            return False
    if isinstance(result, dict):
        return bool(result.get("started"))
    return bool(result)


def submit_query(driver):
    """Submit the current query.

    Strategy: click the 提交 button (most reliable), then verify.
    Falls back to CDP Enter if button not found.

    Returns:
        str: "submitted", "submitted_retry", or "no submit detected".
    """
    # Primary: click the submit button
    clicked = driver.evaluate("""(() => {
        const btn = document.querySelector('button[aria-label="提交"]');
        if (btn) { btn.click(); return 'clicked'; }
        return 'no button';
    })()""")

    if clicked == 'clicked':
        time.sleep(random.uniform(1.0, 2.0))
        if _submit_started(driver):
            return "submitted"

    # Fallback: CDP Enter
    _press_enter(driver)
    time.sleep(random.uniform(0.8, 1.4))
    if _submit_started(driver):
        return "submitted_retry"

    return "no submit detected"
