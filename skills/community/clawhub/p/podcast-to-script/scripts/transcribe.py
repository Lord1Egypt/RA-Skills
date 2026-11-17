#!/usr/bin/env python3
"""Podcast episode link -> transcript, staged under $TMPDIR/podcast-to-script/<slug>/.

Output layout per episode (default; --out overrides):
  $TMPDIR/podcast-to-script/<slug>/
    raw.mp3            original audio enclosure (raw{ext} if not mp3; always kept)
    script.txt         raw transcript plain text (ALWAYS produced: from ASR, or
                       converted from the publisher's official transcript)
    script.srt/vtt     timestamped ASR output for quoting (ASR path only)
    chunks/            per-chunk ASR cache (re-runs resume)
    official_transcript.*  original file when the publisher ships one in RSS
  script.md / outline.md / notes.md are written later by the agent, next to these.

Accepted inputs:
  - Spotify episode URL   https://open.spotify.com/episode/...
  - Apple Podcasts URL    https://podcasts.apple.com/.../podcast/.../id<showId>?i=<episodeId>
  - RSS feed URL          any other URL; --title picks the episode
  - Direct audio URL      --audio <url> (skips metadata/feed resolution)

Pipeline:
  1. Resolve episode title + the show's public RSS feed:
     - Spotify: oEmbed title (no auth) -> iTunes Search API -> feedUrl
     - Apple:   iTunes Lookup by episode/show id -> feedUrl (+ title)
  2. If the RSS item carries a <podcast:transcript> tag (Podcasting 2.0),
     download it, convert to script.txt and stop (free, highest quality).
  3. Otherwise download the public <enclosure> audio (the podcast's own CDN
     file, no cracking) and transcribe locally with faster-whisper: PyAV
     decode -> 16 kHz mono -> 120 s chunks. Chunks transcribe in PARALLEL
     (--workers) and are cached in chunks/, so re-runs resume.
  4. Merge chunks into script.srt/vtt/txt.

Usage:
  python3 transcribe.py <episode_url_or_feed_url> [options]

Options:
  --title TEXT     Episode title hint: required for bare feed URLs with
                   multiple items; optional override elsewhere
  --audio URL      Direct audio file URL (bypasses metadata/feed steps)
  --slug NAME      Output dir slug (default: slugified title)
  --out DIR        Output directory (default: $TMPDIR/podcast-to-script/<slug>)
  --model NAME     faster-whisper model (default: small.en; use "small"
                   or "medium" for non-English audio)
  --lang CODE      Language hint, e.g. en/zh (default: en)
  --workers N      Parallel chunk workers (default: 4). Memory grows ~x N;
                   use 1-2 for medium/large models, 1 disables parallelism
  --proxy SPEC     HTTP proxy as user:pass@host:port (optional)
  --max-seconds N  Transcribe only the first N seconds (testing)
  --chunks-sec N   Chunk length in seconds (default: 120)

Requires: pip install faster-whisper  (pulls ctranslate2 + PyAV)
"""
import argparse
import difflib
import json
import math
import os
import re
import sys
import tempfile
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PODCAST_NS = "{https://podcastindex.org/namespace/1.0}"
UA = {"User-Agent": "Mozilla/5.0 (podcast-to-script/2.0)"}
AUDIO_EXTS = {".mp3", ".m4a", ".wav", ".aac", ".ogg", ".opus", ".flac"}


# ---------------------------------------------------------------- helpers

def http_get(url: str, proxy: str | None = None, timeout: int = 60) -> bytes:
    handlers = []
    if proxy:
        p = f"http://{proxy}"
        handlers.append(urllib.request.ProxyHandler({"http": p, "https": p}))
    opener = urllib.request.build_opener(*handlers)
    req = urllib.request.Request(url, headers=UA)
    with opener.open(req, timeout=timeout) as r:
        return r.read()


def download(url: str, dest: Path, proxy: str | None = None) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        print(f"[cache] {dest.name} already downloaded")
        return
    print(f"[download] {url[:100]}...")
    data = http_get(url, proxy=proxy, timeout=300)
    dest.write_bytes(data)
    print(f"[download] saved {dest} ({len(data)/1e6:.1f} MB)")


