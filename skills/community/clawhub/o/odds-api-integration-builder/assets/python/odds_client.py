"""Public read-only odds-api.net client. Python 3.10+, standard library only."""
import json
import os
import random
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


DEFAULT_BASE = "https://api.odds-api.net/v1"


class ClientError(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def checked_base(value):
    try:
        url = urllib.parse.urlsplit(value)
        port = url.port
    except ValueError:
        raise ClientError("ODDS_API_BASE_URL is invalid.") from None
    official = url.scheme == "https" and url.hostname == "api.odds-api.net" and port in (None, 443)
    loopback = url.scheme in ("http", "https") and url.hostname in ("localhost", "127.0.0.1", "::1")
    if not (official or loopback) or url.username or url.password or url.query or url.fragment or url.path.rstrip("/") != "/v1":
        raise ClientError("Use https://api.odds-api.net/v1 or an explicit loopback /v1 mock server.")
    return value.rstrip("/")


def utc_seconds(value):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?Z", value or ""):
        raise ClientError("Use an ISO 8601 UTC timestamp ending in Z.")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        raise ClientError("Invalid UTC calendar timestamp.") from None


def retry_delay(value):
    if value is None:
        return None
    try:
        number = float(value)
        if 0 <= number < float("inf"):
            return number
    except ValueError:
        pass
    try:
        return max(0, parsedate_to_datetime(value).timestamp() - time.time())
    except (ValueError, TypeError, OverflowError):
        return None


class OddsClient:
    def __init__(self, api_key=None, base=None, opener=None, sleep=time.sleep):
        self.base = checked_base(base or os.environ.get("ODDS_API_BASE_URL", DEFAULT_BASE))
        self._api_key = api_key if api_key is not None else os.environ.get("ODDS_API_KEY")
        if not isinstance(self._api_key, str) or not self._api_key.strip():
            raise ClientError("Set ODDS_API_KEY in your runtime; do not paste it into chat or command arguments.")
        if "\r" in self._api_key or "\n" in self._api_key:
            raise ClientError("ODDS_API_KEY contains an invalid newline.")
        self._opener = opener or urllib.request.build_opener(NoRedirect())
        self._sleep = sleep

    def get(self, path, **query):
        if not re.fullmatch(r"/(sports|leagues|bookmakers|coverage|events(?:/[A-Za-z0-9._~-]+/odds/(?:snapshot|history))?)", path):
            raise ClientError("Unsupported public read endpoint.")
        if any(re.fullmatch(r"api_key|apikey|access_token|token|authorization|x-api-key", key, re.I) for key in query):
            raise ClientError("Credentials belong only in the authentication header.")
        values = {key: str(value).lower() if isinstance(value, bool) else value for key, value in query.items() if value is not None and value != ""}
        url = self.base + path + ("?" + urllib.parse.urlencode(values) if values else "")
        for attempt in range(3):
            request = urllib.request.Request(url, headers={"X-API-Key": self._api_key, "Accept": "application/json"})
            try:
                with self._opener.open(request, timeout=20) as response:
                    try:
                        data = json.load(response)
                    except (ValueError, UnicodeError):
                        raise ClientError("The API returned invalid JSON.") from None
                    if not isinstance(data, dict):
                        raise ClientError("The API returned an unexpected response shape.")
                    return data
            except urllib.error.HTTPError as error:
                if error.code == 429:
                    wait = retry_delay(error.headers.get("Retry-After"))
                    if wait is None:
                        wait = 0.5 * 2 ** attempt + random.random() * 0.25
                    error.close()
                    if attempt == 2 or wait > 30:
                        raise ClientError("Rate or quota limit reached. Retry later; check usage and limits.") from None
                    self._sleep(wait)
                    continue
                request_id = error.headers.get("X-Request-ID", "")
                suffix = " Request ID: " + request_id + "." if re.fullmatch(r"[A-Za-z0-9._:-]{1,128}", request_id) else ""
                code = error.code
                error.close()
                reason = {401: "Check runtime authentication.", 403: "Check account and add-on access.", 404: "Discover a current event ID.", 422: "Check the documented filters."}.get(code, "Request failed; redirects are refused.")
                raise ClientError(f"HTTP {code}: {reason}{suffix}") from None
            except (urllib.error.URLError, TimeoutError, OSError):
                raise ClientError("API connection failed or timed out. Check connectivity and retry.") from None

    def pages(self, path, snapshot=False, **query):
        pages, seen = [], set()
        cursor, count = None, 0
        for _ in range(50):
            data = self.get(path, **dict(query, cursor=cursor))
            if not isinstance(data.get("items"), list):
                raise ClientError("Expected an items array.")
            count += len(data["items"])
            if count > 100000:
                raise ClientError("Response too broad. Narrow filters.")
            pages.append(data)
            cursor = data.get("next_cursor")
            if snapshot and data.get("complete") is False and not cursor:
                raise ClientError("Snapshot incomplete without a continuation cursor.")
            if snapshot and data.get("complete") is True and cursor:
                raise ClientError("Inconsistent snapshot pagination metadata.")
            if not cursor:
                return pages
            if not isinstance(cursor, str) or cursor in seen:
                raise ClientError("Pagination did not advance. Narrow filters.")
            seen.add(cursor)
        raise ClientError("Pagination limit reached. Narrow the request.")

    def snapshot(self, event_id, **query):
        if not re.fullmatch(r"[A-Za-z0-9_-][A-Za-z0-9._~-]{0,199}", event_id or ""):
            raise ClientError("Supply a canonical event ID from event discovery.")
        pages = self.pages(f"/events/{event_id}/odds/snapshot", snapshot=True,
                           **{"price_fields": "odds", "include_unavailable": False, "include_stale": False, **query})
        if any(page.get("event_id") != event_id for page in pages):
            raise ClientError("Snapshot event ID does not match the request.")
        return {"event_id": event_id, "complete": True, "pages": pages}
