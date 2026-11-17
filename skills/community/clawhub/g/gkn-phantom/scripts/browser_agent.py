#!/usr/bin/env python3
"""Interactive Browser Agent for the GKN-Phantom Penetration Testing Skill.

Handles complex authentication flows that cannot be automated with plain
HTTP requests: multi-step login forms, JavaScript-heavy auth, captcha
challenges, MFA/2FA prompts, and CSRF/JWT token extraction.

Integrates with Playwright (Chromium) when available; gracefully falls back
to curl-based simulation with guidance for manual intervention otherwise.

Capabilities:
  - Playwright Integration — auto-detect, launch headless Chromium,
    --install flag for automated setup, fallback when unavailable.
  - Multi-Step Authentication — JSON-defined auth workflows executed
    step-by-step with cookie/token capture at completion.
  - Captcha Handling — bypass detection, manual intervention with
    screenshot, OCR attempt via pytesseract (experimental).
  - MFA/2FA Flow — detect TOTP/SMS/email code prompts, save state,
    prompt user, resume session.
  - Session Persistence — export cookies as JSON, curl cookie jar,
    Python requests session pickle, localStorage/sessionStorage dump.
  - JavaScript Execution — extract CSRF tokens, JWT tokens, trigger
    XHR requests, detect frontend framework state objects.
  - Screenshot Capture — audit trail at each auth step.
  - Proxy Support — route through Burp Suite or custom proxy.

Usage:
  python browser_agent.py --url https://target.com/login --auth-steps steps.json [--output session.json] [--screenshots-dir ./screenshots]
  python browser_agent.py --install   # Install Playwright + Chromium
  python browser_agent.py --check     # Check if Playwright is available
"""

from __future__ import annotations

import argparse
import base64
import http.cookiejar as cookiejar_mod
import json
import os
import pickle
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json, utc_now_iso


# ---------------------------------------------------------------------------
# Playwright detection & setup
# ---------------------------------------------------------------------------

def _find_playwright() -> Optional[str]:
    """Return the path to the playwright CLI if installed, else None."""
    pw_path = shutil.which("playwright")
    return pw_path


def _check_playwright_available() -> dict:
    """Return a status dict describing Playwright availability.

    Keys: available (bool), playwright_path (str|None), browsers (list),
          python_module (bool), message (str).
    """
    result: dict[str, Any] = {
        "available": False,
        "playwright_path": None,
        "browsers": [],
        "python_module": False,
        "message": "",
    }
    # Check Python module
    try:
        import importlib
        importlib.import_module("playwright")
        result["python_module"] = True
    except ImportError:
        result["message"] = "playwright Python module not installed. Run: pip install playwright"
        return result

    # Check CLI
    pw_path = _find_playwright()
    if pw_path:
        result["playwright_path"] = pw_path
    else:
        result["message"] = "playwright CLI not found. Run: playwright install chromium"
        return result

    # Check installed browsers
    try:
        proc = subprocess.run(
            [pw_path, "install", "--dry-run", "chromium"],
            capture_output=True, text=True, timeout=30,
        )
        # If dry-run says already installed, stdout typically contains "chromium"
        if "chromium" in proc.stdout.lower() or proc.returncode == 0:
            result["browsers"].append("chromium")
            result["available"] = True
            result["message"] = "Playwright + Chromium ready."
        else:
            result["message"] = "Chromium not installed. Run: playwright install chromium"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        result["message"] = "Could not verify Chromium installation."

    return result


def install_playwright() -> int:
    """Install playwright Python module and Chromium browser. Returns exit code."""
    print("[*] Installing playwright Python module...")
    ret = subprocess.run(
        [sys.executable, "-m", "pip", "install", "playwright"],
        capture_output=False,
    ).returncode
    if ret != 0:
        print("[!] Failed to install playwright. Try: pip install playwright")
        return ret

    print("[*] Installing Chromium browser...")
    pw_path = _find_playwright()
    if not pw_path:
        print("[!] playwright CLI not found after pip install. Check PATH.")
        return 1

    ret = subprocess.run([pw_path, "install", "chromium"], capture_output=False).returncode
    if ret == 0:
        print("[+] Playwright + Chromium installed successfully.")
    else:
        print("[!] Chromium installation failed.")
    return ret


