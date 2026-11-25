#!/usr/bin/env python3
"""Structured profile extraction from a page (stdlib-only).

Turns a profile page into an ENTITY record — display name, bio, avatar — rather
than raw page text. Extraction order:

  1. Per-site CSS overrides from ``site_profiles.json`` (drop-in, like
     ``sites.d/``), for server-rendered profiles the generic rules miss.
  2. OpenGraph  (og:title / og:description / og:image)
  3. JSON-LD Person (name / image / description)
  4. ``<title>`` / ``<meta name=description>`` as a last resort

The ``name_from_profile`` flag records WHICH source supplied the name. Only a
*structured* name (OG title, JSON-LD Person, or a per-site override) is
trustworthy as an identity signal; a bare ``<title>`` fallback is page chrome
(bot walls, error pages, brand titles) and must not drive correlation. Callers
see the flag and decide — the extractor does not silently discard it.

Supported per-site selector subset (kept deliberately small so it stays
stdlib-only): ``tag``, ``.class``, ``tag.class``, ``.class1.class2``,
``#id``, ``tag#id``, and ``[attr=value]`` suffixed onto any of those. An
override that matches nothing is ignored and the generic value is kept, so a
stale selector degrades rather than blanks the field.

Usage:

    python3 profile_extract.py --url https://github.com/someone
    python3 profile_extract.py --html page.html --site github
    python3 profile_extract.py --input results.json --format detailed
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _envelope import add_format_arg, emit, fail, main_guard  # noqa: E402

_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

_OG = {
    "name": re.compile(r"(?is)<meta[^>]+property=[\"']og:title[\"'][^>]+content=[\"']([^\"']+)"),
    "bio": re.compile(r"(?is)<meta[^>]+property=[\"']og:description[\"'][^>]+content=[\"']([^\"']+)"),
    "avatar": re.compile(r"(?is)<meta[^>]+property=[\"']og:image[\"'][^>]+content=[\"']([^\"']+)"),
}
_META_DESC = re.compile(r"(?is)<meta[^>]+name=[\"']description[\"'][^>]+content=[\"']([^\"']+)")
_TITLE = re.compile(r"(?is)<title[^>]*>(.*?)</title>")
_LD_JSON = re.compile(r"(?is)<script[^>]+type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>")
_LD_PERSON = re.compile(r"\"@type\"\s*:\s*\"Person\"", re.IGNORECASE)
_URL_FIELDS = {
    "name": re.compile(r"\"name\"\s*:\s*\"([^\"]+)\""),
    "avatar": re.compile(r"\"image\"\s*:\s*\"([^\"]+)\""),
    "bio": re.compile(r"\"description\"\s*:\s*\"([^\"]+)\""),
}


def _clean(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).strip()


# ── minimal CSS selector subset ────────────────────────────────────────────

_TAG_RE = re.compile(r"<(?P<tag>[a-zA-Z][\w-]*)(?P<attrs>[^>]*)>")
_ATTR_RE = re.compile(r"([\w:-]+)\s*=\s*[\"']([^\"']*)[\"']")
_SEL_RE = re.compile(
    r"^(?P<tag>[a-zA-Z][\w-]*)?"
    r"(?P<id>#[\w-]+)?"
    r"(?P<classes>(?:\.[\w-]+)*)"
    r"(?P<attr>\[[\w-]+=[^\]]+\])?$"
)


def _parse_selector(sel: str):
    m = _SEL_RE.match((sel or "").strip())
    if not m:
        return None
    classes = [c for c in (m.group("classes") or "").split(".") if c]
    attr = None
    if m.group("attr"):
        inner = m.group("attr").strip("[]")
        if "=" in inner:
            k, v = inner.split("=", 1)
            attr = (k.strip(), v.strip().strip("\"'"))
    return {
        "tag": (m.group("tag") or "").lower(),
        "id": (m.group("id") or "").lstrip("#"),
        "classes": classes,
        "attr": attr,
    }


def _select_text(html: str, selector: str) -> str:
    """First text content matching a selector, or ''."""
    parsed = _parse_selector(selector)
    if not parsed:
        return ""
    for m in _TAG_RE.finditer(html):
        tag = m.group("tag").lower()
        if parsed["tag"] and tag != parsed["tag"]:
            continue
        attrs = dict(_ATTR_RE.findall(m.group("attrs") or ""))
        if parsed["id"] and attrs.get("id") != parsed["id"]:
            continue
        if parsed["classes"]:
            have = set((attrs.get("class") or "").split())
            if not set(parsed["classes"]) <= have:
                continue
        if parsed["attr"]:
            key, val = parsed["attr"]
            if attrs.get(key, "") != val:
                continue
        # Return the element's own text up to its closing tag (or a short tail).
        tail = html[m.end():m.end() + 2000]
        close = re.search(rf"(?is)</{re.escape(tag)}\s*>", tail)
        inner = tail[:close.start()] if close else tail[:400]
        text = _clean(inner)
        if text:
            return text
    return ""


def _select_attr(html: str, selector: str, attr: str) -> str:
    """First value of ``attr`` on an element matching a selector, or ''."""
    parsed = _parse_selector(selector)
    if not parsed:
        return ""
    for m in _TAG_RE.finditer(html):
        tag = m.group("tag").lower()
        if parsed["tag"] and tag != parsed["tag"]:
            continue
        attrs = dict(_ATTR_RE.findall(m.group("attrs") or ""))
        if parsed["id"] and attrs.get("id") != parsed["id"]:
            continue
        if parsed["classes"]:
            have = set((attrs.get("class") or "").split())
            if not set(parsed["classes"]) <= have:
                continue
        if parsed["attr"]:
            key, val = parsed["attr"]
            if attrs.get(key, "") != val:
                continue
        if attrs.get(attr):
            return attrs[attr].strip()
    return ""


# ── per-site overrides ─────────────────────────────────────────────────────

_profiles_cache: dict | None = None


def load_site_profiles(path: str | None = None) -> dict:
    """Per-site selector overrides, or {} when none are configured.

    Reads ``site_profiles.json`` next to this script, then the user config dir's
    copy. A missing or malformed file yields {} so extraction falls back to the
    generic rules rather than failing.
    """
    global _profiles_cache
    if path is None and _profiles_cache is not None:
        return _profiles_cache
    candidates = []
    if path:
        candidates.append(Path(path))
    else:
        candidates.append(Path(__file__).parent / "site_profiles.json")
        xdg = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
        candidates.append(Path(xdg) / "hermes-scout" / "site_profiles.json")
    merged: dict = {}
    for cand in candidates:
        try:
            data = json.loads(cand.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict):
            merged.update({k: v for k, v in data.items() if not k.startswith("_")})
    if path is None:
        _profiles_cache = merged
    return merged


# ── extraction ─────────────────────────────────────────────────────────────

def extract_profile(html: str, site: str = "", url: str = "",
                    site_profiles: dict | None = None) -> dict:
    """Extract a structured profile record from page HTML.

    Returns a dict with name/bio/avatar plus ``name_from_profile`` (True only
    when the name came from a structured field) and per-field ``*_source`` keys
    recording provenance for each extracted value.
    """
    html = html or ""
    overrides = (site_profiles if site_profiles is not None
                 else load_site_profiles()).get((site or "").lower(), {}) or {}

    out = {
        "site": site,
        "url": url,
        "name": "",
        "bio": "",
        "avatar": "",
        "name_from_profile": False,
        "sources": {},
    }

    # 1. per-site overrides first — a selector that matches nothing is ignored.
    if isinstance(overrides, dict):
        if overrides.get("name"):
            v = _select_text(html, overrides["name"])
            if v:
                out["name"] = v
                out["name_from_profile"] = True
                out["sources"]["name"] = "site_selector"
        if overrides.get("bio"):
            v = _select_text(html, overrides["bio"])
            if v:
                out["bio"] = v
                out["sources"]["bio"] = "site_selector"
        if overrides.get("avatar"):
            v = _select_attr(html, overrides["avatar"], "src") or _select_attr(
                html, overrides["avatar"], "data-src")
            if v:
                out["avatar"] = v
                out["sources"]["avatar"] = "site_selector"

    # 2. OpenGraph.
    for field, pattern in _OG.items():
        if out[field]:
            continue
        m = pattern.search(html)
        if m:
            out[field] = _clean(m.group(1))
            out["sources"][field] = "og"
            if field == "name":
                out["name_from_profile"] = True

    # 3. JSON-LD Person.
    if not (out["name"] and out["avatar"]):
        for block in _LD_JSON.findall(html):
            if not _LD_PERSON.search(block):
                continue
            for field, pattern in _URL_FIELDS.items():
                if out[field]:
                    continue
                m = pattern.search(block)
                if m:
                    out[field] = _clean(m.group(1))
                    out["sources"][field] = "jsonld_person"
                    if field == "name":
                        out["name_from_profile"] = True
            if out["name"] and out["avatar"]:
                break

    # 4. Last resort: <title> / <meta name=description>.
    #    The name here is page chrome, so name_from_profile stays False.
    if not out["name"]:
        m = _TITLE.search(html)
        if m:
            out["name"] = _clean(m.group(1))
            out["sources"]["name"] = "title_fallback"
    if not out["bio"]:
        m = _META_DESC.search(html)
        if m:
            out["bio"] = _clean(m.group(1))
            out["sources"]["bio"] = "meta_description"

    out["has_structured_name"] = bool(out["name_from_profile"])
    return out


def _fetch(url: str, timeout: float = 15.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read(400_000).decode("utf-8", errors="ignore")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--url", help="Page URL to fetch and extract from")
    src.add_argument("--html", help="Local HTML file to extract from")
    src.add_argument("--input", help="JSON file: a report or a list of profile URLs")
    ap.add_argument("--site", default="", help="Site name (selects per-site overrides)")
    ap.add_argument("--site-profiles", default="",
                    help="Path to a site_profiles.json (defaults to bundled/user)")
    add_format_arg(ap)
    a = ap.parse_args()

    overrides = load_site_profiles(a.site_profiles or None)

    if a.input:
        try:
            data = json.loads(Path(a.input).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return fail(f"cannot read {a.input}: {exc}", a.format,
                        guidance=("Pass a JSON file that exists and parses. "
                                  "For a person research result use the file "
                                  "written by research_person.py."),
                        code="bad_input")
        targets = []
        if isinstance(data, dict):
            for site, info in (data.get("sites") or {}).items():
                if isinstance(info, dict) and info.get("url"):
                    targets.append((site, info["url"]))
            for prof in data.get("profiles") or []:
                if isinstance(prof, dict) and prof.get("url"):
                    targets.append((prof.get("site", ""), prof["url"]))
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and item.get("url"):
                    targets.append((item.get("site", ""), item["url"]))
                elif isinstance(item, str):
                    targets.append(("", item))
        if not targets:
            return fail("no profile URLs found in input", a.format,
                        guidance=("The input had no 'sites', 'profiles' or URL "
                                  "entries. Pass --url for a single page, or a "
                                  "research result containing profiles."),
                        code="no_targets")
        rows = []
        for site, url in targets:
            country = site or _host_site(url)
            try:
                rows.append(extract_profile(_fetch(url), country, url, overrides))
            except Exception as exc:  # noqa: BLE001
                rows.append({"site": country, "url": url, "error": str(exc)[:200]})
        return _report(rows, a.format)

    if a.html:
        try:
            html = Path(a.html).read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            return fail(f"cannot read {a.html}: {exc}", a.format,
                        guidance="Check the path and re-run.",
                        code="bad_input")
    else:
        try:
            html = _fetch(a.url)
        except Exception as exc:  # noqa: BLE001
            return fail(f"fetch failed for {a.url}: {exc}", a.format,
                        guidance=("A fetch failure is usually a bot wall or a "
                                  "dead URL, not a bug. Fetch the page another "
                                  "way (browser tool / saved HTML) and pass it "
                                  "with --html."),
                        code="fetch_failed")

    site = a.site or _host_site(a.url or "")
    return _report([extract_profile(html, site, a.url or "", overrides)], a.format)


def _host_site(url: str) -> str:
    m = re.match(r"https?://([^/]+)", url or "")
    return (m.group(1) if m else "").lower()


def _report(rows: list[dict], fmt: str) -> int:
    ok = sum(1 for r in rows if r.get("name") and not r.get("error"))
    structured = sum(1 for r in rows if r.get("name_from_profile"))
    emit(
        {"ok": True, "count": len(rows), "extracted": ok,
         "structured_names": structured, "profiles": rows},
        fmt,
        summary=(f"{ok}/{len(rows)} profiles extracted "
                 f"({structured} with a structured name)"),
        concise_keys=("site", "url", "name", "bio", "avatar",
                      "name_from_profile", "sources", "error"),
    )
    if not ok and rows:
        print(json.dumps({
            "actionable_guidance": (
                "No name extracted. If every page is JS-rendered or bot-walled, "
                "fetch with a browser and pass --html. If a specific site is "
                "server-rendered but unrecognised, add a selector for it to "
                "site_profiles.json."
            )}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main_guard(main))
