#!/usr/bin/env python3
"""Shared helpers for the 90-day social calendar pipeline.

Env loading rule (owner spec, 2026-08-18):
  - The ONLY env var this package requires is HIGHLEVEL_ACCESS_TOKEN,
    and it is only needed in HL-connected mode (--email).
  - Everything else (LLM key, image key, location id) can be passed as
    CLI flags. Optional env fallbacks are supported but never required.
  - A local .env file in the repo root is read if present (gitignored).
"""
import json
import os
import sys
import urllib.error
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_BASE = "https://services.leadconnectorhq.com"


def load_env() -> dict:
    env = dict(os.environ)
    dotenv = os.path.join(REPO_ROOT, ".env")
    if os.path.exists(dotenv):
        for line in open(dotenv):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def hl(method: str, path: str, token: str, body: dict = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        f"{API_BASE}{path}", data=data, method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Version": "2021-07-28",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/126.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"_error": f"HTTP {e.code}: {e.read().decode()[:300]}"}
    except Exception as e:
        return {"_error": str(e)}


def resolve_location(token: str, env: dict) -> str:
    """Return a location id for the token.

    Priority: HIGHLEVEL_LOCATION_ID env/flag value, else auto-detect from
    GET /locations/ (single location -> use it; multiple -> error with list).
    """
    loc = (env.get("HIGHLEVEL_LOCATION_ID") or "").strip()
    if loc:
        return loc
    r = hl("GET", "/locations/", token)
    locs = r.get("locations", []) if isinstance(r, dict) else []
    if not locs:
        raise SystemExit(
            "ERROR: could not resolve a HighLevel location. "
            "Set HIGHLEVEL_LOCATION_ID or pass --location-id."
        )
    if len(locs) == 1:
        return locs[0]["id"]
    names = "; ".join(f"{l.get('name','?')} ({l.get('id')})" for l in locs)
    raise SystemExit(
        f"ERROR: token has access to multiple locations: {names}. "
        "Set HIGHLEVEL_LOCATION_ID or pass --location-id."
    )


def find_custom_field_map(token: str, loc: str) -> dict:
    """Map custom field ids to names for a location."""
    r = hl("GET", f"/locations/{loc}/customFields?limit=100", token)
    fmap = {}
    for f in r.get("customFields", []):
        if isinstance(f, dict) and f.get("id") and f.get("name"):
            fmap[f["id"]] = f["name"]
    return fmap


def slugify(text: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-") or "client"
