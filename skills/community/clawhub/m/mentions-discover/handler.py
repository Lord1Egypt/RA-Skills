"""
mentions-discover skill handler — query discovery for AI-visibility tracking
via the MentionsAPI REST API.

Pure standard library. Bearer token in MENTIONSAPI_KEY.
"""

import json
import os
import urllib.error
import urllib.request

API_BASE = "https://api.mentionsapi.com"  # hardcoded: the API key is never sent to any other host
USER_AGENT = "llm-mentions-skills/1.0.0 (+https://github.com/nikhonit/llm-mentions-skills)"
TIMEOUT_SECONDS = 60

SIGNUP_URL = "https://mentionsapi.com/signup"
KEYS_URL = "https://mentionsapi.com/app/keys"
BILLING_URL = "https://mentionsapi.com/app/billing"


def _key():
    k = os.environ.get("MENTIONSAPI_KEY", "").strip()
    if not k:
        raise RuntimeError(
            "MENTIONSAPI_KEY environment variable is not set. "
            "Sign up free (no card, $1 credit) at " + SIGNUP_URL + ", "
            "mint a key at " + KEYS_URL + ", then export MENTIONSAPI_KEY=lvk_live_..."
        )
    return k


def _http_error(e):
    try:
        detail = e.read().decode("utf-8")[:1000]
    except Exception:
        detail = ""
    if e.code == 401:
        return {
            "error": "auth_invalid",
            "detail": "MENTIONSAPI_KEY was rejected. Rotate it at " + KEYS_URL + ".",
            "rotate_url": KEYS_URL,
            "http_status": 401,
        }
    if e.code == 402:
        return {
            "error": "insufficient_balance",
            "detail": "MentionsAPI wallet is empty. Top up ($5 minimum) at " + BILLING_URL + ".",
            "top_up_url": BILLING_URL,
            "http_status": 402,
            "body": detail,
        }
    if e.code == 429:
        return {
            "error": "rate_limit_exceeded",
            "detail": "Hit the rate limit. Back off and retry.",
            "http_status": 429,
        }
    return {"error": "HTTP " + str(e.code), "detail": detail}


def _post(path, payload):
    try:
        body = json.dumps({k: v for k, v in payload.items() if v is not None}).encode("utf-8")
        req = urllib.request.Request(
            API_BASE + path,
            data=body,
            method="POST",
            headers={
                "Authorization": "Bearer " + _key(),
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        return _http_error(e)
    except urllib.error.URLError as e:
        return {"error": "network", "detail": str(e.reason)}
    except RuntimeError as e:
        return {"error": "auth_required", "detail": str(e), "signup_url": SIGNUP_URL}
    except Exception as e:
        return {"error": "unexpected", "detail": str(e)}


def discover_queries(brand, industry=None, count=50):
    """
    Suggest queries worth tracking for `brand`'s AI visibility.

    brand:    brand to generate tracking queries for (e.g. "Linear")
    industry: optional context to sharpen suggestions (e.g. "project management")
    count:    how many queries to return, 1-100 (default 50)

    Returns the API response dict (candidate queries with intents),
    or {"error": "...", "detail": "..."} on failure.
    """
    if not brand:
        return {"error": "invalid_argument", "detail": "brand is required."}
    return _post("/v1/discover", {"brand": brand, "industry": industry, "count": count})
