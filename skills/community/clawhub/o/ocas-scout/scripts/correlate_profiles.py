#!/usr/bin/env python3
"""Cross-site profile correlation (stdlib-only; Pillow optional).

Clusters Found/Maybe profiles that look like the same person, using signals
Scout already holds plus avatar matching. This extends the token-bag entity
resolution into a correlation step that operates on *profiles* rather than
name columns.

Signals, in order of strength:

  1. avatar  — 64-bit dHash, Hamming distance <= AVATAR_MAX_HAMMING (8).
               Requires Pillow; degrades silently to the other signals when it
               is absent.
  2. link    — an identical external URL published in two bios
  3. name    — normalized display name equality
  4. bio     — Jaccard token overlap >= BIO_MIN_JACCARD (0.5)

Profiles are linked pairwise by these signals and grouped with union-find into
clusters ("likely the same person"). Every edge records which signal produced
it, so a brief can state WHY two profiles were joined.

A structured name is required for the name signal (see profile_extract.py's
``name_from_profile``) — a bare ``<title>`` is page chrome and would cluster
unrelated sites.

Usage:

    python3 correlate_profiles.py --input results.json
    python3 correlate_profiles.py --input results.json --format detailed
    python3 correlate_profiles.py --input results.json --min-cluster 2
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import re
import socket
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent))
from _envelope import add_format_arg, emit, fail, main_guard  # noqa: E402

_URL_RE = re.compile(r"https?://[^\s\"'<>)]+", re.IGNORECASE)
_HANDLE_RE = re.compile(r"@([A-Za-z0-9_.]{2,30})")
_WORD_RE = re.compile(r"[a-z0-9]+")

AVATAR_MAX_HAMMING = 8
BIO_MIN_JACCARD = 0.5

ALLOWED_AVATAR_SCHEMES = {"http", "https"}


def _tokens(text: str) -> set[str]:
    return {w for w in _WORD_RE.findall((text or "").lower()) if len(w) > 2}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _norm_name(name: str) -> str:
    return " ".join(_WORD_RE.findall((name or "").lower()))


# ── avatar hashing (optional Pillow) ───────────────────────────────────────

def pillow_available() -> bool:
    try:
        import PIL  # noqa: F401
        return True
    except ImportError:
        return False


def _dhash(image_bytes: bytes) -> int | None:
    """8x8 difference hash -> 64-bit int, or None if Pillow/decoding fails."""
    try:
        import io

        from PIL import Image
    except ImportError:
        return None
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("L").resize((9, 8))
    except Exception:  # noqa: BLE001
        return None
    bits = 0
    for row in range(8):
        for col in range(8):
            left = img.getpixel((col, row))
            right = img.getpixel((col + 1, row))
            bits = (bits << 1) | (1 if left > right else 0)
    return bits


def _hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def _all_public_infos(infos) -> bool:
    if not infos:
        return False
    for info in infos:
        try:
            addr = ipaddress.ip_address(info[4][0])
        except ValueError:
            return False
        if not addr.is_global or addr.is_private or addr.is_loopback:
            return False
    return True


def avatar_url_allowed(url: str, allow_private: bool = False) -> bool:
    """Whether an avatar URL is safe to fetch.

    Avatar URLs are scraped from the target page, so they are chosen by whoever
    controls that page. Fetching them unchecked turns a scan into a request
    generator aimed at cloud metadata endpoints, intranet hosts, or services on
    loopback. The host is resolved and every answer must be public.
    """
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    if parsed.scheme.lower() not in ALLOWED_AVATAR_SCHEMES:
        return False
    host = parsed.hostname
    if not host:
        return False
    if allow_private:
        return True
    try:
        infos = socket.getaddrinfo(host, None)
    except (OSError, UnicodeError):
        return False
    return _all_public_infos(infos)


def _fetch_avatar(url: str, timeout: float = 8.0,
                  allow_private: bool = False) -> bytes | None:
    if not avatar_url_allowed(url, allow_private):
        return None
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "hermes-osint-investigation/0.2"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read(2_000_000)
    except Exception:  # noqa: BLE001
        return None


# ── profiles ───────────────────────────────────────────────────────────────

def profiles_from_result(data, statuses=("Found", "Maybe")) -> list[dict]:
    """Extract correlatable profiles from a research result or report dict."""
    rows: list[dict] = []

    def _add(site, info):
        if not isinstance(info, dict):
            return
        status = info.get("status", "")
        if statuses and status not in statuses:
            return
        sig = ((info.get("ai_analysis") or {}).get("signals") or {}).get("profile") or {}
        prof = info.get("profile") or sig or {}
        bio = prof.get("bio", "") or ""
        name = prof.get("name", "") or ""
        structured = prof.get("name_from_profile")
        rows.append({
            "site": site,
            "url": info.get("url", "") or prof.get("url", ""),
            "avatar": prof.get("avatar", "") or "",
            # Only a structured name is an identity signal.
            "name": name if structured else "",
            "raw_name": name,
            "bio": bio,
            "links": {u.rstrip("/") for u in _URL_RE.findall(bio)},
            "handles": {h.lower() for h in _HANDLE_RE.findall(bio)},
            "status": status,
            "avatar_hash": None,
        })

    if isinstance(data, dict):
        for site, info in (data.get("sites") or {}).items():
            _add(site, info)
        for block in (data.get("variations") or {}).values():
            for site, info in ((block or {}).get("sites") or {}).items():
                _add(site, info)
        for prof in data.get("profiles") or []:
            if isinstance(prof, dict):
                _add(prof.get("site", ""), prof)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                _add(item.get("site", ""), item)
    return rows


def correlate(profiles: list[dict], fetch_avatars: bool = True,
              allow_private: bool = False, timeout: float = 8.0) -> dict:
    """Union-find clustering over the four signals. Returns clusters + edges."""
    n = len(profiles)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    # Avatar hashes first (best signal, and it needs the network anyway).
    hashing = fetch_avatars and pillow_available()
    if fetch_avatars and not hashing:
        for p in profiles:
            p["avatar_hash_note"] = "pillow_unavailable"
    if hashing:
        for p in profiles:
            if not p.get("avatar"):
                continue
            raw = _fetch_avatar(p["avatar"], timeout, allow_private)
            if raw:
                p["avatar_hash"] = _dhash(raw)

    edges: list[dict] = []
    tok = [_tokens(p.get("bio", "")) for p in profiles]

    for i in range(n):
        for j in range(i + 1, n):
            a, b = profiles[i], profiles[j]
            signals = []
            if (a["avatar_hash"] is not None and b["avatar_hash"] is not None
                    and _hamming(a["avatar_hash"], b["avatar_hash"])
                    <= AVATAR_MAX_HAMMING):
                signals.append("avatar")
            if a["links"] and b["links"] and (a["links"] & b["links"]):
                signals.append("link")
            if a["name"] and b["name"] and _norm_name(a["name"]) == _norm_name(b["name"]):
                signals.append("name")
            if tok[i] and tok[j] and _jaccard(tok[i], tok[j]) >= BIO_MIN_JACCARD:
                signals.append("bio")
            if signals:
                union(i, j)
                edges.append({
                    "left": a["site"], "right": b["site"],
                    "signals": signals,
                    "shared_links": sorted(a["links"] & b["links"])[:5],
                    "bio_jaccard": round(_jaccard(tok[i], tok[j]), 3),
                    "avatar_hamming": (
                        _hamming(a["avatar_hash"], b["avatar_hash"])
                        if a["avatar_hash"] is not None and b["avatar_hash"] is not None
                        else None),
                })

    groups: dict[int, list[dict]] = {}
    for idx, p in enumerate(profiles):
        groups.setdefault(find(idx), []).append(p)

    clusters = []
    for members in groups.values():
        if len(members) < 2:
            continue
        signal_set = sorted({
            s for e in edges
            if e["left"] in {m["site"] for m in members}
            and e["right"] in {m["site"] for m in members}
            for s in e["signals"]
        })
        clusters.append({
            "size": len(members),
            "signals": signal_set,
            "strength": ("high" if "avatar" in signal_set or "link" in signal_set
                         else "medium" if "name" in signal_set else "low"),
            "members": [{"site": m["site"], "url": m.get("url", ""),
                         "name": m.get("raw_name", "")} for m in members],
        })
    clusters.sort(key=lambda c: (-c["size"], c["strength"]))

    return {
        "profiles_considered": n,
        "avatar_hashing": bool(hashing),
        "clusters": clusters,
        "edges": edges,
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, help="Research result or report JSON")
    ap.add_argument("--min-cluster", type=int, default=2,
                    help="Minimum cluster size to report (default 2)")
    ap.add_argument("--no-avatars", action="store_true",
                    help="Skip avatar hashing (no image downloads)")
    ap.add_argument("--allow-private", action="store_true",
                    help="Permit fetching avatars from private/loopback hosts")
    ap.add_argument("--timeout", type=float, default=8.0)
    add_format_arg(ap)
    a = ap.parse_args()

    try:
        data = json.loads(Path(a.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"cannot read {a.input}: {exc}", a.format,
                    guidance=("Pass a JSON research result (the file written by "
                              "research_person.py) or a saved report. Check the "
                              "path and that the file is JSON."),
                    code="bad_input")

    profiles = profiles_from_result(data)
    if not profiles:
        return fail("no correlatable profiles in input", a.format,
                    guidance=("The input had no Found/Maybe profiles carrying a "
                              "profile block. Run profile_extract.py first to "
                              "attach structured profiles, then correlate."),
                    code="no_profiles")

    res = correlate(profiles, fetch_avatars=not a.no_avatars,
                    allow_private=a.allow_private, timeout=a.timeout)
    res["clusters"] = [c for c in res["clusters"] if c["size"] >= a.min_cluster]
    res["ok"] = True
    res["count"] = len(res["clusters"])

    note = ""
    if not res["avatar_hashing"] and not a.no_avatars:
        note = (" Avatar hashing skipped (Pillow absent) — clusters rest on "
                "link/name/bio signals only.")

    emit(
        res, a.format,
        summary=(f"{len(res['clusters'])} cluster(s) from "
                 f"{len(profiles)} profile(s).{note}"),
        concise_keys=("size", "strength", "signals", "members"),
    )
    if not res["clusters"]:
        print(json.dumps({"actionable_guidance": (
            "No clusters found. That is a normal result when the found profiles "
            "genuinely differ. If you expected overlap, confirm the input "
            "profiles carry bio/avatar fields (run profile_extract.py) and that "
            "avatar hashing was available.")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main_guard(main))
