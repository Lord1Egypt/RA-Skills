"""
Scrapes reels from public Instagram profiles using a headless browser (Playwright).
Logs in with INSTAGRAM_USERNAME / INSTAGRAM_PASSWORD (from .env) when provided,
which avoids the login wall that blocks headless browsers in sandboxed environments.
Session cookies are saved to .instagram_session.json and reused on subsequent runs.
"""

import json
import tempfile
import requests
from pathlib import Path
from datetime import datetime, timedelta, timezone

from playwright.sync_api import sync_playwright, Response

import config


# ── constants ─────────────────────────────────────────────────────────────────

SESSION_FILE = Path(__file__).parent / ".instagram_session.json"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)
VIEWPORT = {"width": 1280, "height": 900}


# ── helpers ───────────────────────────────────────────────────────────────────

def _ts_to_dt(ts: int) -> datetime:
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def _find_posts(data, found: list, depth: int = 0) -> None:
    """Recursively find post nodes in a nested JSON structure."""
    if depth > 12:
        return
    if isinstance(data, dict):
        if "shortcode" in data and "taken_at_timestamp" in data:
            found.append(data)
            return
        for v in data.values():
            _find_posts(v, found, depth + 1)
    elif isinstance(data, list):
        for item in data:
            _find_posts(item, found, depth + 1)


def _download_thumbnail(url: str, dest: Path) -> bool:
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            dest.write_bytes(r.content)
            return True
    except Exception:
        pass
    return False


def _capture_json(response: Response, captured: list) -> None:
    if response.status != 200:
        return
    url = response.url
    if "graphql" not in url and "api/v1" not in url:
        return
    try:
        captured.append(response.json())
    except Exception:
        pass


def _get_storage_state(p) -> dict | None:
    """
    Returns a Playwright storage_state dict (cookies + localStorage) for Instagram.
    - If SESSION_FILE exists, loads and returns the saved session.
    - Otherwise logs in fresh using config credentials and saves the session.
    - Returns None if no credentials are configured or login fails.
    """
    if not config.INSTAGRAM_USERNAME or not config.INSTAGRAM_PASSWORD:
        return None

    # Reuse saved session
    if SESSION_FILE.exists():
        print("Loading saved Instagram session.")
        return json.loads(SESSION_FILE.read_text(encoding="utf-8"))

    # Fresh login — use a visible browser so the user can complete any
    # CAPTCHA or phone-verification challenge Instagram may present.
    print("Logging in to Instagram (a browser window will open) …")
    browser = p.chromium.launch(headless=False)
    ctx = browser.new_context(user_agent=USER_AGENT, viewport=VIEWPORT, locale="en-US")
    page = ctx.new_page()
    try:
        page.goto(
            "https://www.instagram.com/accounts/login/",
            wait_until="domcontentloaded",
            timeout=30_000,
        )
        page.wait_for_timeout(3_000)

        # Dismiss cookie/consent dialogs if present
        for selector in [
            'button:has-text("Allow all cookies")',
            'button:has-text("Accept All")',
            'button:has-text("Accept")',
            '[data-testid="cookie-policy-manage-dialog-accept-button"]',
        ]:
            try:
                btn = page.query_selector(selector)
                if btn and btn.is_visible():
                    btn.click()
                    page.wait_for_timeout(1_500)
                    break
            except Exception:
                pass

        # Wait explicitly for the login form
        page.wait_for_selector('input[name="username"]', state="visible", timeout=30_000)

        page.fill('input[name="username"]', config.INSTAGRAM_USERNAME)
        page.fill('input[name="password"]', config.INSTAGRAM_PASSWORD)
        page.click('button[type="submit"]')

        # Wait up to 60 s for the user to pass any challenge Instagram shows
        print("  Waiting for login to complete (complete any verification if prompted) …")
        try:
            page.wait_for_url(
                lambda url: "accounts/login" not in url and "challenge" not in url,
                timeout=60_000,
            )
        except Exception:
            pass  # fall through to URL check below

        if "accounts/login" not in page.url and "challenge" not in page.url:
            state = ctx.storage_state()
            SESSION_FILE.write_text(json.dumps(state), encoding="utf-8")
            print("  Login successful — session saved.")
            return state
        else:
            print("  Login failed or challenge not completed. Delete .instagram_session.json and try again.")
            return None
    except Exception as e:
        print(f"  Login error: {e}")
        return None
    finally:
        page.close()
        browser.close()


