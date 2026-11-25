#!/usr/bin/env python3
"""Recursive handle expansion from found profiles (stdlib-only).

Mines linked usernames out of profile bios and feeds them back as a new pass of
handle candidates. This is the step that turns a linear Sherlock -> Maigret
sweep into a graph walk: a bio that says "@oldhandle" or links to another
profile is a lead the first pass cannot see.

Hard cap: exactly ONE additional pass (2 total), per Scout invariant 9
(recursion cap). The cap is enforced structurally — this script emits the
NEXT pass's candidates and marks them ``pass=2``; it will refuse to emit a
third pass even if the second pass's bios contain more handles. Recursion is
capped because each pass multiplies cost and false-positive risk, and a chain
of username coincidences converges on nothing.

Handles are NOT auto-accepted. Each candidate carries the evidence that
produced it, and the caller applies the identity gate (invariant 7) — a handle
found in a bio is a lead, not a verified identity.

Usage:

    python3 recurse_expand.py --input results.json
    python3 recurse_expand.py --input results.json --pass 1 --format detailed
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _envelope import add_format_arg, emit, fail, main_guard  # noqa: E402

MAX_PASSES = 2

_HANDLE_RE = re.compile(r"@([A-Za-z0-9_.]{2,30})")
# Profile URLs whose path segment is a username.
_PROFILE_URL_RE = re.compile(
    r"https?://(?:www\.)?([a-z0-9.-]+)/(?:u/|user/|users/|profile/|@|in/)?"
    r"([A-Za-z0-9_.-]{2,40})/?$", re.IGNORECASE)

# Hosts where a path segment is a HANDLE; elsewhere the segment is often a
# slug, article id, or category and treating it as a handle invents leads.
_HANDLE_HOSTS = {
    "github.com", "gitlab.com", "twitter.com", "x.com", "bsky.app",
    "mastodon.social", "reddit.com", "medium.com", "dev.to", "keybase.io",
    "instagram.com", "tiktok.com", "youtube.com", "twitch.tv", "soundcloud.com",
    "behance.net", "dribbble.com", "pinterest.com", "telegram.me", "t.me",
    "linktr.ee", "about.me", "gravatar.com", "stackoverflow.com",
}

# Generic words that appear in bio links but are not handles.
_STOPWORDS = {
    "about", "contact", "privacy", "terms", "login", "signup", "home", "blog",
    "index", "search", "help", "support", "explore", "settings", "profile",
    "share", "watch", "feed", "rss", "api", "docs", "status", "jobs",
}


def _norm_handle(h: str, min_len: int = 2) -> str:
    h = (h or "").strip().strip(".").lstrip("@").lower()
    if len(h) < min_len or h in _STOPWORDS:
        return ""
    if re.fullmatch(r"\d+", h):     # numeric ids are not handles
        return ""
    return h


def handles_from_text(bio: str) -> list[dict]:
    """Handles mentioned in a bio, with the @-form or URL that produced them."""
    out = []
    for m in _HANDLE_RE.finditer(bio or ""):
        h = _norm_handle(m.group(1))
        if h:
            out.append({"handle": h, "via": "mention", "evidence": m.group(0)})
    for m in _PROFILE_URL_RE.finditer(bio or ""):
        host, seg = m.group(1).lower(), m.group(2)
        if host not in _HANDLE_HOSTS:
            continue
        h = _norm_handle(seg)
        if h:
            out.append({"handle": h, "via": "url", "evidence": m.group(0),
                        "host": host})
    return out


def _iter_profiles(data) -> list[dict]:
    rows = []
    if isinstance(data, dict):
        for prof in data.get("profiles") or []:
            if isinstance(prof, dict):
                rows.append(prof)
    elif isinstance(data, list):
        rows = [p for p in data if isinstance(p, dict)]
    return rows


def expand(data, current_pass: int = 1, known: set[str] | None = None) -> dict:
    """Produce next-pass handle candidates from the current result.

    ``current_pass`` is the pass the input represents. Pass 1 -> emits pass 2.
    A request to expand from pass 2 is refused (invariant 9).
    """
    current_pass = max(1, int(current_pass))
    if current_pass >= MAX_PASSES:
        return {
            "candidates": [],
            "refused": True,
            "reason": (f"recursion cap reached: pass {current_pass} of "
                       f"{MAX_PASSES} may not expand further (invariant 9)"),
        }

    known = {k.lower() for k in (known or set())}
    profiles = _iter_profiles(data)

    found: dict[str, dict] = {}
    for prof in profiles:
        bio = ""
        sig = ((prof.get("ai_analysis") or {}).get("signals") or {}).get("profile")
        if isinstance(sig, dict) and sig.get("bio"):
            bio = sig["bio"]
        if not bio and isinstance(prof.get("bio"), str):
            bio = prof["bio"]
        if not bio:
            continue
        origin = prof.get("site") or prof.get("url") or "unknown"
        for hit in handles_from_text(bio):
            h = hit["handle"]
            if h in known:
                continue
            entry = found.setdefault(h, {
                "handle": h, "pass": current_pass + 1, "sources": []})
            entry["sources"].append({
                "found_in": origin,
                "via": hit["via"],
                "evidence": hit["evidence"],
            })

    candidates = sorted(found.values(), key=lambda c: -len(c["sources"]))

    # A handle observed in TWO independent bios is corroborated; one is a lead.
    for c in candidates:
        c["corroborated"] = len({s["found_in"] for s in c["sources"]}) >= 2
        c["confidence"] = "medium" if c["corroborated"] else "low"

    return {
        "candidates": candidates,
        "refused": False,
        "from_pass": current_pass,
        "to_pass": current_pass + 1,
        "profiles_scanned": len(profiles),
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, help="Research result JSON")
    ap.add_argument("--pass", dest="current_pass", type=int, default=1,
                    help="Pass the input represents (default 1)")
    ap.add_argument("--known", default="",
                    help="Comma-separated handles already scanned (excluded)")
    ap.add_argument("--out", default="", help="Write candidates JSON to this path")
    add_format_arg(ap)
    a = ap.parse_args()

    try:
        data = json.loads(Path(a.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"cannot read {a.input}: {exc}", a.format,
                    guidance=("Pass a JSON research result or a list of profile "
                              "objects each carrying a bio."),
                    code="bad_input")

    known = {h.strip() for h in a.known.split(",") if h.strip()}
    res = expand(data, a.current_pass, known)
    res["ok"] = not res.get("refused")
    res["count"] = len(res["candidates"])

    if res.get("refused"):
        return fail(res["reason"], a.format,
                    guidance=("Do not re-run expansion for this subject. Apply "
                              "the identity gate to the pass-2 candidates you "
                              "already hold and finish the brief."),
                    code="recursion_cap",
                    extra={"candidates": []})

    emit(
        res, a.format,
        summary=(f"pass {res['from_pass']}->{res['to_pass']}: "
                 f"{len(res['candidates'])} new handle candidate(s) from "
                 f"{res['profiles_scanned']} profile(s)"),
        concise_keys=("handle", "confidence", "corroborated", "sources"),
    )

    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=2), encoding="utf-8")
        print(f"# wrote {a.out}")

    if not res["candidates"]:
        print(json.dumps({"actionable_guidance": (
            "No new handles. Expected when the found profiles carry no bios or "
            "link only to handles already scanned. Nothing further to expand — "
            "proceed to the identity gate and brief.")}))
    else:
        print(json.dumps({"actionable_guidance": (
            f"Feed these {len(res['candidates'])} handle(s) into one more "
            "scan pass, then STOP — this is the last permitted pass. Treat "
            "every candidate as a lead: apply the 2+ data-point identity gate "
            "before it enters synthesis.")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main_guard(main))
