#!/usr/bin/env python3
"""Bounded, read-only Home Assistant REST queries (Python 3.10+, stdlib only)."""

import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
from http.client import HTTPException
import json
import math
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener


MAX_RESPONSE = 8 * 1024 * 1024
ENTITY = re.compile(r"[a-z0-9_]+\.[a-z0-9_]+\Z")
READ_PATH = re.compile(r"/api/(?:config|components|services|states(?:/[a-z0-9_]+\.[a-z0-9_]+)?|calendars)?\Z")


def safe_json(value, token):
    """Redact echoed credentials inside JSON strings while preserving valid JSON."""
    output = json.dumps(value, ensure_ascii=True, indent=2)
    return re.sub(r'"(?:\\.|[^"\\])*"',
                  lambda match: json.dumps(json.loads(match[0]).replace(token, "[REDACTED]")), output)


def time_window(start, end, maximum_days=31):
    try:
        first = datetime.fromisoformat(start.replace("Z", "+00:00"))
        last = datetime.fromisoformat(end.replace("Z", "+00:00"))
        if first.utcoffset() is None or last.utcoffset() is None or not timedelta(0) < last - first <= timedelta(days=maximum_days):
            raise ValueError
    except (ValueError, TypeError, OverflowError):
        raise HAError(f"Use timezone-aware ISO timestamps with end after start, at most {maximum_days} days apart.") from None
    return first.isoformat(), last.isoformat()


