#!/usr/bin/env python3
"""Resolve a chapter friendly-name (slug) to its endpoint URL via NEST.

The skill ships no hardcoded chapter→URL table. Discovery is dynamic:
ask the public NANDA registry (NEST) at runtime, filter to entries
that are actually NANDA chapters by probing /health.slug, return the
endpoint matching the requested slug.

Usage (from the OpenClaw agent's tool-call)::

    python helpers/discover_chapter.py boston
    # → {"slug":"boston","agent_id":"...","endpoint":"https://...",
    #    "display_name":"Boston TEST Chapter"}

    python helpers/discover_chapter.py            # list every chapter
    # → {"chapters":[{"slug":"bayarea","agent_id":...,"endpoint":...}, ...]}

Errors go to stderr; exit code is non-zero on failure.

Discovery algorithm:

  1. Paginate through GET https://nest.projectnanda.org/api/agents.
  2. Strip the `skill-` prefix that NEST adds to every id.
  3. Heuristic: keep only agent_ids ending in -chapter, -nanda-chapter,
     or -agent. Reduces the full list to a small candidate set.
  4. Drop entries with no endpoint (cannot route to them).
  5. /health probe: GET each candidate's /health and require a non-empty
     ``slug`` field. NANDA chapters declare this; non-NANDA agents that
     happen to share the suffix don't. The chapter's own /health.slug
     wins over any client-side derivation — operators control identity.
  6. KNOWN_CHAPTERS pin: chapters listed in ``KNOWN_CHAPTERS`` below
     MUST present the expected did:key in /health.did_key; otherwise
     they are dropped, even if /health.slug matches. This blocks slug
     collision / squatting on well-known names like ``bayarea``.
  7. Ambiguity rejection: if two distinct endpoints both claim the
     same slug, the slug is REMOVED from the result rather than
     resolving to a coin-flip winner. Users see "ambiguous slug" and
     can address by full URL.

A 30-second HMAC-SIGNED cache lives at
``$OPENCLAW_HOME/skills/nanda-chapter/chapter-cache.json``. The MAC
is keyed on the agent's identity private key so an attacker who can
write the cache file cannot poison the allowlist that
``sign_request.py`` consults. See helpers/_cache_signing.py.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import httpx

NEST_URL = "https://nest.projectnanda.org"
PAGE_LIMIT = 200
HTTP_TIMEOUT = 10.0
CACHE_TTL_SECONDS = 30

# Pinned did:keys for chapters with well-known slugs. Discovery refuses
# to resolve these slugs to any endpoint whose /health.did_key does
# not match. Empty until a chapter graduates to "well-known" status;
# adding an entry is a deliberate trust decision, not a discovery
# affordance.
KNOWN_CHAPTERS: dict[str, str] = {
    # Example shape: "bayarea": "did:key:z6Mk..."
    # Left empty pending the chapter publishing a stable did_key.
}


def _resolve_openclaw_home() -> Path:
    """Same validation contract as sign_request.py — refuses
    ``$OPENCLAW_HOME`` that resolves outside the calling user's home.
    """
    raw = os.environ.get("OPENCLAW_HOME", str(Path.home() / ".openclaw"))
    candidate = Path(raw).expanduser().resolve()
    home = Path.home().resolve()
    try:
        candidate.relative_to(home)
    except ValueError:
        print(
            json.dumps(
                {
                    "error": "openclaw_home_outside_user_home",
                    "openclaw_home": str(candidate),
                    "user_home": str(home),
                    "detail": (
                        "$OPENCLAW_HOME must resolve under the calling "
                        "user's home directory. Refusing to start."
                    ),
                }
            ),
            file=sys.stderr,
        )
        sys.exit(1)
    return candidate


OPENCLAW_HOME = _resolve_openclaw_home()
SKILL_DIR = OPENCLAW_HOME / "skills" / "nanda-chapter"
IDENTITY_FILE = SKILL_DIR / "identity.json"


def _cache_path() -> Path:
    SKILL_DIR.mkdir(parents=True, exist_ok=True)
    return SKILL_DIR / "chapter-cache.json"


def _load_cache() -> list[dict[str, Any]] | None:
    """Return the cached chapter list, or None if cache is missing /
    expired / unsigned / MAC-invalid. See helpers/_cache_signing.py
    for the verification contract.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _cache_signing import load_signed_cache  # noqa: E402

    return load_signed_cache(_cache_path(), IDENTITY_FILE)