# ---------------------------------------------------------------------------
# Playwright session wrapper
# ---------------------------------------------------------------------------

class BrowserSession:
    """Wraps a Playwright browser context for an interactive auth session.

    Manages page lifecycle, screenshot capture, cookie/storage extraction,
    and JS execution within the page context.
    """

    def __init__(
        self,
        headless: bool = True,
        proxy: Optional[dict] = None,
        screenshots_dir: Optional[str] = None,
        timeout: int = 30000,
    ):
        self._headless = headless
        self._proxy = proxy  # {"server": "http://127.0.0.1:8080"}
        self._screenshots_dir = screenshots_dir
        self._timeout = timeout
        self._browser = None
        self._context = None
        self._page = None
        self._playwright = None
        self._step_index = 0
        self._screenshots: list[str] = []

    def _ensure_dir(self, path: str) -> None:
        if path:
            os.makedirs(path, exist_ok=True)

    def start(self) -> None:
        """Launch browser and create a fresh context."""
        import importlib
        try:
            self._playwright = importlib.import_module("playwright")
        except ImportError:
            raise RuntimeError(
                "Playwright not installed. Run: pip install playwright && "
                "playwright install chromium"
            )

        pw = self._playwright
        self._browser = pw.chromium.launch(
            headless=self._headless,
        )
        context_opts: dict[str, Any] = {}
        if self._proxy:
            context_opts["proxy"] = self._proxy
        self._context = self._browser.new_context(**context_opts)
        self._page = self._context.new_page()
        self._page.set_default_timeout(self._timeout)
        if self._screenshots_dir:
            self._ensure_dir(self._screenshots_dir)

    def stop(self) -> None:
        """Close browser and clean up."""
        if self._context:
            try:
                self._context.close()
            except Exception:
                pass
            self._context = None
        if self._browser:
            try:
                self._browser.close()
            except Exception:
                pass
            self._browser = None
        self._page = None

    def navigate(self, url: str) -> None:
        """Navigate to a URL and wait for network idle."""
        if not self._page:
            raise RuntimeError("Browser session not started.")
        self._page.goto(url, wait_until="networkidle")

    def fill(self, selector: str, value: str) -> None:
        """Fill an input field identified by CSS selector."""
        if not self._page:
            raise RuntimeError("Browser session not started.")
        self._page.fill(selector, value)

    def click(self, selector: str) -> None:
        """Click an element identified by CSS selector."""
        if not self._page:
            raise RuntimeError("Browser session not started.")
        self._page.click(selector)

    def wait_for_url(self, pattern: str, timeout: Optional[int] = None) -> bool:
        """Wait until the page URL matches a regex pattern."""
        if not self._page:
            raise RuntimeError("Browser session not started.")
        t = timeout or self._timeout
        try:
            self._page.wait_for_url(re.compile(pattern), timeout=t)
            return True
        except Exception:
            return False

    def wait_for_selector(self, selector: str, timeout: Optional[int] = None) -> bool:
        """Wait for an element to appear on the page."""
        if not self._page:
            raise RuntimeError("Browser session not started.")
        t = timeout or self._timeout
        try:
            self._page.wait_for_selector(selector, timeout=t)
            return True
        except Exception:
            return False

    def wait_for_navigation(self, timeout: Optional[int] = None) -> None:
        """Wait for page navigation to complete."""
        if not self._page:
            raise RuntimeError("Browser session not started.")
        self._page.wait_for_load_state("networkidle", timeout=timeout or self._timeout)

    def screenshot(self, label: str = "") -> str:
        """Take a screenshot. Returns the file path."""
        if not self._page or not self._screenshots_dir:
            return ""
        self._step_index += 1
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        fname = f"step{self._step_index:03d}_{label}_{ts}.png" if label else f"step{self._step_index:03d}_{ts}.png"
        fpath = os.path.join(self._screenshots_dir, fname)
        self._page.screenshot(path=fpath, full_page=True)
        self._screenshots.append(fpath)
        return fpath

    def get_cookies(self) -> list[dict]:
        """Return all cookies for the current context as a list of dicts."""
        if not self._context:
            return []
        return self._context.cookies()

    def execute_js(self, script: str) -> Any:
        """Execute JavaScript in the page context and return the result."""
        if not self._page:
            raise RuntimeError("Browser session not started.")
        return self._page.evaluate(script)

    def get_storage(self) -> dict:
        """Return localStorage and sessionStorage contents."""
        if not self._page:
            return {"localStorage": {}, "sessionStorage": {}}
        return {
            "localStorage": self._page.evaluate("() => JSON.parse(JSON.stringify(window.localStorage))"),
            "sessionStorage": self._page.evaluate("() => JSON.parse(JSON.stringify(window.sessionStorage))"),
        }

    def get_page_content(self) -> str:
        """Return the full HTML content of the current page."""
        if not self._page:
            return ""
        return self._page.content()

    def get_current_url(self) -> str:
        """Return the current page URL."""
        if not self._page:
            return ""
        return self._page.url

    def detect_mfa_prompt(self) -> Optional[str]:
        """Heuristically detect MFA/2FA prompts on the current page.

        Returns one of: 'totp', 'sms', 'email', 'push', None.
        """
        if not self._page:
            return None
        content = self._page.content().lower()

        # Common MFA patterns in DOM text
        totp_patterns = [
            "authenticator", "totp", "one-time code", "6-digit", "6 digit",
            "verification code", "auth code", "2fa code", "two-factor",
            "google authenticator", "microsoft authenticator", "authy",
        ]
        sms_patterns = [
            "sms", "text message", "phone number", "mobile code",
            "sent a code to your phone", "texted",
        ]
        email_patterns = [
            "email code", "emailed", "check your email", "email sent",
            "code to your email",
        ]
        push_patterns = [
            "push notification", "approve sign-in", "tap yes",
            "duo push", "duo security",
        ]

        for p in totp_patterns:
            if p in content:
                return "totp"
        for p in sms_patterns:
            if p in content:
                return "sms"
        for p in email_patterns:
            if p in content:
                return "email"
        for p in push_patterns:
            if p in content:
                return "push"
        return None


