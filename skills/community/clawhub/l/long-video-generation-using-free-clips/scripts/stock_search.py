#!/usr/bin/env python3
"""Search free stock sources for each scene and store ranked candidates in project.json.

Sources (keys come from environment variables, never from files):
  pexels    PEXELS_API_KEY        videos + photos   (200 requests/hour, 20,000/month)
  pixabay   PIXABAY_API_KEY       videos + photos   (100 requests/60 s; responses are cached 24 h here)
  unsplash  UNSPLASH_ACCESS_KEY   photos, opt-in only (terms for use inside rendered videos are unclear)
  commons   no key                Wikimedia Commons; licence differs per file, always check
  archive   no key                Internet Archive; NOT automatically public domain, always check
Mixkit has no API in the sources checked: download by hand and register with fetch_clips.py add-local.

Usage
  stock_search.py PROJECT_DIR [--scene ID] [--sources pexels,pixabay] [--kinds video,image]
                  [--keep 12] [--max-keywords 3] [--per-page 8] [--max-requests 120] [--dry-run]
"""
import argparse
import os
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402

KEYS = {"pexels": "PEXELS_API_KEY", "pixabay": "PIXABAY_API_KEY", "unsplash": "UNSPLASH_ACCESS_KEY"}
DEFAULT_SOURCES = ["pexels", "pixabay"]
BUDGET = {"used": 0, "max": 120}


def get(url, headers=None, cache=None):
    # Only real network requests count against the budget; cached repeats are free.
    if not c.is_cached(url, cache):
        if BUDGET["used"] >= BUDGET["max"]:
            raise c.Fail(f"Request budget of {BUDGET['max']} reached; stopping so API limits are respected. "
                         "Cached results are kept; rerun later or raise --max-requests deliberately.")
        BUDGET["used"] += 1
    return c.http_json(url, headers=headers, cache_dir=cache)[0]


def cand(**kw):
    base = {"source": "", "id": "", "kind": "video", "url": "", "page_url": "", "creator": "", "creator_url": "",
            "license": "", "license_status": "ok", "attribution_required": True, "width": 0, "height": 0,
            "duration": 0, "thumb": "", "tags": "", "extra": {}}
    base.update(kw)
    base["id"] = str(base["id"])
    return base


def slug_words(url):
    """Words from a page URL slug, e.g. pexels.com/video/a-man-adjusting-an-air-conditioner-123/."""
    path = urllib.parse.urlsplit(url or "").path
    return " ".join(p for p in c.re.split(r"[/_-]+", path) if p and not p.isdigit())


def pick_rendition(files, width_key="width"):
    """Smallest rendition that is at least 1920 wide, else the widest. Avoids 4K downloads for a 1080p render."""
    files = [f for f in files if f.get(width_key)]
    if not files:
        return None
    big = [f for f in files if f[width_key] >= 1920]
    return min(big, key=lambda x: x[width_key]) if big else max(files, key=lambda x: x[width_key])


# ---- sources ---------------------------------------------------------------
def pexels_videos(q, key, per, cache):
    url = "https://api.pexels.com/v1/videos/search?" + urllib.parse.urlencode(
        {"query": q, "orientation": "landscape", "per_page": per})
    out = []
    for v in get(url, {"Authorization": key}, cache).get("videos", []):
        files = [f for f in v.get("video_files", []) if f.get("file_type") == "video/mp4" and f.get("width")]
        f = pick_rendition(files)
        if not f:
            continue
        user = v.get("user") or {}
        out.append(cand(source="pexels", id=v.get("id"), kind="video", url=f.get("link", ""), page_url=v.get("url", ""),
                        creator=user.get("name", ""), creator_url=user.get("url", ""), license="Pexels License",
                        width=f.get("width", 0), height=f.get("height", 0), duration=v.get("duration", 0),
                        thumb=v.get("image", ""), tags=slug_words(v.get("url", ""))))
    return out


