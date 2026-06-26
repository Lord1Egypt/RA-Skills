"""
mentions-full skill handler — complete AI brand-visibility toolkit over the
MentionsAPI REST API: check_mentions, discover_queries, compare_mentions, watch_brand.

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

SHIPPABLE_MODES = (
    "quick",
    "perplexity_live",
    "chatgpt_live",
    "gemini_live",
    "ai_overview",
    "ai_mode",
    "bing_copilot",
    "all_live",
)


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
            "detail": "Hit the per-mode rate limit. Back off and retry.",
            "http_status": 429,
        }
    if e.code == 501:
        return {
            "error": "mode_roadmap",
            "detail": (
                "That mode is on the roadmap. Available today: "
                + ", ".join(SHIPPABLE_MODES)
                + "."
            ),
            "http_status": 501,
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


def check_mentions(query, brand, mode="quick", providers=None, runs=None, region=None):
    """
    Check whether `brand` is mentioned across AI search surfaces for `query`.

    mode: one of SHIPPABLE_MODES (default "quick").
    providers: subset of ["chatgpt","claude","gemini","perplexity"] (mode:quick only).
    runs: repeat 1-7 times to measure volatility (multiplies cost).
    Returns per-surface mentioned/rank/context/citations, or an {"error": ...} dict.
    """
    if not query or not brand:
        return {"error": "invalid_argument", "detail": "Both query and brand are required."}
    return _post(
        "/v1/check",
        {
            "query": query,
            "brand": brand,
            "mode": mode,
            "providers": providers,
            "runs": runs,
            "region": region,
        },
    )


def discover_queries(brand, industry=None, count=50):
    """
    Suggest queries worth tracking for `brand`'s AI visibility (informational,
    commercial, comparison intents). count: 1-100 (default 50).
    """
    if not brand:
        return {"error": "invalid_argument", "detail": "brand is required."}
    return _post("/v1/discover", {"brand": brand, "industry": industry, "count": count})


def compare_mentions(query_a, brand_a, query_b=None, brand_b=None, mode="quick"):
    """
    Compute the delta between two brands (same query) or two queries (same brand).

    Provide brand_b for competitor analysis, or query_b to compare phrasings.
    mode: "quick" or "perplexity_live" (default "quick").
    """
    if not query_a or not brand_a:
        return {"error": "invalid_argument", "detail": "query_a and brand_a are required."}
    return _post(
        "/v1/compare",
        {
            "query_a": query_a,
            "query_b": query_b,
            "brand_a": brand_a,
            "brand_b": brand_b,
            "mode": mode,
        },
    )


def watch_brand(
    query,
    brand,
    webhook_url,
    webhook_secret,
    mode="quick",
    interval="daily",
    trigger_on=None,
):
    """
    Create a persistent monitor that webhooks you when mentions/rank/citations change.

    webhook_url:    your HTTPS endpoint to receive change events
    webhook_secret: shared secret for HMAC signature verification (>= 16 chars)
    interval:       "hourly" | "daily" | "weekly" (default "daily")
    trigger_on:     subset of ["mention_added","mention_removed","rank_changed","citation_changed"]
    Billed per scheduled run ($1/run).
    """
    if not query or not brand:
        return {"error": "invalid_argument", "detail": "query and brand are required."}
    if not webhook_url or not webhook_secret:
        return {
            "error": "invalid_argument",
            "detail": "webhook_url and webhook_secret are required.",
        }
    if len(webhook_secret) < 16:
        return {
            "error": "invalid_argument",
            "detail": "webhook_secret must be at least 16 characters.",
        }
    return _post(
        "/v1/watch",
        {
            "query": query,
            "brand": brand,
            "mode": mode,
            "interval": interval,
            "webhook_url": webhook_url,
            "webhook_secret": webhook_secret,
            "trigger_on": trigger_on,
        },
    )
