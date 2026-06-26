#!/usr/bin/env python3
"""Gerenciamento de sessão para o Google Keep.

Login: Chrome puro (sem automação) para interação normal do usuário.
Operações: nodriver (headless) reutilizando o perfil/cookies.
"""

import asyncio
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import nodriver as uc

CONFIG_DIR = Path.home() / ".config" / "google-keep-skill"
PROFILE_DIR = CONFIG_DIR / "chrome-profile"
COOKIES_FILE = CONFIG_DIR / "cookies.json"
KEEP_URL = "https://keep.google.com/"


def _find_chrome() -> str:
    """Locates the Chrome executable in the system."""
    candidates = [
        "google-chrome",
        "google-chrome-stable",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
    ]
    for c in candidates:
        result = shutil.which(c)
        if result:
            return result
    raise FileNotFoundError("Google Chrome not found. Install it with: sudo apt install google-chrome-stable")


def interactive_login() -> bool:
    """Opens pure Chrome (no automation) for manual login.

    The user acts organically.
    Upon closing Chrome, the profile and cookies are automatically saved to `~/.config/google-keep-skill/`.
    """
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(CONFIG_DIR, 0o700)
    chrome = _find_chrome()

    print("=" * 60, flush=True)
    print("  GOOGLE KEEP LOGIN", flush=True)
    print("=" * 60, flush=True)
    print(flush=True)
    print("Chrome will open natively (without automation).", flush=True)
    print("1. Log in to your Google account", flush=True)
    print("2. Wait for Google Keep to load", flush=True)
    print("3. CLOSE the browser (click the X)", flush=True)
    print(flush=True)
    print(f"The session will be saved to {CONFIG_DIR} upon closing.", flush=True)
    print(flush=True)

    cmd = [
        chrome,
        f"--user-data-dir={PROFILE_DIR}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-default-apps",
        "--new-window",
        KEEP_URL,
    ]

    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Chrome opened. Waiting for you to close the browser...", flush=True)
        proc.wait()
        print("Chrome closed.", flush=True)
        print(flush=True)

        # After closing, extract cookies from the profile via nodriver (fast headless)
        print("Extracting session cookies...", flush=True)
        ok = uc.loop().run_until_complete(_extract_and_save_cookies())
        if ok:
            print("Session saved successfully!", flush=True)
        else:
            print("Warning: could not verify the session.", flush=True)
            print("Run the 'check' command to confirm.", flush=True)
        return ok

    except FileNotFoundError:
        print(f"Error: Chrome not found at {chrome}", flush=True)
        return False
    except Exception as e:
        print(f"Error: {e}", flush=True)
        return False


async def _extract_and_save_cookies() -> bool:
    """Opens headless with the profile, navigates to Keep and saves CDP cookies."""
    browser = await _start_nodriver(headless=True)
    tab = browser.main_tab

    await tab.get(KEEP_URL)
    await asyncio.sleep(4)

    url = tab.target.url
    if "accounts.google" in url:
        browser.stop()
        return False

    await _save_cookies_cdp(tab)
    browser.stop()
    return True


async def _start_nodriver(*, headless: bool = True, use_temp_profile: bool = False) -> uc.Browser:
    """Starts nodriver. Uses a temporary profile if use_temp_profile=True."""
    kwargs = {
        "headless": headless,
        "browser_args": [
            "--no-first-run",
            "--no-default-browser-check",
            "--lang=pt-BR",
            "--window-size=1920,1080",
            "--disable-session-crashed-bubble",
            "--disable-infobars",
        ],
    }
    if not use_temp_profile:
        PROFILE_DIR.mkdir(parents=True, exist_ok=True)
        kwargs["user_data_dir"] = str(PROFILE_DIR)
    browser = await uc.start(**kwargs)
    return browser


async def _save_cookies_cdp(tab) -> None:
    """Saves cookies via CDP to a JSON file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    cookies = await tab.send(uc.cdp.network.get_all_cookies())
    cookie_list = []
    for c in cookies:
        cookie_list.append({
            "name": c.name,
            "value": c.value,
            "domain": c.domain,
            "path": c.path,
            "secure": c.secure,
            "httpOnly": c.http_only,
            "sameSite": c.same_site.value if c.same_site else "None",
        })
    with open(COOKIES_FILE, "w") as f:
        json.dump(cookie_list, f)
    COOKIES_FILE.chmod(0o600)
    print(f"  {len(cookie_list)} cookies saved.", flush=True)


async def _restore_cookies_cdp(tab) -> bool:
    """Restores cookies saved via CDP."""
    if not COOKIES_FILE.exists():
        return False
    try:
        with open(COOKIES_FILE, "r") as f:
            cookie_list = json.load(f)

        for c in cookie_list:
            same_site = None
            raw = c.get("sameSite", "None")
            if raw == "Strict":
                same_site = uc.cdp.network.CookieSameSite("Strict")
            elif raw == "Lax":
                same_site = uc.cdp.network.CookieSameSite("Lax")
            elif raw == "None":
                same_site = uc.cdp.network.CookieSameSite("None")

            await tab.send(uc.cdp.network.set_cookie(
                name=c["name"],
                value=c["value"],
                domain=c.get("domain", ""),
                path=c.get("path", "/"),
                secure=c.get("secure", False),
                http_only=c.get("httpOnly", False),
                same_site=same_site,
            ))
        return True
    except Exception:
        return False


async def open_keep_session(*, headless: bool = True):
    """Opens Keep with restored session (persistent profile + CDP cookies)."""
    browser = await _start_nodriver(headless=headless)
    tab = browser.main_tab

    await _restore_cookies_cdp(tab)

    try:
        await tab.send(uc.cdp.storage.clear_data_for_origin(
            origin="https://keep.google.com",
            storage_types="indexeddb,cache_storage,local_storage",
        ))
    except Exception:
        pass

    await tab.get(KEEP_URL)
    await asyncio.sleep(5)

    url = tab.target.url
    if "accounts.google" in url:
        browser.stop()
        return None, None

    return browser, tab


async def check_session_async() -> bool:
    """Checks if the session is active."""
    browser, tab = await open_keep_session(headless=True)
    if not browser:
        return False
    browser.stop()
    return True


def clear_session() -> bool:
    """Removes the profile and cookies completely."""
    if PROFILE_DIR.exists():
        shutil.rmtree(PROFILE_DIR, ignore_errors=True)
    if COOKIES_FILE.exists():
        COOKIES_FILE.unlink()
    print("Session cleared.", flush=True)
    return True


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "login"

    if cmd == "login":
        ok = interactive_login()
        sys.exit(0 if ok else 1)
    elif cmd == "check":
        ok = uc.loop().run_until_complete(check_session_async())
        print(f"Session active: {ok}", flush=True)
        sys.exit(0 if ok else 1)
    elif cmd == "clear":
        clear_session()
    else:
        print("Usage: auth.py [login|check|clear]", flush=True)