def pexels_photos(q, key, per, cache):
    url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
        {"query": q, "orientation": "landscape", "per_page": per})
    out = []
    for p in get(url, {"Authorization": key}, cache).get("photos", []):
        src = p.get("src") or {}
        link = src.get("large2x") or src.get("original")
        if not link:
            continue
        out.append(cand(source="pexels", id=p.get("id"), kind="image", url=link, page_url=p.get("url", ""),
                        creator=p.get("photographer", ""), creator_url=p.get("photographer_url", ""),
                        license="Pexels License", width=p.get("width", 0), height=p.get("height", 0),
                        thumb=src.get("medium", ""), tags=p.get("alt") or slug_words(p.get("url", ""))))
    return out


def pixabay_videos(q, key, per, cache):
    url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode(
        {"key": key, "q": q[:100], "per_page": max(3, per), "safesearch": "true"})
    out = []
    for h in get(url, None, cache).get("hits", []):
        vs = h.get("videos") or {}
        f = pick_rendition([vs[k] for k in ("large", "medium", "small", "tiny") if (vs.get(k) or {}).get("url")])
        if not f:
            continue
        out.append(cand(source="pixabay", id=h.get("id"), kind="video", url=f["url"], page_url=h.get("pageURL", ""),
                        creator=h.get("user", ""), license="Pixabay Content License", width=f.get("width", 0),
                        height=f.get("height", 0), duration=h.get("duration", 0), tags=h.get("tags", "")))
    return out


def pixabay_images(q, key, per, cache):
    url = "https://pixabay.com/api/?" + urllib.parse.urlencode(
        {"key": key, "q": q[:100], "image_type": "photo", "orientation": "horizontal", "per_page": max(3, per),
         "safesearch": "true"})
    out = []
    for h in get(url, None, cache).get("hits", []):
        link = h.get("largeImageURL")
        if not link:
            continue
        out.append(cand(source="pixabay", id=h.get("id"), kind="image", url=link, page_url=h.get("pageURL", ""),
                        creator=h.get("user", ""), license="Pixabay Content License",
                        width=h.get("imageWidth", 0), height=h.get("imageHeight", 0), thumb=h.get("previewURL", ""),
                        tags=h.get("tags", "")))
    return out


def unsplash_images(q, key, per, cache):
    url = "https://api.unsplash.com/search/photos?" + urllib.parse.urlencode(
        {"query": q, "orientation": "landscape", "per_page": per})
    out = []
    for p in get(url, {"Authorization": f"Client-ID {key}"}, cache).get("results", []):
        urls, links, user = p.get("urls") or {}, p.get("links") or {}, p.get("user") or {}
        link = urls.get("full") or urls.get("regular")
        if not link:
            continue
        out.append(cand(source="unsplash", id=p.get("id"), kind="image", url=link, page_url=links.get("html", ""),
                        creator=user.get("name", ""), creator_url=(user.get("links") or {}).get("html", ""),
                        license="Unsplash License", license_status="check", width=p.get("width", 0),
                        height=p.get("height", 0), thumb=urls.get("small", ""),
                        tags=" ".join(filter(None, [p.get("alt_description"), p.get("description")])),
                        extra={"download_location": links.get("download_location", "")}))
    return out


def commons(q, per, cache, kinds):
    api = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6, "gsrsearch": q,
        "gsrlimit": per, "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata|mediatype"})
    pages = (get(api, None, cache).get("query") or {}).get("pages") or {}
    out = []
    for p in pages.values():
        info = (p.get("imageinfo") or [{}])[0]
        mime = info.get("mime", "")
        kind = "video" if mime.startswith("video/") else "image" if mime.startswith("image/") else ""
        if not kind or kind not in kinds or mime in ("image/svg+xml", "image/gif", "image/tiff"):
            continue
        if kind == "video" and mime not in ("video/webm", "video/ogg", "video/mp4"):
            continue
        md = info.get("extmetadata") or {}
        lic = (md.get("LicenseShortName") or {}).get("value", "unknown")
        artist = c.re.sub(r"<[^>]+>", "", (md.get("Artist") or {}).get("value", "")).strip()
        out.append(cand(source="commons", id=p.get("pageid"), kind=kind, url=info.get("url", ""),
                        page_url=info.get("descriptionurl", ""), creator=artist, license=lic, license_status="check",
                        width=info.get("width", 0), height=info.get("height", 0), duration=info.get("duration", 0),
                        tags=c.re.sub(r"^File:|\.\w+$", "", p.get("title", ""))))
    return out