def _save_cache(chapters: list[dict[str, Any]]) -> None:
    """Write a HMAC-signed, 0o600 cache file. Best-effort — a write
    failure does NOT raise; the skill works without the cache (just
    re-paginates NEST on the next call)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _cache_signing import write_signed_cache  # noqa: E402

    try:
        write_signed_cache(
            _cache_path(),
            IDENTITY_FILE,
            chapters=chapters,
            expires_at=int(time.time()) + CACHE_TTL_SECONDS,
        )
    except OSError:
        pass


def strip_skill_prefix(raw_id: str) -> str:
    """NEST returns ids prefixed with `skill-`; strip for matching."""
    return raw_id[len("skill-"):] if raw_id.startswith("skill-") else raw_id


def derive_chapter_slug(agent_id: str) -> str:
    """Best-effort slug derivation when /health is unreachable.

    The chapter's own /health.slug wins (see filter_to_chapters).
    This derivation is the fallback used to seed the candidate
    list; if /health is reachable the declared value overrides.
    """
    s = agent_id.lower()
    if s.startswith("test-"):
        s = s[len("test-"):]
    for suffix in ("-nanda-chapter", "-chapter", "-agent"):
        if s.endswith(suffix):
            s = s[: -len(suffix)]
            break
    return s or agent_id


def looks_like_chapter(agent_id: str) -> bool:
    """Heuristic — chapter naming convention vs. member agents."""
    s = agent_id.lower()
    return (
        s.endswith("-chapter")
        or s.endswith("-nanda-chapter")
        or s.endswith("-agent")
    )


def fetch_all_nest_agents(client: httpx.Client) -> list[dict[str, Any]]:
    """Paginate through every NEST entry (chapter + member alike)."""
    out: list[dict[str, Any]] = []
    page = 1
    while True:
        resp = client.get(
            f"{NEST_URL}/api/agents",
            params={"page": page, "limit": PAGE_LIMIT},
            timeout=HTTP_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        agents = data.get("agents", []) if isinstance(data, dict) else data
        if not agents:
            break
        out.extend(agents)
        pagination = data.get("pagination", {}) if isinstance(data, dict) else {}
        if not pagination.get("hasNext"):
            break
        page += 1
        if page > 200:  # safety cap
            break
    return out


def filter_to_chapters(
    agents: list[dict[str, Any]],
    *,
    fast: bool = False,
    client: httpx.Client | None = None,
) -> list[dict[str, Any]]:
    """Reduce NEST list to NANDA chapter records with slug + endpoint.

    Two-pass filter:

      1. Heuristic — keep only agent_ids ending in -chapter, -nanda-chapter,
         or -agent. Reduces 150+ NEST entries to ~10 candidates. Common
         convention but too loose on its own (random agents like
         `legentpro-agent` and `echo` end in -agent too).
      2. /health probe — GET each candidate's /health and require a
         non-empty ``slug`` field. NANDA chapters declare slug as part
         of their /health contract; non-NANDA agents don't have this
         field. This is the actual contract for "is this a NANDA chapter."

    Pass ``fast=True`` to skip the /health probe and trust the
    heuristic alone — used by the cache-rebuild path when NEST
    pagination is the bottleneck. False positives may surface as
    cache entries the agent will rediscover when it tries to use
    them; harmless but noisy.

    After the /health probe:

      a. KNOWN_CHAPTERS pin — pinned slugs MUST present the expected
         did_key in /health.did_key or they are dropped.
      b. Ambiguity rejection — if two distinct endpoints claim the
         same slug, the slug is removed entirely. Users must address
         by full URL rather than getting a coin-flip resolution.
    """
    candidates: list[dict[str, Any]] = []
    for agent in agents:
        agent_id = strip_skill_prefix(str(agent.get("id", "")))
        if not looks_like_chapter(agent_id):
            continue
        endpoint = agent.get("endpoint", "")
        if not endpoint:
            continue
        candidates.append(
            {
                "slug": derive_chapter_slug(agent_id),
                "agent_id": agent_id,
                "endpoint": endpoint,
                "display_name": agent.get("name") or agent_id,
                "description": agent.get("description", ""),
            }
        )

    if fast or client is None:
        return _reject_ambiguous_slugs(candidates)

    # /health probe — trust the chapter's own declared slug + display_name
    # + did_key. An entry without /health.slug is not a NANDA chapter and
    # gets dropped from the result.
    confirmed: list[dict[str, Any]] = []
    for chapter in candidates:
        try:
            health = client.get(
                f"{chapter['endpoint']}/health", timeout=HTTP_TIMEOUT
            ).json()
        except (httpx.HTTPError, json.JSONDecodeError, ValueError):
            continue
        declared_slug = health.get("slug")
        if not declared_slug:
            continue  # not a NANDA chapter — heuristic false positive
        chapter["slug"] = declared_slug
        if health.get("display_name"):
            chapter["display_name"] = health["display_name"]
        if health.get("did_key"):
            chapter["did_key"] = health["did_key"]

        # KNOWN_CHAPTERS pin — refuse to accept a chapter that claims
        # a well-known slug under a different did_key.
        pinned = KNOWN_CHAPTERS.get(declared_slug)
        if pinned and chapter.get("did_key") != pinned:
            continue

        confirmed.append(chapter)

    return _reject_ambiguous_slugs(confirmed)


def _reject_ambiguous_slugs(chapters: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """If two endpoints claim the same slug, drop the slug entirely.

    Users see no resolution rather than a coin-flip winner. We do not
    silently pick one — that's how slug-squatting attacks become
    successful in practice.

    All surviving records have their externally-supplied string fields
    sanitized — control-character / RTL-override / lookalike attacks
    against display_name and description are stripped here so cached
    records are LLM-safe by construction (M6 / A5).
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _sanitize import sanitize_chapter_record  # noqa: E402

    by_slug: dict[str, list[dict[str, Any]]] = {}
    for ch in chapters:
        by_slug.setdefault(ch["slug"], []).append(ch)
    out: list[dict[str, Any]] = []
    for _slug, entries in by_slug.items():
        # Distinct by endpoint — multiple NEST rows for the SAME
        # endpoint are merged silently (NEST occasionally double-lists).
        unique_endpoints = {e["endpoint"] for e in entries}
        if len(unique_endpoints) <= 1:
            out.append(sanitize_chapter_record(entries[0]))
    return out


