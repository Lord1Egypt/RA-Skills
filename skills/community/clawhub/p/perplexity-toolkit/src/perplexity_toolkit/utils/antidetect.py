"""Anti-detection utilities — human-like timing, input, and behavior."""

import json
import random
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..drivers.base import BrowserDriver


# ──────────────────────────────────────────────
# Timing helpers
# ──────────────────────────────────────────────

def human_delay(lo: float = 0.5, hi: float = 2.0):
    """Random delay simulating human pause/think time."""
    time.sleep(random.uniform(lo, hi))


def micro_delay(lo: float = 0.05, hi: float = 0.15):
    """Tiny delay between keystrokes or micro-actions."""
    time.sleep(random.uniform(lo, hi))


# ──────────────────────────────────────────────
# Human-like typing via CDP Input.dispatchKeyEvent
# ──────────────────────────────────────────────

def human_type(driver: "BrowserDriver", text: str,
               base_delay: float = 0.06, jitter: float = 0.09):
    """Type text character by character with realistic timing.

    Uses CDP Input.dispatchKeyEvent which is indistinguishable from
    real keyboard input (same protocol as physical keystrokes).

    Args:
        driver: BrowserDriver with .cdp() support.
        text: Text to type.
        base_delay: Base ms between keystrokes.
        jitter: Random extra ms added to base_delay.
    """
    for ch in text:
        # keyDown
        driver.cdp("Input.dispatchKeyEvent", {
            "type": "keyDown",
            "text": ch,
            "key": ch,
            "code": f"Key{ch.upper()}" if ch.isalpha() else "",
            "unmodifiedText": ch,
        })
        # keyUp
        driver.cdp("Input.dispatchKeyEvent", {
            "type": "keyUp",
            "text": ch,
            "key": ch,
            "code": f"Key{ch.upper()}" if ch.isalpha() else "",
        })
        time.sleep(base_delay + random.uniform(0, jitter))


def human_paste(driver: "BrowserDriver", text: str,
                chunk_size: int = 5, delay: float = 0.08):
    """Paste text in small chunks with pauses — faster than per-char typing.

    Simulates a human who types fast in bursts then pauses.
    Uses CDP Input.insertText for each chunk (still not detectable).
    """
    i = 0
    while i < len(text):
        # Vary chunk size slightly
        chunk_len = random.randint(max(1, chunk_size - 2), chunk_size + 3)
        chunk = text[i:i + chunk_len]
        driver.cdp("Input.insertText", {"text": chunk})
        i += chunk_len
        # Pause between chunks
        if i < len(text):
            time.sleep(delay + random.uniform(0, delay * 0.5))


# ──────────────────────────────────────────────
# Mouse movement simulation
# ──────────────────────────────────────────────

def human_mouse_move(driver: "BrowserDriver", x: int, y: int,
                     steps: int = 8):
    """Move mouse to (x, y) with a curved trajectory.

    Real humans don't move in straight lines — they overshoot
    slightly and correct. Uses cubic Bezier for natural curve.
    """
    # Current position (approximate — use page center as start)
    start_x, start_y = 400, 300

    # Random control points for Bezier curve
    cp1_x = start_x + (x - start_x) * 0.3 + random.randint(-50, 50)
    cp1_y = start_y + (y - start_y) * 0.1 + random.randint(-30, 30)
    cp2_x = start_x + (x - start_x) * 0.7 + random.randint(-30, 30)
    cp2_y = start_y + (y - start_y) * 0.9 + random.randint(-20, 20)

    for i in range(steps + 1):
        t = i / steps
        # Cubic Bezier interpolation
        mt = 1 - t
        px = int(mt**3 * start_x + 3 * mt**2 * t * cp1_x +
                 3 * mt * t**2 * cp2_x + t**3 * x)
        py = int(mt**3 * start_y + 3 * mt**2 * t * cp1_y +
                 3 * mt * t**2 * cp2_y + t**3 * y)

        driver.cdp("Input.dispatchMouseEvent", {
            "type": "mouseMoved",
            "x": px, "y": py,
        })
        time.sleep(random.uniform(0.01, 0.03))

    # Small overshoot correction
    time.sleep(random.uniform(0.02, 0.05))
    driver.cdp("Input.dispatchMouseEvent", {
        "type": "mouseMoved",
        "x": x, "y": y,
    })