class HAError(Exception):
    """Safe diagnostics: never include credentials, response bodies or URLs."""


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Client:
    def __init__(self, url, token, timeout=30):
        try:
            parts = urlsplit(url)
            port = parts.port
        except ValueError:
            raise HAError("Invalid HA_URL.") from None
        if (parts.scheme not in {"http", "https"} or not parts.hostname
                or parts.username is not None or parts.password is not None
                or "?" in url or "#" in url or parts.path not in {"", "/"}
                or any(c.isspace() or ord(c) < 32 for c in url)
                or "\\" in url or port == 0):
            raise HAError("HA_URL must be an http(s) origin without credentials, path, query or fragment.")
        if not token or any(not 33 <= ord(c) <= 126 for c in token):
            raise HAError("Set a nonempty ASCII HA_TOKEN without whitespace.")
        if not math.isfinite(timeout) or not 0 < timeout <= 120:
            raise HAError("Timeout must be greater than 0 and at most 120 seconds.")
        self.url = url.rstrip("/")
        self.token = token
        self.timeout = timeout
        # Direct connections, verified TLS and no credential-bearing redirects.
        self.opener = build_opener(ProxyHandler({}), NoRedirect())

    def _request(self, path, data=None):
        body = None if data is None else json.dumps(data).encode("utf-8")
        request = Request(self.url + path, data=body, headers={
            "Authorization": "Bearer " + self.token,
            "Accept": "application/json", "Content-Type": "application/json",
        })
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                raw = response.read(MAX_RESPONSE + 1)
        except HTTPError as error:
            code = error.code
            error.close()
            hints = {401: "Check HA_TOKEN locally.", 403: "The user lacks permission.",
                     404: "Endpoint or entity not found.",
                     400: "Check entity, service support and parameters.",
                     503: "Home Assistant is unavailable or starting."}
            if 300 <= code < 400:
                raise HAError("Redirect refused; set HA_URL to the final trusted origin.") from None
            raise HAError(f"Home Assistant returned HTTP {code}. {hints.get(code, 'Request failed.')}") from None
        except (URLError, TimeoutError, OSError, ValueError, HTTPException):
            raise HAError("Connection failed or timed out; check reachability and TLS. No retry was sent.") from None
        if len(raw) > MAX_RESPONSE:
            raise HAError("Response exceeds the 8 MiB limit; query a specific entity.")
        try:
            return json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError, RecursionError):
            raise HAError("Expected a JSON API response; check HA_URL and proxy configuration.") from None

    def get(self, path):
        if not READ_PATH.fullmatch(path):
            raise HAError("Only /api/, config, components, services, states and calendars reads are allowed.")
        return self._request(path)

    def calendar(self, entity, days=7, now=None):
        if not ENTITY.fullmatch(entity) or not entity.startswith("calendar."):
            raise HAError("Use an exact calendar entity ID.")
        if not 1 <= days <= 31:
            raise HAError("Calendar window must be between 1 and 31 days.")
        start = now or datetime.now(timezone.utc)
        if start.tzinfo is None or start.utcoffset() is None:
            raise HAError("Calendar start must include a timezone.")
        query = urlencode({"start": start.isoformat(), "end": (start + timedelta(days=days)).isoformat()})
        return self._request(f"/api/calendars/{entity}?{query}")

    def forecast(self, entity, kind="daily"):
        if not ENTITY.fullmatch(entity) or not entity.startswith("weather."):
            raise HAError("Use an exact weather entity ID.")
        if kind not in {"daily", "hourly", "twice_daily"}:
            raise HAError("Forecast type must be daily, hourly or twice_daily.")
        # This is a data-returning service, not a device-control operation.
        result = self._request("/api/services/weather/get_forecasts?return_response",
                               {"entity_id": entity, "type": kind})
        try:
            forecast = result["service_response"][entity]["forecast"]
        except (KeyError, TypeError):
            raise HAError("Forecast response is missing service_response for the requested entity.") from None
        if not isinstance(forecast, list):
            raise HAError("Expected a forecast list.")
        return forecast

    def profile(self):
        config = self.get("/api/config")
        services = self.get("/api/services")
        if not isinstance(config, dict) or not isinstance(config.get("version"), str) or not isinstance(services, list):
            raise HAError("Expected versioned configuration and a REST service-domain list.")
        components = config.get("components", [])
        if not isinstance(components, list) or any(not isinstance(component, str) for component in components):
            raise HAError("Expected a list of loaded component names.")
        domains = {}
        for entry in services:
            if not isinstance(entry, dict) or not isinstance(entry.get("domain"), str) or not isinstance(entry.get("services"), dict):
                raise HAError("Expected REST service domains containing action-schema objects.")
            domains[entry["domain"]] = sorted(entry["services"])
        # Avoid leaking coordinates, URLs, filesystem paths and household names.
        return {"version": config["version"], "time_zone": config.get("time_zone"),
                "unit_system": config.get("unit_system"), "components": sorted(components),
                "actions": domains}

    def action_schema(self, action):
        if not ENTITY.fullmatch(action):
            raise HAError("Use an exact domain.action name.")
        domain, service = action.split(".", 1)
        result = self.get("/api/services")
        if not isinstance(result, list):
            raise HAError("Expected a REST service-domain list.")
        for entry in result:
            if isinstance(entry, dict) and entry.get("domain") == domain:
                services = entry.get("services")
                if isinstance(services, dict) and service in services:
                    return {"action": action, "schema": services[service]}
        raise HAError("Requested action is not exposed by this installation.")

    def health(self):
        states = self.get("/api/states")
        if not isinstance(states, list) or any(not isinstance(state, dict) or not isinstance(state.get("entity_id"), str) for state in states):
            raise HAError("Expected a list of entity state objects.")
        return {"entity_count": len(states),
                "domains": dict(sorted(Counter(s["entity_id"].split(".", 1)[0] for s in states).items())),
                "unavailable": [s["entity_id"] for s in states if s.get("state") == "unavailable"],
                "unknown": [s["entity_id"] for s in states if s.get("state") == "unknown"]}

    def history(self, entity, start, end):
        if not ENTITY.fullmatch(entity):
            raise HAError("Use one exact entity ID for history.")
        start, end = time_window(start, end, 7)
        query = urlencode({"filter_entity_id": entity, "end_time": end,
                           "minimal_response": "", "no_attributes": ""})
        from urllib.parse import quote
        return self._request(f"/api/history/period/{quote(start, safe='')}?{query}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=30)
    commands = parser.add_subparsers(dest="command", required=True)
    get = commands.add_parser("get", help="Read an allowlisted API endpoint")
    get.add_argument("path", nargs="?", default="/api/")
    calendar = commands.add_parser("calendar", help="Read upcoming events, including all-day events")
    calendar.add_argument("entity")
    calendar.add_argument("--days", type=int, default=7)
    forecast = commands.add_parser("forecast", help="Read forecasts using return_response")
    forecast.add_argument("entity")
    forecast.add_argument("--type", choices=["daily", "hourly", "twice_daily"], default="daily")
    commands.add_parser("profile", help="Installed version, units, components and exposed action names")
    commands.add_parser("health", help="Counts plus unavailable/unknown entity IDs; no full attributes")
    schema = commands.add_parser("action-schema", help="Inspect an action's fields/targets without calling it")
    schema.add_argument("action")
    history = commands.add_parser("history", help="Attribute-free recorder history for one entity (maximum 7 days)")
    history.add_argument("entity")
    history.add_argument("--start", required=True)
    history.add_argument("--end", required=True)
    args = parser.parse_args(argv)
    try:
        client = Client(os.environ.get("HA_URL", ""), os.environ.get("HA_TOKEN", ""), args.timeout)
        if args.command == "get":
            result = client.get(args.path)
        elif args.command == "calendar":
            result = client.calendar(args.entity, args.days)
        elif args.command == "forecast":
            result = client.forecast(args.entity, args.type)
        elif args.command == "profile":
            result = client.profile()
        elif args.command == "health":
            result = client.health()
        elif args.command == "action-schema":
            result = client.action_schema(args.action)
        else:
            result = client.history(args.entity, args.start, args.end)
        print(safe_json(result, client.token))
        return 0
    except HAError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