def archive(q, per, cache):
    qs = f'({q}) AND mediatype:(movies) AND NOT collection:(podcasts)'
    url = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(
        {"q": qs, "fl[]": ["identifier", "title", "creator", "licenseurl"], "rows": per, "output": "json"}, doseq=True)
    out = []
    for d in (get(url, None, cache).get("response") or {}).get("docs", []):
        ident = d.get("identifier")
        if not ident:
            continue
        creator = d.get("creator", "")
        out.append(cand(source="archive", id=ident, kind="video", url="", page_url=f"https://archive.org/details/{ident}",
                        creator=", ".join(creator) if isinstance(creator, list) else creator,
                        license=d.get("licenseurl") or "unknown (check item page)", license_status="check",
                        tags=str(d.get("title", "")), extra={"title": d.get("title", "")}))
    return out


# ---- ranking ---------------------------------------------------------------
STOP = {"a", "an", "the", "of", "and", "or", "in", "on", "at", "to", "for", "with", "by", "from"}


def norm_words(text):
    out = set()
    for w in c.re.findall(r"[a-z0-9]+", str(text).lower()):
        if w in STOP or len(w) < 2:
            continue
        out.add(w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w)
    return out


WEAK = 0.3  # below this a candidate is treated as off-topic by fetch_clips.py pick (unless --allow-offtopic)


def relevance(cd, kw):
    """How well the result's own tags/title/alt text match the keyword, 0 to 1.
    Tag position counts (Pixabay lists the most important tags first): first tag 1.0, falling to 0.4 from the
    sixth tag on. A tag holding ALL the keyword's words scores that full value; if the words are only spread over
    tags, or only some are present, the score is halved, because single shared words mislead ("electricity meter"
    vs an audio "meter", "electricity bill" vs a dollar "bill", "air conditioner" vs "air, clouds").
    None = the source gave no text to compare (unknown), 0.0 = text present but no word matches."""
    want = norm_words(kw)
    text = str(cd.get("tags", ""))
    tags = [norm_words(t) for t in text.split(",")] if "," in text else [norm_words(text)]
    if not want or not any(tags):
        return None

    def pos(i):
        return max(0.4, 1 - 0.12 * i)

    full = next((i for i, t in enumerate(tags) if want <= t), None)
    if full is not None:
        return round(pos(full), 2)
    total = 0.0
    for w in want:
        idx = next((i for i, t in enumerate(tags) if w in t), None)
        total += 0 if idx is None else pos(idx)
    return round(0.5 * total / len(want), 2)


def score(cd, rank, shot):
    s = 0.0
    w, h = cd["width"] or 0, cd["height"] or 0
    if w and h and w < h:
        s -= 5
    s += 2 if w >= 1920 else 1 if w >= 1280 else 0 if w else -0.5
    rel = cd.get("relevance")
    if rel is not None:
        s += 6 * rel if rel >= WEAK else -6  # topic first: an on-topic photo must beat an off-topic video
    if cd["kind"] == "video":
        s += 1
        if cd["duration"] and cd["duration"] >= shot:
            s += 1
    if cd["license_status"] != "ok":
        s -= 1.5
    if cd["source"] == "archive":
        s -= 1
    s += max(0, 1.5 - 0.5 * rank)
    return round(s, 2)


