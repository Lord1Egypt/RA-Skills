"""
Shared HTTP client for the indeed-skills scripts.

Pure Python standard library. Auth via the ROLESAPI_KEY environment
variable, sent as a Bearer token to https://api.rolesapi.com.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.rolesapi.com"
USER_AGENT = "indeed-skills/1.0.0 (+https://github.com/nikhonit/indeed-skills)"
TIMEOUT_SECONDS = 60
KEYS_URL = "https://rolesapi.com/app/keys"
BILLING_URL = "https://rolesapi.com/app/billing"


def api_key():
    key = os.environ.get("ROLESAPI_KEY", "").strip()
    if not key:
        sys.stderr.write(
            "ROLESAPI_KEY environment variable is not set.\n"
            "Create a key at " + KEYS_URL + " (free plan includes 100 credits, "
            "no card required), then run:\n"
            "  export ROLESAPI_KEY=rk_live_...\n"
        )
        sys.exit(2)
    return key


def _fail(status, payload):
    """Print a structured API error to stderr and exit nonzero."""
    err = {}
    if isinstance(payload, dict):
        err = payload.get("error") or {}
    code = err.get("code", "http_" + str(status))
    message = err.get("message", "Request failed with HTTP " + str(status))
    sys.stderr.write("API error " + code + ": " + message + "\n")
    if code == "out_of_credits":
        sys.stderr.write(
            "Your account has no credits left. Top up or upgrade at "
            + BILLING_URL + "\n"
        )
    elif code in ("missing_api_key", "invalid_api_key"):
        sys.stderr.write("Check your key or create a new one at " + KEYS_URL + "\n")
    sys.exit(1)


def request(method, path, params=None, body=None):
    """Call the API. Returns the parsed JSON envelope on success.

    Retries once on 429, honoring the Retry-After header. Any other
    error prints a message to stderr and exits nonzero.
    """
    url = API_BASE + path
    if params:
        filtered = {k: v for k, v in params.items() if v is not None}
        if filtered:
            url = url + "?" + urllib.parse.urlencode(filtered)
    data = None
    headers = {
        "Authorization": "Bearer " + api_key(),
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    if body is not None:
        data = json.dumps({k: v for k, v in body.items() if v is not None}).encode("utf-8")
        headers["Content-Type"] = "application/json"

    for attempt in (1, 2):
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            try:
                payload = json.loads(e.read().decode("utf-8"))
            except Exception:
                payload = {}
            if e.code == 429 and attempt == 1:
                retry_after = e.headers.get("Retry-After", "5")
                try:
                    wait = min(int(retry_after), 60)
                except ValueError:
                    wait = 5
                sys.stderr.write(
                    "Rate limited (429). Retrying once in " + str(wait) + "s...\n"
                )
                time.sleep(wait)
                continue
            _fail(e.code, payload)
        except urllib.error.URLError as e:
            sys.stderr.write("Network error: " + str(e.reason) + "\n")
            sys.exit(1)


def output(envelope):
    """Pretty-print the API response envelope to stdout."""
    print(json.dumps(envelope, indent=2, ensure_ascii=False))
