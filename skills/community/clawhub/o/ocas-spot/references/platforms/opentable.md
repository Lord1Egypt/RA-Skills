# OpenTable

**Status:** ⚠️ Working (session required)
**Method:** One-time manual browser login + Playwright session persistence
**Previously:** ❌ Blocked by Akamai CDN bot detection on direct requests

---

## Overview

OpenTable's Akamai CDN blocks headless browser automation and direct HTTP requests. The
workaround: run a **visible (headed) browser once** for manual login, save the session state,
then reuse it for subsequent headless checks. The saved session satisfies Akamai's
human-verification requirement.

---

## One-Time Login (spot.opentable.login)

Opens a visible browser window. The user logs in manually, then confirms in the terminal.
Session cookies and storage are saved to `{agent_root}/commons/data/ocas-spot/opentable-session.json`.

```python
from playwright.sync_api import sync_playwright
import json, os

SESSION_PATH = os.path.expanduser("{agent_root}/commons/data/ocas-spot/opentable-session.json")

def save_opentable_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Headed — user sees it
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto("https://www.opentable.com/login")
        input("Log in to OpenTable in the browser window, then press Enter here...")
        storage = ctx.storage_state()
        os.makedirs(os.path.dirname(SESSION_PATH), exist_ok=True)
        with open(SESSION_PATH, "w") as f:
            json.dump(storage, f)
        browser.close()
        print(f"Session saved to {SESSION_PATH}")
```

---

## Availability Check (with saved session)

```python
from playwright.sync_api import sync_playwright
import json, os

SESSION_PATH = os.path.expanduser("{agent_root}/commons/data/ocas-spot/opentable-session.json")

def check_opentable_availability(restaurant_slug: str, date: str, party_size: int = 2) -> dict:
    if not os.path.exists(SESSION_PATH):
        raise RuntimeError("No OpenTable session found. Run spot.opentable.login first.")

    with open(SESSION_PATH) as f:
        storage_state = json.load(f)

    url = f"https://www.opentable.com/{restaurant_slug}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(storage_state=storage_state)
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)

        times = page.evaluate("""() => {
            return [...document.querySelectorAll('[data-test="available-time"]')]
                .map(el => el.textContent.trim());
        }""")

        browser.close()
        return {
            "venue": restaurant_slug,
            "date": date,
            "party_size": party_size,
            "available": len(times) > 0,
            "times": times,
            "note": "Session-based check — re-run spot.opentable.login if blocked",
        }
```

---

## Session Maintenance

- Session cookies expire. If checks start failing with redirects to login, re-run `spot.opentable.login`.
- Session file path: `{agent_root}/commons/data/ocas-spot/opentable-session.json`
- This file is in `.gitignore` — do not commit it.

---

## Rejected Methods

| Method | Result |
|--------|--------|
| Direct HTTP requests | Akamai 403 / HTTP2 protocol error |
| Headless browser (no session) | Akamai CAPTCHA/block |
| Mobile viewport / user-agent spoofing | TLS fingerprint still detected |
| Stealth scripts alone | Insufficient without prior human session |
| Disabling HTTP/2 | Chrome ignores flag; still fails |