def slugify(text: str, maxlen: int = 48) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:maxlen].strip("-") or "episode"


def default_out_dir(slug: str) -> Path:
    """$TMPDIR/podcast-to-script/<slug> (tempfile honors the TMPDIR env var)."""
    return Path(tempfile.gettempdir()) / "podcast-to-script" / slug


def audio_ext_from_url(url: str) -> str:
    ext = Path(urllib.parse.urlparse(url).path).suffix.lower()
    return ext if ext in AUDIO_EXTS else ".mp3"


# ------------------------------------------------- input resolvers

def resolve_spotify(episode_url: str, proxy=None) -> dict:
    """Spotify episode URL -> {'title', 'feed'} via oEmbed + iTunes Search."""
    if not re.search(r"open\.spotify\.com/(?:intl-[a-z-]+/)?episode/[A-Za-z0-9]+", episode_url):
        sys.exit(f"ERROR: not a Spotify episode URL: {episode_url}")
    api = "https://open.spotify.com/oembed?url=" + urllib.parse.quote(episode_url, safe="")
    title = json.loads(http_get(api, proxy=proxy)).get("title", "")
    print(f"[meta] title: {title}")
    term = urllib.parse.quote(title)
    api = f"https://itunes.apple.com/search?term={term}&media=podcast&entity=podcastEpisode&limit=10"
    data = json.loads(http_get(api, proxy=proxy))
    best, best_ratio = None, 0.0
    for r in data.get("results", []):
        ratio = difflib.SequenceMatcher(None, r.get("trackName", "").lower(), title.lower()).ratio()
        if r.get("feedUrl") and ratio > best_ratio:
            best, best_ratio = r["feedUrl"], ratio
    if not best or best_ratio <= 0.5:
        sys.exit("ERROR: show has no public RSS feed (Spotify-exclusive?). Cannot proceed via RSS path.")
    print(f"[rss] feed: {best} (title match {best_ratio:.2f})")
    return {"title": title, "feed": best}


def resolve_apple(apple_url: str, proxy=None) -> dict:
    """Apple Podcasts URL -> {'title'|None, 'feed'} via iTunes Lookup."""
    m_show = re.search(r"/id(\d+)", apple_url)
    m_ep = re.search(r"[?&]i=(\d+)", apple_url)
    if m_ep:
        api = f"https://itunes.apple.com/lookup?id={m_ep.group(1)}&entity=podcastEpisode"
        results = json.loads(http_get(api, proxy=proxy)).get("results", [])
        for r in results:
            if r.get("feedUrl"):
                print(f"[meta] title: {r.get('trackName', '')}")
                print(f"[rss] feed: {r['feedUrl']}")
                return {"title": r.get("trackName", ""), "feed": r["feedUrl"]}
        sys.exit("ERROR: iTunes lookup returned no feedUrl for this episode id.")
    if m_show:
        api = f"https://itunes.apple.com/lookup?id={m_show.group(1)}&entity=podcast"
        results = json.loads(http_get(api, proxy=proxy)).get("results", [])
        for r in results:
            if r.get("feedUrl"):
                print(f"[rss] feed: {r['feedUrl']} (show-level link; --title picks the episode)")
                return {"title": None, "feed": r["feedUrl"]}
        sys.exit("ERROR: iTunes lookup returned no feedUrl for this show id.")
    sys.exit(f"ERROR: cannot parse show/episode id from Apple Podcasts URL: {apple_url}")


# ------------------------------------------------- RSS item handling

def load_items(feed_xml: bytes):
    channel = ET.fromstring(feed_xml).find("channel")
    if channel is None:
        sys.exit("ERROR: not an RSS 2.0 feed (no <channel>). Atom feeds are not supported.")
    return channel.findall("item")


