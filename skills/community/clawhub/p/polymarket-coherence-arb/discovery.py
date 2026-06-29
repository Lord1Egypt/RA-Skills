"""Discover coherent market sets to arb.

A 'set' is a list of markets that are mutually exclusive AND exhaustive, so their YES prices
should sum to ~1. We only trade a set whose exclusivity we can CONFIRM from market text — anything
unconfirmed is reported (alert), never traded.

v0.1 confirms ONE relationship from text: a complete FIFA 'win Group X' set (4 legs, same letter,
2026 format = 4 teams/group). This is the one mutually-exclusive-exhaustive set we can verify
without external data. Remix `discover_sets()` to add other relationships — win-tournament <=
reach-final ladders, parlay consistency, etc.

You can also supply explicit market-id groups via the COHERENCE_GROUPS env var:
  COHERENCE_GROUPS="id1,id2,id3,id4; idA,idB,idC"   (';' separates groups, ',' separates legs)
Configured groups are trusted as-is (you are asserting their exclusivity).

NOTE: the canonical WC tag/series slug is unverified upstream; v0.1 discovers via text search and
filters locally. The shipped SDK (0.17.27) has no server-side search kwarg, so we try known
variants then fall back to an unfiltered fetch and regex-filter ourselves.
"""

import os
import re
import unicodedata

GROUP_RE = re.compile(r"win\s+group\s+([A-L])\b", re.IGNORECASE)
SEARCH_QUERIES = ["win Group", "World Cup Group"]
COMPLETE_SET_SIZE = 4   # 2026 format: 4 teams per group


def _norm(text):
    return unicodedata.normalize("NFKD", text or "")


def _fetch_markets(client, query, limit):
    """Docs show get_markets(q=..., limit=...) but shipped SDKs differ on the search kwarg.
    Try known variants, then fall back to an unfiltered fetch — we regex-filter locally anyway."""
    for kwargs in ({"q": query, "limit": limit}, {"query": query, "limit": limit},
                   {"search": query, "limit": limit}, {"limit": limit}):
        try:
            return client.get_markets(**kwargs)
        except TypeError:
            continue
    return client.get_markets()


def _configured_sets(client):
    """Explicit market-id groups from COHERENCE_GROUPS, trusted as mutually exclusive by the user."""
    raw = (os.getenv("COHERENCE_GROUPS") or "").strip()
    if not raw:
        return []
    out = []
    for i, grp in enumerate(raw.split(";")):
        ids = [x.strip() for x in grp.split(",") if x.strip()]
        markets = []
        for mid in ids:
            try:
                markets.append(client.get_market(mid))
            except Exception as exc:                      # one bad id must not kill the set
                print(f"  ! configured market {mid} fetch failed: {exc}")
        if len(markets) >= 2:
            out.append((f"configured[{i}]", markets))
    return out


def is_confirmed_set(legs):
    """Complete 4-leg group set, all 'win Group X' for the SAME letter -> exclusivity confirmed.
    Anything else (partial set, mixed letters, advance/qualify wording) -> NOT confirmed."""
    if len(legs) != COMPLETE_SET_SIZE:
        return False
    letters = {GROUP_RE.search(_norm(m.question)).group(1).upper() for m in legs
               if GROUP_RE.search(_norm(getattr(m, "question", "")))}
    return len(letters) == 1


def discover_sets(client, limit=200):
    """Return [(label, [markets])] of confirmed mutually-exclusive sets, deduped by market id.
    Unconfirmed candidates are printed as alerts and excluded."""
    sets = _configured_sets(client)
    seen = {}
    for q in SEARCH_QUERIES:
        try:
            for m in _fetch_markets(client, q, limit):
                if getattr(m, "status", "active") != "active":
                    continue
                match = GROUP_RE.search(_norm(getattr(m, "question", "")))
                if match:
                    seen.setdefault(match.group(1).upper(), {})[m.id] = m
        except Exception as exc:                          # one bad query must not kill the run
            print(f"  ! discovery query {q!r} failed: {exc}")
    for letter, d in sorted(seen.items()):
        legs = list(d.values())
        if is_confirmed_set(legs):
            sets.append((f"Group {letter}", legs))
        else:
            print(f"  ALERT [unconfirmed-set] Group {letter}: {len(legs)} visible leg(s) — "
                  f"exclusivity unconfirmed from text; alert only, no arb.")
    return sets