# ---------------------------------------------------------------------------
# Captcha handling strategies
# ---------------------------------------------------------------------------

def detect_captcha(page_content: str) -> Optional[str]:
    """Heuristically detect captcha presence on a page.

    Returns captcha type: 'recaptcha_v2', 'recaptcha_v3', 'hcaptcha',
    'image_captcha', 'math_captcha', 'cloudflare', or None.
    """
    html_lower = page_content.lower()
    if "g-recaptcha" in html_lower or "recaptcha" in html_lower or "grecaptcha" in html_lower:
        if "recaptcha/api2" in html_lower or "g-recaptcha-response" in html_lower:
            return "recaptcha_v2"
        if "recaptcha/api.js" in html_lower and "score" in html_lower:
            return "recaptcha_v3"
        return "recaptcha_v2"
    if "h-captcha" in html_lower or "hcaptcha" in html_lower:
        return "hcaptcha"
    if "captcha" in html_lower and ('<img' in html_lower and ('src="' in html_lower or "src='" in html_lower)):
        # Look for image captcha patterns
        img_match = re.search(r'<img[^>]+src=["\']([^"\']*captcha[^"\']*)["\']', page_content, re.IGNORECASE)
        if img_match:
            return "image_captcha"
    if "cf-turnstile" in html_lower or "cloudflare" in html_lower:
        return "cloudflare"
    if re.search(r'\d+\s*[\+\-\*]\s*\d+\s*=', html_lower) and "captcha" in html_lower:
        return "math_captcha"
    return None