def find_item(feed_xml: bytes, title: str):
    best, best_ratio = None, 0.0
    for item in load_items(feed_xml):
        t = (item.findtext("title") or "").strip()
        ratio = difflib.SequenceMatcher(None, t.lower(), title.lower()).ratio()
        if ratio > best_ratio:
            best, best_ratio = item, ratio
    if best is None or best_ratio < 0.5:
        return None
    print(f"[rss] matched item: {(best.findtext('title') or '').strip()[:80]} (match {best_ratio:.2f})")
    return best


def pick_item(feed_xml: bytes, title: str | None):
    """Pick an RSS item: fuzzy title match, or the only item in the feed."""
    items = load_items(feed_xml)
    if title:
        return find_item(feed_xml, title)
    if len(items) == 1:
        t = (items[0].findtext("title") or "").strip()
        print(f"[rss] single-item feed, using: {t[:80]}")
        return items[0]
    print("[rss] feed has multiple items; re-run with --title. Latest items:")
    for item in items[:10]:
        print(f"  - {(item.findtext('title') or '').strip()[:90]}")
    return None


TS_LINE_RE = re.compile(r"^\d{1,2}:\d{2}:\d{2}[.,]\d{1,3}\s*-->")


def transcript_to_txt(path: Path, out_dir: Path) -> Path:
    """Convert an official transcript (srt/vtt/json) to plain script.txt."""
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = []
    if path.suffix.lower() == ".json":
        data = json.loads(text)
        segs = data.get("segments") if isinstance(data, dict) else data
        for seg in segs or []:
            body = (seg.get("body") or seg.get("text") or "").strip() if isinstance(seg, dict) else ""
            if body:
                lines.append(body)
    else:
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line == "WEBVTT" or line.isdigit() or TS_LINE_RE.match(line):
                continue
            lines.append(line)
    dest = out_dir / "script.txt"
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[done] script.txt <- {path.name} ({len(lines)} lines)")
    return dest


def official_transcript(item, out_dir: Path, proxy=None) -> Path | None:
    for tr in item.findall(f"{PODCAST_NS}transcript"):
        url = tr.get("url")
        if not url:
            continue
        ext = ".json" if "json" in (tr.get("type") or "") else ".srt" if "srt" in (tr.get("type") or "") else ".vtt"
        dest = out_dir / f"official_transcript{ext}"
        download(url, dest, proxy=proxy)
        return dest
    return None


ITUNES_NS = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
CONTENT_NS = "{http://purl.org/rss/1.0/modules/content/}"
IMG_SRC_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)')
MAX_IMAGES = 12


def fetch_episode_images(feed_xml: bytes, item, out_dir: Path, proxy=None) -> list[Path]:
    """Download episode images (itunes:image, then <img> in description/content)
    into images/, with manifest.json mapping filename -> source URL. notes.md
    references these files by name; keep names stable (TOS filename match)."""
    urls: list[str] = []
    channel = ET.fromstring(feed_xml).find("channel")
    for owner in (item, channel):  # episode artwork wins over show artwork
        if owner is None:
            continue
        img = owner.find(f"{ITUNES_NS}image")
        if img is not None and img.get("href"):
            urls.append(img.get("href"))
            break
    for field in ("description", f"{CONTENT_NS}encoded"):
        urls.extend(IMG_SRC_RE.findall(item.findtext(field) or ""))

    img_dir = out_dir / "images"
    manifest: dict[str, str] = {}
    for u in urls:
        u = u.strip()
        if not u.startswith("http") or u in manifest.values():
            continue
        if len(manifest) >= MAX_IMAGES:
            break
        name = re.sub(r"[^A-Za-z0-9._-]+", "_",
                      Path(urllib.parse.urlparse(u).path).name) or "image.jpg"
        stem, dot, ext = name.rpartition(".")
        if not dot:
            name, stem, ext = name + ".jpg", name, "jpg"
        n = 1
        while name in manifest:
            n += 1
            name = f"{stem}_{n}.{ext}"
        try:
            dest = img_dir / name
            if not dest.exists() or dest.stat().st_size == 0:
                img_dir.mkdir(exist_ok=True)
                dest.write_bytes(http_get(u, proxy=proxy, timeout=60))
            manifest[name] = u
            print(f"[img] {name}")
        except Exception as e:
            print(f"[img] skip {u[:80]} ({type(e).__name__})")
    if manifest:
        (img_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2))
        print(f"[img] {len(manifest)} image(s) -> {img_dir}")
    return [img_dir / n for n in manifest]