# ── main scrape ───────────────────────────────────────────────────────────────

def scrape() -> tuple[dict, Path]:
    """
    Returns:
        results  – dict keyed by username:
                   {"reels": [...], "stories": [...]}
                   Each reel item has "path" (thumbnail jpg), "type"="image", and metadata.
        base_dir – temporary directory holding downloaded files.
                   Caller is responsible for cleanup.
    """
    base_dir = Path(tempfile.mkdtemp(prefix="insta_digest_"))
    results: dict = {}
    cutoff = datetime.now(tz=timezone.utc) - timedelta(hours=config.LOOKBACK_HOURS)

    with sync_playwright() as p:
        storage_state = _get_storage_state(p)

        browser = p.chromium.launch(headless=True)
        ctx_kwargs = dict(
            user_agent=USER_AGENT,
            viewport=VIEWPORT,
            locale="en-US",
        )
        if storage_state:
            ctx_kwargs["storage_state"] = storage_state

        ctx = browser.new_context(**ctx_kwargs)

        for username in config.INSTAGRAM_ACCOUNTS:
            print(f"\nScraping @{username} …")
            account_data: dict = {"reels": [], "stories": []}
            account_dir = base_dir / username
            account_dir.mkdir(parents=True, exist_ok=True)

            captured: list[dict] = []
            page = ctx.new_page()
            page.on("response", lambda r: _capture_json(r, captured))

            try:
                page.goto(
                    f"https://www.instagram.com/{username}/",
                    wait_until="networkidle",
                    timeout=30_000,
                )
                page.wait_for_timeout(2_000)
            except Exception as e:
                print(f"  Error loading page: {e}")
                page.close()
                results[username] = account_data
                continue

            # Extract all post nodes from captured API responses
            raw_posts: list[dict] = []
            for blob in captured:
                _find_posts(blob, raw_posts)

            # Deduplicate by shortcode and sort newest-first
            seen: set = set()
            posts: list[dict] = []
            for post in raw_posts:
                sc = post.get("shortcode")
                if sc and sc not in seen:
                    seen.add(sc)
                    posts.append(post)
            posts.sort(key=lambda x: x.get("taken_at_timestamp", 0), reverse=True)

            if not posts:
                print("  No posts found (Instagram may have shown a login wall).")
                page.close()
                results[username] = account_data
                continue

            reel_count = 0
            for post in posts[:30]:
                if reel_count >= config.MAX_REELS_PER_ACCOUNT:
                    break
                if not post.get("is_video", False):
                    continue

                post_dt = _ts_to_dt(post.get("taken_at_timestamp", 0))
                if post_dt < cutoff:
                    continue

                shortcode = post.get("shortcode", "")
                thumb_url = post.get("thumbnail_src") or post.get("display_url", "")
                thumb_path = account_dir / f"reel_{shortcode}.jpg"

                downloaded = thumb_url and _download_thumbnail(thumb_url, thumb_path)

                caption_edges = post.get("edge_media_to_caption", {}).get("edges", [])
                caption = caption_edges[0]["node"]["text"] if caption_edges else ""

                account_data["reels"].append({
                    "path":      str(thumb_path) if downloaded else "",
                    "type":      "image",
                    "shortcode": shortcode,
                    "caption":   caption[:300],
                    "likes":     post.get("edge_liked_by", {}).get("count", 0),
                    "url":       f"https://www.instagram.com/p/{shortcode}/",
                    "date":      datetime.fromtimestamp(
                                     post.get("taken_at_timestamp", 0)
                                 ).strftime("%Y-%m-%d %H:%M"),
                })
                reel_count += 1
                print(f"  + reel {shortcode}")

            page.close()
            results[username] = account_data

        browser.close()

    return results, base_dir