def human_click(driver: "BrowserDriver", x: int, y: int,
                move_mouse: bool = True):
    """Click at (x, y) with human-like mouse movement + delay.

    Args:
        driver: BrowserDriver with .cdp() support.
        x, y: Target coordinates.
        move_mouse: Whether to simulate mouse movement first.
    """
    if move_mouse:
        human_mouse_move(driver, x, y)

    time.sleep(random.uniform(0.05, 0.12))

    driver.cdp("Input.dispatchMouseEvent", {
        "type": "mousePressed", "x": x, "y": y,
        "button": "left", "clickCount": 1,
    })
    time.sleep(random.uniform(0.04, 0.08))

    driver.cdp("Input.dispatchMouseEvent", {
        "type": "mouseReleased", "x": x, "y": y,
        "button": "left", "clickCount": 1,
    })


# ──────────────────────────────────────────────
# Scroll simulation
# ──────────────────────────────────────────────

def human_scroll(driver: "BrowserDriver", direction: str = "down",
                 amount: int = 3, delay: float = 0.3):
    """Scroll with variable speed — slower at start/end."""
    for i in range(amount):
        delta_y = random.randint(100, 300) * (1 if direction == "down" else -1)
        driver.cdp("Input.dispatchMouseEvent", {
            "type": "mouseWheel", "x": 400, "y": 400,
            "deltaX": 0, "deltaY": delta_y,
        })
        # Ease in/out: slower at start and end
        if i == 0 or i == amount - 1:
            time.sleep(delay * 1.5)
        else:
            time.sleep(delay + random.uniform(-0.1, 0.1))


# ──────────────────────────────────────────────
# JS call consolidation
# ──────────────────────────────────────────────

def combined_snapshot_and_info(driver: "BrowserDriver") -> dict:
    """Get snapshot + page info + check if search done in ONE evaluate call.

    Consolidates what would normally be 3 separate evaluate() calls
    into a single CDP round-trip.
    """
    result = driver.evaluate("""(() => {
        const info = {
            url: location.href,
            title: document.title,
            done: false,
            hasInput: !!document.querySelector("[contenteditable]")
        };
        const btns = Array.from(document.querySelectorAll("button"));
        info.done = btns.some(b => b.innerText.includes("已完成"));
        info.expandable = btns.some(b => b.innerText.includes("查看更多"));
        return JSON.stringify(info);
    })()""")
    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {}
    return result if isinstance(result, dict) else {}


def combined_extract(driver: "BrowserDriver") -> dict:
    """Extract answer + sources + follow-ups in ONE evaluate call.

    Normally this is 4+ separate evaluate() calls.
    """
    result = driver.evaluate("""(() => {
        const main = document.querySelector("main");
        const r = {answer: "", sources: [], follow_ups: []};
        if (!main) return JSON.stringify(r);

        r.answer = main.innerText;

        // Sources
        const seen = new Set();
        r.sources = Array.from(main.querySelectorAll("a[href]"))
            .map(a => ({text: a.textContent.trim().substring(0, 200), href: a.href}))
            .filter(l => l.href.startsWith("http") && !l.href.includes("perplexity.ai") && l.text.length > 2)
            .filter(l => { if (seen.has(l.href)) return false; seen.add(l.href); return true; });

        // Follow-ups
        const skip = new Set(["分享","搜索","Computer","Ming","Pro","添加","展开","完成","来源","会话","答案","链接","图片"]);
        r.follow_ups = Array.from(document.querySelectorAll("button"))
            .map(b => b.innerText.trim())
            .filter(t => t.length > 20 && t.length < 200 && ![...skip].some(s => t.includes(s)))
            .slice(0, 5);

        return JSON.stringify(r);
    })()""")
    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"answer": "", "sources": [], "follow_ups": []}
    return result if isinstance(result, dict) else {"answer": "", "sources": [], "follow_ups": []}


def lognormal_delay(mu: float = -0.5, sigma: float = 0.5):
    """Lognormal delay — fast responses common, slow ones rare."""
    delay = random.lognormvariate(mu, sigma)
    time.sleep(delay)


def distraction_delay(chance: float = 0.05, lo: float = 3.0, hi: float = 5.0):
    """Occasional long pause simulating human distraction (5% default)."""
    if random.random() < chance:
        time.sleep(random.uniform(lo, hi))