def search_scene(scene, sources, kinds, per, max_kw, shot, cache, keys):
    found, seen = [], set()
    for rank, kw in enumerate((scene.get("keywords") or [])[:max_kw]):
        kw = str(kw).strip()
        if not kw:
            continue
        batch = []
        for src in sources:
            try:
                if src == "pexels":
                    if "video" in kinds:
                        batch += pexels_videos(kw, keys["pexels"], per, cache)
                    if "image" in kinds:
                        batch += pexels_photos(kw, keys["pexels"], per, cache)
                elif src == "pixabay":
                    if "video" in kinds:
                        batch += pixabay_videos(kw, keys["pixabay"], per, cache)
                    if "image" in kinds:
                        batch += pixabay_images(kw, keys["pixabay"], per, cache)
                elif src == "unsplash" and "image" in kinds:
                    batch += unsplash_images(kw, keys["unsplash"], per, cache)
                elif src == "commons":
                    batch += commons(kw, per, cache, kinds)
                elif src == "archive" and "video" in kinds:
                    batch += archive(kw, per, cache)
            except c.Fail as e:
                if "request budget" in str(e).lower() or "429" in str(e):
                    raise
                print(f"  ! {src} '{kw}': {e}", file=sys.stderr)
        for cd in batch:
            key = (cd["source"], cd["id"])
            if key in seen:
                continue
            seen.add(key)
            cd["query"] = kw
            cd["relevance"] = relevance(cd, kw)
            cd["score"] = score(cd, rank, shot)
            found.append(cd)
    found.sort(key=lambda x: -x["score"])
    return found


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir")
    ap.add_argument("--scene")
    ap.add_argument("--sources", default=",".join(DEFAULT_SOURCES))
    ap.add_argument("--kinds", default="video,image")
    ap.add_argument("--keep", type=int, default=12)
    ap.add_argument("--max-keywords", type=int, default=3)
    ap.add_argument("--per-page", type=int, default=8)
    ap.add_argument("--max-requests", type=int, default=120)
    ap.add_argument("--dry-run", action="store_true", help="show the planned request count and exit")
    a = ap.parse_args(argv)
    try:
        project = c.load_project(a.dir)
        sources = [s.strip() for s in a.sources.split(",") if s.strip()]
        bad = [s for s in sources if s not in ("pexels", "pixabay", "unsplash", "commons", "archive")]
        if bad:
            raise c.Fail(f"Unknown source(s): {', '.join(bad)}. Mixkit is manual: use fetch_clips.py add-local.")
        kinds = {k.strip() for k in a.kinds.split(",") if k.strip()}
        keys, usable = {}, []
        for s in sources:
            if s in KEYS:
                v = os.environ.get(KEYS[s], "").strip()
                if not v:
                    print(f"Skipping {s}: set {KEYS[s]} (free key).", file=sys.stderr)
                    continue
                keys[s] = v
            usable.append(s)
        if not usable:
            raise c.Fail("No usable source. Set PEXELS_API_KEY and/or PIXABAY_API_KEY, or add --sources commons.")
        scenes = [s for s in project["scenes"] if not a.scene or s["id"] == a.scene]
        if not scenes:
            raise c.Fail(f"No scene with id '{a.scene}'.")
        per_scene = min(a.max_keywords, 99) * sum(len(kinds) if s in ("pexels", "pixabay") else 1 for s in usable)
        print(f"Plan: {len(scenes)} scene(s) x up to {per_scene} requests = up to {len(scenes) * per_scene} requests "
              f"(budget {a.max_requests}; cached repeats are free).")
        if a.dry_run:
            return 0
        BUDGET["max"] = a.max_requests
        cache = str(Path(a.dir) / "cache" / "search")
        shot = project.get("shot_seconds", 6)
        try:
            for sc in scenes:
                found = search_scene(sc, usable, kinds, a.per_page, a.max_keywords, shot, cache, keys)
                rejected = {str(x) for x in sc.get("rejected", [])}
                found = [x for x in found if f"{x['source']}/{x['id']}" not in rejected]
                sc["candidates"] = found[:a.keep]
                kept = sc["candidates"]
                vids = sum(1 for x in kept if x["kind"] == "video")
                on = sum(1 for x in kept if (x.get("relevance") or 0) >= WEAK)
                off = sum(1 for x in kept if x.get("relevance") is not None and x["relevance"] < WEAK)
                note = "  <- none, change keywords" if not found else (
                    "  <- no on-topic match; use more common nouns, --kinds image, or add-local" if kept and not on else "")
                print(f"{sc['id']}: {len(found)} found, kept {len(kept)} ({vids} video; {on} on-topic, "
                      f"{off} off-topic by tags)" + note)
        finally:
            c.save_project(a.dir, project)
        print(f"Network requests: {c.STATS['network']}, cache hits: {c.STATS['cached']}. Saved to project.json.")
        return 0
    except c.Fail as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