# ------------------------------------------------------- whisper fallback

def transcribe_audio(audio_path: Path, out_dir: Path, model_name: str, lang: str,
                     chunk_sec: int, max_seconds: float | None, workers: int) -> list[dict]:
    import numpy as np
    from faster_whisper import WhisperModel
    from faster_whisper.audio import decode_audio

    chunk_dir = out_dir / "chunks"
    chunk_dir.mkdir(exist_ok=True)
    print(f"[asr] decoding {audio_path.name} ...")
    audio = decode_audio(str(audio_path), sampling_rate=16000)
    total_s = len(audio) / 16000
    if max_seconds:
        total_s = min(total_s, max_seconds)
        audio = audio[: int(total_s * 16000)]
    n_chunks = math.ceil(total_s / chunk_sec) or 1
    print(f"[asr] duration {total_s/60:.1f} min, model={model_name}, chunk={chunk_sec}s, "
          f"chunks={n_chunks}, workers={workers}")

    model_kw = {}
    if workers > 1:
        model_kw = {"num_workers": workers,
                    "cpu_threads": max(1, (os.cpu_count() or 4) // workers)}
    model = WhisperModel(model_name, device="cpu", compute_type="int8", **model_kw)

    def transcribe_chunk(i: int) -> tuple[int, int]:
        seg = audio[i * chunk_sec * 16000: min((i + 1) * chunk_sec * 16000, len(audio))]
        segments, _ = model.transcribe(
            np.asarray(seg), language=lang, vad_filter=True, beam_size=1,
            condition_on_previous_text=False,
        )
        offset = i * chunk_sec
        rows = [{"start": round(s.start + offset, 2), "end": round(s.end + offset, 2),
                 "text": s.text.strip()} for s in segments]
        (chunk_dir / f"chunk_{i:04d}.json").write_text(json.dumps(rows, ensure_ascii=False))
        return i, len(rows)

    pending = [i for i in range(n_chunks)
               if not (chunk_dir / f"chunk_{i:04d}.json").exists()]
    t0 = time.time()
    if workers > 1 and len(pending) > 1:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            for i, n in ex.map(transcribe_chunk, pending):
                print(f"[asr] chunk {i+1}/{n_chunks} done ({n} segs)", flush=True)
    else:
        for i in pending:
            t1 = time.time()
            _, n = transcribe_chunk(i)
            print(f"[asr] chunk {i+1}/{n_chunks} ({n} segs, {time.time()-t1:.0f}s)", flush=True)
    if pending:
        print(f"[asr] {len(pending)} chunk(s) transcribed in {time.time()-t0:.0f}s "
              f"(workers={workers})")

    segs = []
    for i in range(n_chunks):
        segs.extend(json.loads((chunk_dir / f"chunk_{i:04d}.json").read_text()))
    segs.sort(key=lambda x: x["start"])
    return segs


def fmt_ts(t: float, sep=",") -> str:
    h, m, s = int(t // 3600), int(t % 3600 // 60), int(t % 60)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{int(round((t - int(t)) * 1000)):03d}"


def write_outputs(segs: list[dict], out_dir: Path) -> None:
    srt, vtt, txt = [], ["WEBVTT", ""], []
    for idx, s in enumerate(segs, 1):
        srt.append(f"{idx}\n{fmt_ts(s['start'])} --> {fmt_ts(s['end'])}\n{s['text']}\n")
        vtt.append(f"{fmt_ts(s['start'], '.')} --> {fmt_ts(s['end'], '.')}\n{s['text']}\n")
        txt.append(s["text"])
    (out_dir / "script.srt").write_text("\n".join(srt), encoding="utf-8")
    (out_dir / "script.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (out_dir / "script.txt").write_text("\n".join(txt), encoding="utf-8")
    print(f"[done] {len(segs)} segments -> {out_dir}/script.{{srt,vtt,txt}}")


def transcribe_downloaded_audio(audio_path: Path, out_dir: Path, args) -> None:
    segs = transcribe_audio(audio_path, out_dir, args.model, args.lang,
                            args.chunks_sec, args.max_seconds, args.workers)
    write_outputs(segs, out_dir)
    print(f"[out] raw audio kept at {audio_path}")


# ------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Podcast episode link -> transcript")
    ap.add_argument("url", nargs="?", help="Spotify/Apple episode URL, or RSS feed URL")
    ap.add_argument("--title", help="Episode title hint (required for multi-item feeds)")
    ap.add_argument("--audio", help="Direct audio file URL (skips feed resolution)")
    ap.add_argument("--slug", help="Output dir slug (default: slugified title)")
    ap.add_argument("--out", help="Output dir (default: $TMPDIR/podcast-to-script/<slug>)")
    ap.add_argument("--model", default="small.en")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--workers", type=int, default=4,
                    help="parallel chunk workers (default 4; use 1-2 for large models)")
    ap.add_argument("--proxy")
    ap.add_argument("--max-seconds", type=float)
    ap.add_argument("--chunks-sec", type=int, default=120)
    args = ap.parse_args()
    args.workers = max(1, args.workers)

    if not args.url and not args.audio:
        ap.error("provide an episode/feed URL or --audio URL")

    # ---- Path 0: direct audio URL
    if args.audio:
        title = args.title or Path(urllib.parse.urlparse(args.audio).path).stem or "episode"
        slug = args.slug or slugify(title)
        out_dir = Path(args.out) if args.out else default_out_dir(slug)
        out_dir.mkdir(parents=True, exist_ok=True)
        audio_path = out_dir / f"raw{audio_ext_from_url(args.audio)}"
        download(args.audio, audio_path, proxy=args.proxy)
        transcribe_downloaded_audio(audio_path, out_dir, args)
        print(f"[dir] {out_dir}")
        return

    # ---- Resolve title + feed by input type
    url = args.url
    if "open.spotify.com" in url:
        resolved = resolve_spotify(url, proxy=args.proxy)
    elif "podcasts.apple.com" in url:
        resolved = resolve_apple(url, proxy=args.proxy)
    else:
        print(f"[rss] treating input as a feed URL: {url[:100]}")
        resolved = {"title": None, "feed": url}

    feed_xml = http_get(resolved["feed"], proxy=args.proxy)
    title = args.title or resolved["title"]
    if title:
        item = find_item(feed_xml, title)
    else:
        item = pick_item(feed_xml, None)  # single-item feed, or lists items and returns None
        if item is not None:
            title = (item.findtext("title") or "").strip()
    if item is None:
        sys.exit("ERROR: episode not found in RSS feed (pass --title to pick it).")

    slug = args.slug or slugify(title)
    out_dir = Path(args.out) if args.out else default_out_dir(slug)
    out_dir.mkdir(parents=True, exist_ok=True)
    fetch_episode_images(feed_xml, item, out_dir, proxy=args.proxy)

    # ---- Path 1: official transcript published in RSS -> also emit script.txt
    official = official_transcript(item, out_dir, proxy=args.proxy)
    if official:
        transcript_to_txt(official, out_dir)
        print(f"[dir] {out_dir}")
        return

    # ---- Path 2: download public enclosure, transcribe locally
    enc = item.find("enclosure")
    if enc is None or not enc.get("url"):
        sys.exit("ERROR: no audio enclosure in RSS item.")
    audio_path = out_dir / f"raw{audio_ext_from_url(enc.get('url'))}"
    download(enc.get("url"), audio_path, proxy=args.proxy)
    transcribe_downloaded_audio(audio_path, out_dir, args)
    print(f"[dir] {out_dir}")


if __name__ == "__main__":
    main()