def list_chapters(*, fast: bool = False, force_refresh: bool = False) -> list[dict[str, Any]]:
    """Return every NANDA chapter on NEST. Cached 30s unless --refresh.

    ``fast=True`` skips the /health probe (heuristic-only); see
    ``filter_to_chapters`` for the tradeoff. Default does the probe.
    """
    if not force_refresh:
        cached = _load_cache()
        if cached is not None:
            return cached
    with httpx.Client(follow_redirects=False) as client:
        agents = fetch_all_nest_agents(client)
        chapters = filter_to_chapters(agents, fast=fast, client=client)
    _save_cache(chapters)
    return chapters


def find_chapter(slug: str, **kwargs: Any) -> dict[str, Any] | None:
    """Return the chapter matching ``slug``, or None if not found."""
    target = slug.lower().strip()
    for chapter in list_chapters(**kwargs):
        if chapter["slug"] == target:
            return chapter
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("slug", nargs="?", help="Chapter slug to resolve. Omit to list all.")
    ap.add_argument(
        "--fast",
        action="store_true",
        help=(
            "Skip the /health probe — return heuristic matches directly. "
            "Faster but may include non-NANDA agents that happen to have "
            "a chapter-shaped agent_id."
        ),
    )
    ap.add_argument(
        "--refresh",
        action="store_true",
        help="Bypass the 30s LRU cache and re-paginate NEST.",
    )
    args = ap.parse_args()

    try:
        if args.slug is None:
            chapters = list_chapters(
                fast=args.fast, force_refresh=args.refresh
            )
            print(json.dumps({"chapters": chapters}))
            return 0

        chapter = find_chapter(
            args.slug, fast=args.fast, force_refresh=args.refresh
        )
        if chapter is None:
            available = [c["slug"] for c in list_chapters()]
            print(
                json.dumps(
                    {
                        "error": "chapter_not_found",
                        "slug": args.slug,
                        "available": available,
                    }
                )
            )
            return 2

        print(json.dumps(chapter))
        return 0
    except httpx.HTTPError as e:
        print(json.dumps({"error": "nest_unreachable", "detail": str(e)}), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