def attempt_captcha_bypass(
    url: str, method: str, params: dict, data: dict, headers: dict
) -> dict:
    """Try common captcha bypass techniques against vuln_detector captcha_bypass rules.

    Returns {"bypassed": True/False, "technique": str, "notes": str}.
    """
    # Strategy 1: Omit the captcha parameter entirely
    # Strategy 2: Send empty captcha value
    # Strategy 3: Send well-known test/bypass tokens
    bypass_techniques = [
        ("omit_param", "Remove captcha parameter from request"),
        ("empty_value", "Send empty string as captcha value"),
        ("null_value", "Send null/None as captcha value"),
        ("test_token", "Use common test tokens (e.g. 'test', 'bypass', '1234')"),
    ]
    return {
        "bypassed": False,
        "technique": "not_attempted",
        "notes": (
            "Captcha bypass requires live interaction. Available strategies: "
            + ", ".join(f"{t[0]}={t[1]}" for t in bypass_techniques)
            + ". Run with --interactive for manual captcha resolution."
        ),
    }


def attempt_captcha_ocr(image_path: str) -> Optional[str]:
    """Attempt OCR on a captcha image using pytesseract if available.

    Returns the recognized text or None. This is experimental and low-reliability.
    """
    try:
        import importlib
        importlib.import_module("pytesseract")
    except ImportError:
        return None

    try:
        import pytesseract
        from PIL import Image
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
        return text.strip()
    except Exception as e:
        print(f"[!] OCR attempt failed: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Auth workflow executor
# ---------------------------------------------------------------------------

def _substitute_vars(value: str, variables: dict) -> str:
    """Replace {{var}} placeholders in a string with values from variables dict."""
    def _replacer(m: re.Match) -> str:
        key = m.group(1)
        return str(variables.get(key, m.group(0)))
    return re.sub(r"\{\{(\w+)\}\}", _replacer, value)


def execute_auth_workflow(
    session: BrowserSession,
    steps: list[dict],
    variables: Optional[dict] = None,
    interactive: bool = False,
) -> dict:
    """Execute a multi-step authentication workflow.

    Args:
        session: An already-started BrowserSession.
        steps: List of action dicts (navigate, fill, click, wait_for_url,
               wait_for_selector, wait, execute_js, extract_cookies,
               extract_storage, screenshot, mfa_check, input).
        variables: Dict of substitution values for {{var}} in step values.
        interactive: If True, prompt user for MFA codes and captcha input.

    Returns:
        Dict with keys: success (bool), cookies (list), storage (dict),
        screenshots (list), extracted_tokens (dict), errors (list),
        mfa_detected (bool), captcha_detected (str|None).
    """
    vars_dict = variables or {}
    result: dict[str, Any] = {
        "success": False,
        "cookies": [],
        "storage": {},
        "screenshots": [],
        "extracted_tokens": {},
        "errors": [],
        "mfa_detected": False,
        "captcha_detected": None,
    }

    for i, step in enumerate(steps):
        action = step.get("action", "")
        try:
            if action == "navigate":
                url = _substitute_vars(step.get("url", ""), vars_dict)
                session.navigate(url)
                print(f"  [navigate] {url}")

            elif action == "fill":
                selector = _substitute_vars(step.get("selector", ""), vars_dict)
                value = _substitute_vars(step.get("value", ""), vars_dict)
                session.fill(selector, value)
                print(f"  [fill] {selector} = ***")

            elif action == "click":
                selector = _substitute_vars(step.get("selector", ""), vars_dict)
                session.click(selector)
                print(f"  [click] {selector}")

            elif action == "wait_for_url":
                pattern = step.get("pattern", "")
                timeout_val = step.get("timeout")
                ok = session.wait_for_url(pattern, timeout=timeout_val)
                if not ok:
                    result["errors"].append(f"Step {i}: wait_for_url '{pattern}' timed out")
                print(f"  [wait_for_url] {pattern} -> {'OK' if ok else 'TIMEOUT'}")

            elif action == "wait_for_selector":
                selector = _substitute_vars(step.get("selector", ""), vars_dict)
                timeout_val = step.get("timeout")
                ok = session.wait_for_selector(selector, timeout=timeout_val)
                if not ok:
                    result["errors"].append(f"Step {i}: wait_for_selector '{selector}' timed out")
                print(f"  [wait_for_selector] {selector} -> {'OK' if ok else 'TIMEOUT'}")

            elif action == "wait":
                duration = float(step.get("seconds", 1))
                time.sleep(duration)
                print(f"  [wait] {duration}s")

            elif action == "execute_js":
                script = step.get("script", "")
                js_result = session.execute_js(script)
                store_key = step.get("store_as")
                if store_key:
                    result["extracted_tokens"][store_key] = js_result
                print(f"  [execute_js] -> {store_key or 'discarded'}")

            elif action == "extract_cookies":
                result["cookies"] = session.get_cookies()
                print(f"  [extract_cookies] {len(result['cookies'])} cookies captured")

            elif action == "extract_storage":
                result["storage"] = session.get_storage()
                print(f"  [extract_storage] localStorage + sessionStorage captured")

            elif action == "screenshot":
                label = step.get("label", f"step{i}")
                fpath = session.screenshot(label=label)
                if fpath:
                    result["screenshots"].append(fpath)
                    print(f"  [screenshot] {fpath}")

            elif action == "mfa_check":
                mfa_type = session.detect_mfa_prompt()
                if mfa_type:
                    result["mfa_detected"] = True
                    print(f"  [mfa_check] MFA prompt detected: {mfa_type}")
                    if interactive:
                        code = input(f"  [?] Enter {mfa_type} code: ").strip()
                        # Find the next fill step or attempt common MFA field selectors
                        mfa_field = step.get("mfa_field", "")
                        if mfa_field:
                            session.fill(mfa_field, code)
                        else:
                            # Try common MFA input selectors
                            for sel in [
                                "input[id*='totp']", "input[id*='mfa']",
                                "input[id*='2fa']", "input[id*='code']",
                                "input[name*='code']", "input[name*='otp']",
                                "input[name*='token']", "input[type='number']",
                            ]:
                                if session.wait_for_selector(sel, timeout=1000):
                                    session.fill(sel, code)
                                    break
                        if step.get("submit_selector"):
                            session.click(_substitute_vars(step["submit_selector"], vars_dict))
                            session.wait_for_navigation()
                else:
                    print(f"  [mfa_check] No MFA prompt detected")

            elif action == "input":
                # Generic user input prompt
                prompt_text = step.get("prompt", "Enter value:")
                var_name = step.get("store_as", "user_input")
                user_val = input(f"  [?] {prompt_text} ").strip()
                vars_dict[var_name] = user_val

            elif action == "check_captcha":
                content = session.get_page_content()
                captcha_type = detect_captcha(content)
                if captcha_type:
                    result["captcha_detected"] = captcha_type
                    print(f"  [check_captcha] Captcha detected: {captcha_type}")
                    if interactive:
                        print(f"  [!] {captcha_type} detected. Please solve it manually in the browser.")
                        if session._screenshots_dir:
                            fpath = session.screenshot(label=f"captcha_{captcha_type}")
                            if fpath:
                                print(f"  [screenshot] Captcha screenshot saved: {fpath}")
                        input("  [?] Press Enter after solving the captcha...")
                else:
                    print(f"  [check_captcha] No captcha detected")

            else:
                result["errors"].append(f"Step {i}: unknown action '{action}'")
                print(f"  [!] Unknown action: {action}")

        except Exception as e:
            result["errors"].append(f"Step {i} ({action}): {e}")
            print(f"  [ERROR] Step {i} ({action}): {e}", file=sys.stderr)
            if step.get("critical", False):
                break

    # Final state capture
    if result["errors"]:
        result["success"] = False
    else:
        result["success"] = True
        # Ensure cookies are captured if not explicitly done
        if not result["cookies"]:
            result["cookies"] = session.get_cookies()
        if not result["storage"]:
            result["storage"] = session.get_storage()
        # Also capture CSRF/JWT tokens via JS
        try:
            tokens_js = session.execute_js("""
                (() => {
                    const tokens = {};
                    // CSRF
                    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
                    if (csrfMeta) tokens.csrf_token = csrfMeta.content;
                    const csrfInput = document.querySelector('input[name="_csrf"], input[name="csrf_token"], input[name="csrfmiddlewaretoken"]');
                    if (csrfInput) tokens.csrf_token = csrfInput.value;
                    // JWT
                    try { tokens.jwt = localStorage.getItem('token') || localStorage.getItem('jwt') || localStorage.getItem('access_token'); } catch(e) {}
                    if (!tokens.jwt) try { tokens.jwt = sessionStorage.getItem('token') || sessionStorage.getItem('jwt'); } catch(e) {}
                    // Bearer token from common patterns
                    try {
                        const authData = localStorage.getItem('auth') || localStorage.getItem('persist:root');
                        if (authData) {
                            try { const parsed = JSON.parse(authData); if (parsed.token) tokens.jwt = parsed.token; } catch(e) {}
                        }
                    } catch(e) {}
                    return tokens;
                })()
            """)
            if tokens_js:
                result["extracted_tokens"].update(tokens_js)
                print(f"  [auto-extract] Tokens: {list(tokens_js.keys())}")
        except Exception:
            pass

    return result


# ---------------------------------------------------------------------------
# Session persistence / export
# ---------------------------------------------------------------------------

def _cookies_to_netscape(cookies: list[dict]) -> str:
    """Convert cookie dicts to Netscape/Mozilla cookie jar format (curl-compatible)."""
    lines = ["# Netscape HTTP Cookie File", "# Generated by GKN-Phantom browser_agent.py", ""]
    for c in cookies:
        domain = c.get("domain", "")
        flag = "TRUE" if domain.startswith(".") else "FALSE"
        path = c.get("path", "/")
        secure = "TRUE" if c.get("secure", False) else "FALSE"
        expires = str(int(c.get("expires", -1))) if c.get("expires", -1) and c.get("expires", -1) > 0 else "0"
        name = c.get("name", "")
        value = c.get("value", "")
        lines.append(f"{domain}\t{flag}\t{path}\t{secure}\t{expires}\t{name}\t{value}")
    return "\n".join(lines) + "\n"


def _cookies_to_curl_header(cookies: list[dict]) -> str:
    """Convert cookies to a curl-compatible Cookie: header value."""
    pairs = [f"{c.get('name', '')}={c.get('value', '')}" for c in cookies if c.get("name")]
    return "; ".join(pairs)


def _cookies_to_python_cookiejar(cookies: list[dict]) -> http.cookiejar.CookieJar:
    """Convert cookie dicts to a Python http.cookiejar.CookieJar for use with requests."""
    jar = cookiejar_mod.CookieJar()
    for c in cookies:
        cookie = cookiejar_mod.Cookie(
            version=0,
            name=c.get("name", ""),
            value=c.get("value", ""),
            port=None,
            port_specified=False,
            domain=c.get("domain", ""),
            domain_specified=bool(c.get("domain")),
            domain_initial_dot=c.get("domain", "").startswith("."),
            path=c.get("path", "/"),
            path_specified=bool(c.get("path")),
            secure=bool(c.get("secure", False)),
            expires=int(c.get("expires", -1)) if c and c.get("expires", -1) and c.get("expires", -1) > 0 else None,
            discard=False,
            comment=None,
            comment_url=None,
            rest={"HttpOnly": c.get("httpOnly", False)},
            rfc2109=False,
        )
        jar.set_cookie(cookie)
    return jar


def save_session(
    session_result: dict,
    output_path: str,
    formats: Optional[list[str]] = None,
) -> dict:
    """Persist session data to disk in multiple formats.

    Args:
        session_result: The dict returned by execute_auth_workflow.
        output_path: Base path for output files (without extension).
        formats: List of formats: json, netscape, curl_header, pickle, all.
                 Default: all.

    Returns:
        Dict mapping format to output file path.
    """
    fmts = formats or ["all"]
    if "all" in fmts:
        fmts = ["json", "netscape", "curl_header", "pickle"]

    cookies = session_result.get("cookies", [])
    storage = session_result.get("storage", {})
    tokens = session_result.get("extracted_tokens", {})
    outputs: dict[str, str] = {}
    base = output_path

    if "json" in fmts:
        fpath = f"{base}.json"
        payload = {
            "cookies": cookies,
            "storage": storage,
            "tokens": tokens,
            "exported_at": utc_now_iso(),
        }
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        outputs["json"] = fpath
        print(f"  [+] Session JSON: {fpath}")

    if "netscape" in fmts:
        fpath = f"{base}_cookies.txt"
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(_cookies_to_netscape(cookies))
        outputs["netscape"] = fpath
        print(f"  [+] Netscape cookie jar: {fpath}")

    if "curl_header" in fmts:
        fpath = f"{base}_cookie_header.txt"
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(_cookies_to_curl_header(cookies))
        outputs["curl_header"] = fpath
        print(f"  [+] Curl Cookie header: {fpath}")

    if "pickle" in fmts:
        fpath = f"{base}_session.pkl"
        jar = _cookies_to_python_cookiejar(cookies)
        sess_data = {
            "cookiejar": jar,
            "storage": storage,
            "tokens": tokens,
        }
        with open(fpath, "wb") as f:
            pickle.dump(sess_data, f)
        outputs["pickle"] = fpath
        print(f"  [+] Pickled session: {fpath}")

    return outputs


# ---------------------------------------------------------------------------
# Curl-based fallback simulation
# ---------------------------------------------------------------------------

def _curl_fallback_guide(url: str, steps: list[dict], variables: dict) -> str:
    """Generate a manual curl-based walkthrough when Playwright is unavailable."""
    lines = [
        "# ================================================================",
        "# GKN-Phantom Browser Agent — Curl Fallback Guide",
        "# Playwright is not available. Use the curl commands below to",
        "# manually replicate the auth workflow and capture cookies.",
        "# ================================================================",
        "",
        f"# Target: {url}",
        f"# Steps: {len(steps)}",
        "",
    ]
    vars_dict = variables or {}
    for i, step in enumerate(steps):
        action = step.get("action", "")
        lines.append(f"# --- Step {i+1}: {action} ---")
        if action == "navigate":
            step_url = _substitute_vars(step.get("url", ""), vars_dict)
            lines.append(f"curl -c cookies.txt -b cookies.txt -L '{step_url}'")
        elif action == "fill":
            # Cannot fill with curl; suggest the user does it manually or use data
            selector = step.get("selector", "")
            lines.append(f"# (Manual) Fill field '{selector}' in the login form")
            lines.append(f"# Use curl -d '{selector}=VALUE' if the endpoint supports direct POST")
        elif action == "click":
            selector = step.get("selector", "")
            lines.append(f"# (Manual) Click '{selector}'")
        elif action == "wait_for_url":
            lines.append(f"# Wait until URL matches: {step.get('pattern', '')}")
        elif action == "extract_cookies":
            lines.append("# Capture cookies from cookies.txt")
        elif action == "extract_storage":
            lines.append("# (Manual) Extract localStorage/sessionStorage from browser DevTools")
        elif action == "screenshot":
            lines.append("# (Manual) Take a screenshot")
        else:
            lines.append(f"# {json.dumps(step)}")
        lines.append("")

    lines.append("# After completing all steps, save cookies with:")
    lines.append("# curl -c final_cookies.txt -b cookies.txt 'https://target.com/'")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="GKN-Phantom Interactive Browser Agent — automated auth flow handler",
    )
    p.add_argument("--url", help="Target URL for the auth flow start page")
    p.add_argument("--auth-steps", help="JSON file with auth workflow steps")
    p.add_argument("--output", default="session", help="Base path for session output files")
    p.add_argument("--screenshots-dir", default="./screenshots", help="Directory for screenshots")
    p.add_argument("--variables", help="JSON file with {{var}} substitution values")
    p.add_argument("--proxy", help="Proxy server (e.g. http://127.0.0.1:8080)")
    p.add_argument("--timeout", type=int, default=30000, help="Default timeout in ms (default: 30000)")
    p.add_argument("--headless", action=argparse.BooleanOptionalAction, default=True, help="Run headless (default: True)")
    p.add_argument("--interactive", "-i", action="store_true", help="Prompt user for MFA/captcha input")
    p.add_argument("--format", default="all", help="Output formats: json,netscape,curl_header,pickle,all")
    p.add_argument("--install", action="store_true", help="Install Playwright + Chromium and exit")
    p.add_argument("--check", action="store_true", help="Check Playwright availability and exit")
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # --install
    if args.install:
        return install_playwright()

    # --check
    if args.check:
        status = _check_playwright_available()
        print(json.dumps(status, indent=2))
        return 0 if status["available"] else 1

    # Validate required args for auth flow
    if not args.url:
        parser.error("--url is required for auth workflow execution")
    if not args.auth_steps:
        parser.error("--auth-steps is required for auth workflow execution")

    # Load steps
    steps = load_json(args.auth_steps)
    if isinstance(steps, dict):
        # Support {"steps": [...]} wrapper or bare array
        if "steps" in steps:
            steps = steps["steps"]
            variables_file = args.variables or steps.get("variables_file", "")
            if variables_file and not args.variables:
                try:
                    vars_loaded = load_json(variables_file)
                    args.variables = variables_file  # will load below
                except Exception:
                    pass
        else:
            steps = [steps]
    if not isinstance(steps, list):
        print("[!] Auth steps must be a JSON array or {\"steps\": [...]}", file=sys.stderr)
        return 1

    # Load variables
    variables: dict = {}
    if args.variables:
        try:
            variables = load_json(args.variables)
        except Exception:
            pass

    # Check Playwright
    pw_status = _check_playwright_available()
    if not pw_status["available"]:
        print("[!] Playwright not available. Generating curl fallback guide...")
        guide = _curl_fallback_guide(args.url, steps, variables)
        fallback_path = f"{args.output}_curl_guide.sh"
        with open(fallback_path, "w", encoding="utf-8") as f:
            f.write(guide)
        print(f"[+] Curl fallback guide written to: {fallback_path}")
        print("[*] Install Playwright for full automation: python browser_agent.py --install")
        # Still output the guide path
        result = {
            "success": False,
            "mode": "curl_fallback",
            "guide_path": fallback_path,
            "note": "Playwright not installed. Use --install flag to set up.",
        }
        with open(f"{args.output}_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        return 1

    # Proxy config
    proxy_config = None
    if args.proxy:
        proxy_config = {"server": args.proxy}

    # Run the browser session
    session = BrowserSession(
        headless=args.headless,
        proxy=proxy_config,
        screenshots_dir=args.screenshots_dir,
        timeout=args.timeout,
    )

    print(f"[*] Starting browser session for {args.url}")
    try:
        session.start()
    except Exception as e:
        print(f"[!] Failed to start browser: {e}", file=sys.stderr)
        return 1

    try:
        result = execute_auth_workflow(
            session, steps, variables=variables,
            interactive=args.interactive,
        )
    finally:
        session.stop()

    # Save session
    formats = [f.strip() for f in args.format.split(",")] if args.format != "all" else None
    outputs = save_session(result, args.output, formats=formats)

    # Write consolidated result
    result["output_files"] = outputs
    result["exported_at"] = utc_now_iso()
    with open(f"{args.output}_result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    if result["success"]:
        print(f"\n[+] Auth workflow completed successfully.")
    else:
        print(f"\n[!] Auth workflow completed with {len(result.get('errors', []))} error(s).")
        for err in result.get("errors", []):
            print(f"    - {err}")

    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
