"""
Shared NCCUOJ session utility.
Handles CSRF token acquisition and cookie persistence.

Usage (from other scripts):
    from session import get_session
    session = get_session()
"""

import http.cookiejar
import json
import os
import urllib.request
import urllib.parse
import ssl

BASE_URL = os.environ.get("NCCUOJ_BASE_URL", "https://nccuoj.ebg.tw")
API_URL = f"{BASE_URL}/api"

# .nccuoj directory at workspace root for cookies and data
_NCCUOJ_DIR = os.path.join(os.getcwd(), ".nccuoj")
_COOKIE_FILE = os.path.join(_NCCUOJ_DIR, "cookies.txt")

# Allow overriding for self-signed certs in dev
_ssl_ctx = ssl.create_default_context()


_USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def _ensure_nccuoj_dir():
    """Ensure .nccuoj directory exists."""
    os.makedirs(_NCCUOJ_DIR, exist_ok=True)


def _build_opener():
    _ensure_nccuoj_dir()
    cookie_jar = http.cookiejar.MozillaCookieJar(_COOKIE_FILE)
    if os.path.exists(_COOKIE_FILE):
        cookie_jar.load(ignore_discard=True, ignore_expires=True)
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookie_jar),
        urllib.request.HTTPSHandler(context=_ssl_ctx),
    )
    opener.addheaders = [("User-Agent", _USER_AGENT)]
    return opener, cookie_jar


def _get_csrf_token(cookie_jar):
    for cookie in cookie_jar:
        if cookie.name == "csrftoken":
            return cookie.value
    return None


def get_session():
    """Create a session with CSRF token pre-fetched via GET /api/profile."""
    opener, cookie_jar = _build_opener()
    # Hit profile to get csrftoken cookie
    req = urllib.request.Request(f"{API_URL}/profile", method="GET")
    opener.open(req)
    cookie_jar.save(ignore_discard=True, ignore_expires=True)
    csrf = _get_csrf_token(cookie_jar)
    return opener, cookie_jar, csrf


def api_get(opener, url):
    """Make a GET request and return parsed JSON data."""
    req = urllib.request.Request(url, method="GET")
    with opener.open(req) as resp:
        body = json.loads(resp.read().decode())
    if body.get("error"):
        raise RuntimeError(f"API error: {body['data']}")
    return body.get("data")


def api_post(opener, cookie_jar, url, payload):
    """Make a POST request with CSRF token and return parsed JSON data."""
    csrf = _get_csrf_token(cookie_jar)
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Referer", BASE_URL + "/")
    req.add_header("Origin", BASE_URL)
    if csrf:
        req.add_header("X-CSRFToken", csrf)
    with opener.open(req) as resp:
        body = json.loads(resp.read().decode())
    cookie_jar.save(ignore_discard=True, ignore_expires=True)
    if body.get("error"):
        raise RuntimeError(f"API error: {body['data']}")
    return body.get("data")


def get_solution_dir(problem_id, contest_id=None):
    """Return the solution directory path for a problem, creating it if needed.

    Public:  .nccuoj/solution/public/<problem_id>/
    Contest: .nccuoj/solution/contest/<contest_id>/<problem_id>/
    """
    if contest_id:
        path = os.path.join(_NCCUOJ_DIR, "solution", "contest", str(contest_id), str(problem_id))
    else:
        path = os.path.join(_NCCUOJ_DIR, "solution", "public", str(problem_id))
    os.makedirs(path, exist_ok=True)
    return path
