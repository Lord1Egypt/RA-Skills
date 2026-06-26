#!/usr/bin/env python3
"""Idea Vault helper.

This script is designed to be called by an OpenClaw agent.
It does three things:

1) extract: Parse recent Discord messages into a structured capture (URL, timestamps, notes, attachments).
2) fetch: Fetch YouTube captions/transcript and build clip snippets around timestamps.
3) save: Write a markdown entry + update an index.json, optionally downloading attachments.

All IO is JSON via stdin/stdout and files on disk.

Stdlib + requests only.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import html
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
import unicodedata
from typing import Any, Dict, List, Optional, Tuple

import requests

TRANSCRIPTAPI_BASE = os.environ.get('IDEA_VAULT_TRANSCRIPTAPI_BASE', 'https://transcriptapi.com/api/v2')
CHANNEL_HANDLE_DEFAULT = os.environ.get('IDEA_VAULT_CHANNEL_HANDLE', '@example_channel')


# -------------------------
# Utilities
# -------------------------

def utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def slugify(s: str, max_len: int = 80) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    if not s:
        s = "entry"
    return s[:max_len].strip("-")


def hms(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def parse_video_id(url: str) -> Optional[str]:
    # youtu.be/<id>
    m = re.search(r"https?://youtu\.be/([A-Za-z0-9_-]{6,})", url)
    if m:
        return m.group(1)
    # youtube.com/watch?v=<id>
    m = re.search(r"[?&]v=([A-Za-z0-9_-]{6,})", url)
    if m:
        return m.group(1)
    # shorts
    m = re.search(r"https?://(?:www\.)?youtube\.com/shorts/([A-Za-z0-9_-]{6,})", url)
    if m:
        return m.group(1)
    return None


def parse_youtube_time_param(url: str) -> Optional[int]:
    # t=1234 or t=1h2m3s or start=...
    m = re.search(r"[?&](?:t|start)=([^&#]+)", url)
    if not m:
        return None
    val = m.group(1)
    if val.isdigit():
        return int(val)
    # 1h2m3s
    mh = re.search(r"(\d+)h", val)
    mm = re.search(r"(\d+)m", val)
    ms = re.search(r"(\d+)s", val)
    if any([mh, mm, ms]):
        h = int(mh.group(1)) if mh else 0
        mi = int(mm.group(1)) if mm else 0
        se = int(ms.group(1)) if ms else 0
        return h * 3600 + mi * 60 + se
    return None


Timestamp = Tuple[int, str]  # (seconds, raw)


def _ts_from_parts(parts: List[int]) -> int:
    if len(parts) == 2:
        m, s = parts
        return m * 60 + s
    if len(parts) == 3:
        h, m, s = parts
        return h * 3600 + m * 60 + s
    raise ValueError(parts)


def parse_timestamps_freeform(text: str) -> List[Timestamp]:
    """Parse timestamps from freeform text.

    Supports:
      - 24:21
      - 1:02:33
      - 24.21 (interpreted as 24:21)
      - @45.00 / @45:00
      - "at 24 mins 21 seconds"
      - "at 1 hour 2 mins 3 seconds"
    """
    out: List[Timestamp] = []

    # hh:mm:ss or mm:ss
    for m in re.finditer(r"(?<!\d)(@?)(\d{1,2}):(\d{2})(?::(\d{2}))?(?!\d)", text):
        h_or_m = int(m.group(2))
        mm = int(m.group(3))
        ss = int(m.group(4)) if m.group(4) else None
        if ss is None:
            secs = _ts_from_parts([h_or_m, mm])
        else:
            secs = _ts_from_parts([h_or_m, mm, ss])
        out.append((secs, m.group(0)))

    # mm.ss (treat as mm:ss)
    for m in re.finditer(r"(?<!\d)(@?)(\d{1,3})\.(\d{2})(?!\d)", text):
        mins = int(m.group(2))
        secs = int(m.group(3))
        out.append((mins * 60 + secs, m.group(0)))

    # "at 24 mins 21 seconds" / variants
    for m in re.finditer(
        r"\bat\s+(\d+)\s*(?:mins?|minutes?)\s+(\d+)\s*(?:secs?|seconds?)\b",
        text,
        flags=re.IGNORECASE,
    ):
        mins = int(m.group(1))
        secs = int(m.group(2))
        out.append((mins * 60 + secs, m.group(0)))

    for m in re.finditer(
        r"\bat\s+(\d+)\s*(?:hours?|hrs?)\s+(\d+)\s*(?:mins?|minutes?)\s+(\d+)\s*(?:secs?|seconds?)\b",
        text,
        flags=re.IGNORECASE,
    ):
        hh = int(m.group(1))
        mm = int(m.group(2))
        ss = int(m.group(3))
        out.append((hh * 3600 + mm * 60 + ss, m.group(0)))

    # De-dupe preserving first raw form
    seen = set()
    dedup: List[Timestamp] = []
    for secs, raw in out:
        if secs not in seen:
            seen.add(secs)
            dedup.append((secs, raw))
    return sorted(dedup, key=lambda x: x[0])


YOUTUBE_URL_RE = re.compile(r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)/\S+", re.IGNORECASE)
URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)


def find_youtube_urls(text: str) -> List[str]:
    return [m.group(0).rstrip(")].,>") for m in YOUTUBE_URL_RE.finditer(text)]


def find_urls(text: str) -> List[str]:
    """Find generic http(s) URLs in text."""
    return [m.group(0).rstrip(")].,>") for m in URL_RE.finditer(text)]


# -------------------------
# YouTube transcript fetch
# -------------------------


def _extract_json_object(text: str, anchor: str) -> Optional[dict]:
    """Find a JS assignment like `anchor = {...};` and return the parsed JSON object.

    Uses brace matching to extract the JSON substring.
    """
    idx = text.find(anchor)
    if idx < 0:
        return None
    # Find first '{' after anchor
    brace = text.find("{", idx)
    if brace < 0:
        return None
    depth = 0
    in_str = False
    esc = False
    for i in range(brace, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        else:
            if ch == '"':
                in_str = True
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    blob = text[brace : i + 1]
                    try:
                        return json.loads(blob)
                    except Exception:
                        return None
    return None


def fetch_youtube_player_response(video_id: str, lang: str = "en") -> dict:
    url = f"https://www.youtube.com/watch?v={video_id}&hl={lang}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
        "Accept-Language": f"{lang},en;q=0.9",
    }
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    html_text = r.text

    # Common forms: `var ytInitialPlayerResponse = {...};` or `ytInitialPlayerResponse = {...};`
    pr = _extract_json_object(html_text, "ytInitialPlayerResponse")
    if not pr:
        # Fallback: sometimes embedded in a JSON blob
        m = re.search(r"\"ytInitialPlayerResponse\"\s*:\s*(\{)", html_text)
        if m:
            start = m.start(0)
            pr = _extract_json_object(html_text[start:], "ytInitialPlayerResponse")
    if not pr:
        raise RuntimeError("Could not parse ytInitialPlayerResponse from YouTube HTML")

    return pr


def fetch_youtube_oembed(video_id: str) -> Optional[dict]:
    """Fetch basic metadata via YouTube oEmbed (often accessible even when watch page is gated)."""
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


def pick_caption_track(pr: dict, prefer_lang: str = "en") -> Optional[dict]:
    caps = (
        pr.get("captions", {})
        .get("playerCaptionsTracklistRenderer", {})
        .get("captionTracks", [])
    )
    if not caps:
        return None

    def score(track: dict) -> Tuple[int, int]:
        lang = track.get("languageCode", "")
        kind = track.get("kind", "")
        is_asr = 1 if kind == "asr" else 0
        is_pref = 1 if lang.startswith(prefer_lang) else 0
        # prefer pref lang, prefer non-asr
        return (is_pref, -is_asr)

    caps_sorted = sorted(caps, key=score, reverse=True)
    return caps_sorted[0]


def fetch_caption_json(track_base_url: str) -> dict:
    """Fetch YouTube timedtext as json3.

    YouTube caption track baseUrl may already contain fmt=srv3 (XML-ish). We force fmt=json3.
    """
    url = track_base_url
    if "fmt=" in url:
        url = re.sub(r"([?&])fmt=[^&]+", r"\1fmt=json3", url)
    else:
        url += "&fmt=json3"

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
        "Accept-Language": "en,en;q=0.9",
    }
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    try:
        return r.json()
    except Exception as e:
        # Helpful debugging payload (often HTML)
        snippet = (r.text or "")[:400]
        raise RuntimeError(f"Failed to parse captions JSON (status={r.status_code}). First bytes: {snippet}") from e


@dataclasses.dataclass
class TranscriptSeg:
    start: float
    end: float
    text: str


def parse_vtt(path: str) -> List[TranscriptSeg]:
    """Parse a WebVTT subtitle file into segments.

    Minimal parser: extracts time ranges and associated text.
    """
    def to_sec(ts: str) -> float:
        # 00:01:02.345 or 01:02.345
        ts = ts.replace(',', '.')
        parts = ts.split(':')
        if len(parts) == 3:
            h, m, s = parts
        elif len(parts) == 2:
            h = '0'
            m, s = parts
        else:
            return 0.0
        return int(h) * 3600 + int(m) * 60 + float(s)

    segs: List[TranscriptSeg] = []
    cur_start = None
    cur_end = None
    cur_lines: List[str] = []

    time_re = re.compile(r"^(\d{1,2}:)?\d{2}:\d{2}\.\d{3}\s+-->\s+(\d{1,2}:)?\d{2}:\d{2}\.\d{3}")

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for raw in f:
            line = raw.strip('\n')
            if not line.strip():
                if cur_start is not None and cur_end is not None and cur_lines:
                    text = ' '.join(l.strip() for l in cur_lines if l.strip())
                    text = re.sub(r"\s+", " ", text).strip()
                    if text:
                        segs.append(TranscriptSeg(start=cur_start, end=cur_end, text=text))
                cur_start = cur_end = None
                cur_lines = []
                continue

            if line.startswith('WEBVTT'):
                continue
            if '-->' in line:
                # new cue
                try:
                    left, right = line.split('-->')
                    start_s = left.strip().split()[0]
                    end_s = right.strip().split()[0]
                    cur_start = to_sec(start_s)
                    cur_end = to_sec(end_s)
                    cur_lines = []
                except Exception:
                    continue
                continue

            # ignore cue identifiers
            if cur_start is None:
                continue

            # remove vtt styling tags
            cleaned = re.sub(r"<[^>]+>", "", line)
            cur_lines.append(cleaned)

    # flush
    if cur_start is not None and cur_end is not None and cur_lines:
        text = ' '.join(l.strip() for l in cur_lines if l.strip())
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            segs.append(TranscriptSeg(start=cur_start, end=cur_end, text=text))

    return segs


def parse_transcript(cj: dict) -> List[TranscriptSeg]:
    segs: List[TranscriptSeg] = []
    for ev in cj.get("events", []) or []:
        if "segs" not in ev:
            continue
        start = float(ev.get("tStartMs", 0)) / 1000.0
        dur = float(ev.get("dDurationMs", 0)) / 1000.0
        end = start + dur
        text = "".join(s.get("utf8", "") for s in ev.get("segs", []) if isinstance(s, dict))
        text = html.unescape(text).replace("\n", " ").strip()
        if not text:
            continue
        segs.append(TranscriptSeg(start=start, end=end, text=text))
    return segs


def transcriptapi_fetch(video_url_or_id: str, api_key: str) -> Tuple[dict, List[TranscriptSeg], Optional[dict]]:
    """Fetch transcript from TranscriptAPI.

    Returns: (raw_json, segs, metadata)
    """
    url = TRANSCRIPTAPI_BASE.rstrip('/') + '/youtube/transcript'
    headers = {"Authorization": f"Bearer {api_key}", "User-Agent": "OpenClaw-IdeaVault/1.0"}
    params = {
        "video_url": video_url_or_id,
        "format": "json",
        "include_timestamp": "true",
        "include_metadata": "true",
    }
    r = requests.get(url, headers=headers, params=params, timeout=40)
    if r.status_code != 200:
        raise RuntimeError(f"TranscriptAPI error {r.status_code}: {r.text[:200]}")
    data = r.json()

    items = data.get('transcript') or []
    segs: List[TranscriptSeg] = []
    for it in items:
        try:
            text = (it.get('text') or '').strip()
            if not text:
                continue
            start = float(it.get('start') or 0.0)
            dur = float(it.get('duration') or 0.0)
            segs.append(TranscriptSeg(start=start, end=start + dur, text=text))
        except Exception:
            continue
    meta = data.get('metadata') if isinstance(data.get('metadata'), dict) else None
    return data, segs, meta


def transcriptapi_channel_latest(channel: str, api_key: str) -> dict:
    """Fetch latest channel uploads (up to 15) via TranscriptAPI's RSS-backed endpoint."""
    url = TRANSCRIPTAPI_BASE.rstrip('/') + '/youtube/channel/latest'
    headers = {"Authorization": f"Bearer {api_key}", "User-Agent": "OpenClaw-IdeaVault/1.0"}
    r = requests.get(url, headers=headers, params={"channel": channel}, timeout=40)
    if r.status_code != 200:
        raise RuntimeError(f"TranscriptAPI channel/latest error {r.status_code}: {r.text[:200]}")
    return r.json()


def build_clip(segs: List[TranscriptSeg], center_sec: int, window_sec: int) -> str:
    start = max(0, center_sec - window_sec)
    end = center_sec + window_sec
    lines: List[str] = []
    for s in segs:
        if s.end < start:
            continue
        if s.start > end:
            break
        lines.append(s.text)
    # Light cleanup: collapse spaces
    clip = re.sub(r"\s+", " ", " ".join(lines)).strip()
    return clip


def write_transcript_txt(segs: List[TranscriptSeg], out_path: str) -> None:
    ensure_dir(os.path.dirname(out_path))
    with open(out_path, "w", encoding="utf-8") as f:
        for s in segs:
            f.write(f"{hms(int(s.start))} {s.text}\n")


def which(cmd: str) -> Optional[str]:
    for p in os.environ.get('PATH', '').split(os.pathsep):
        cand = os.path.join(p, cmd)
        if os.path.isfile(cand) and os.access(cand, os.X_OK):
            return cand
    return None


def ytdlp_fetch_subtitles_vtt(video_url: str, out_dir: str, video_id: str, cookies_file: Optional[str] = None) -> str:
    """Use yt-dlp to fetch subtitles into out_dir, return path to a .vtt file.

    Requires yt-dlp to be installed. YouTube may require cookies in some environments.
    """
    # Optional explicit yt-dlp binary path, otherwise resolve from PATH.
    ytdlp = os.environ.get('IDEA_VAULT_YTDLP_BIN') or which('yt-dlp') or which('yt-dlp.py')
    if not ytdlp:
        raise RuntimeError('yt-dlp not found on PATH (or IDEA_VAULT_YTDLP_BIN unset)')

    ensure_dir(out_dir)

    out_tmpl = os.path.join(out_dir, f"{video_id}.%(language)s.%(ext)s")

    cmd = [
        ytdlp,
        '--skip-download',
        '--write-auto-subs',
        '--write-subs',
        '--sub-langs', 'en.*',
        '--sub-format', 'vtt',
        '--output', out_tmpl,
    ]

    # If supported, provide a JS runtime (helps with newer YouTube extraction flows)
    try:
        help_out = subprocess.run([ytdlp, '--help'], capture_output=True, text=True).stdout
        if '--js-runtimes' in (help_out or ''):
            node_path = shutil.which('node')
            if node_path:
                cmd[1:1] = ['--js-runtimes', f'node:{node_path}']
    except Exception:
        pass

    if cookies_file:
        cmd += ['--cookies', cookies_file]

    cmd.append(video_url)

    p = subprocess.run(cmd, cwd=out_dir, capture_output=True, text=True)
    if p.returncode != 0:
        tail = (p.stderr or p.stdout or '').strip()[-900:]
        raise RuntimeError(f"yt-dlp failed: {tail}")

    # Find the newest vtt file matching our template
    vtts = [
        os.path.join(out_dir, fn)
        for fn in os.listdir(out_dir)
        if fn.startswith(video_id + '.') and fn.endswith('.vtt')
    ]
    if not vtts:
        raise RuntimeError('yt-dlp completed but no .vtt subtitles were written')

    vtts.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return vtts[0]


# -------------------------
# Index + entry writing
# -------------------------


def load_index(index_path: str) -> dict:
    if not os.path.exists(index_path):
        return {"entries": []}
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_index(index_path: str, idx: dict) -> None:
    ensure_dir(os.path.dirname(index_path))
    tmp = index_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(idx, f, indent=2, ensure_ascii=False)
    os.replace(tmp, index_path)


def download_asset(url: str, out_path: str) -> None:
    ensure_dir(os.path.dirname(out_path))
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=60)
    r.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(r.content)


def render_entry_md(
    *,
    created_at: str,
    title: str,
    source_kind: str,
    source_url: Optional[str],
    source_author: Optional[str],
    source_id: Optional[str],
    capture_messages: List[dict],
    notes_text: str,
    timestamps: List[Timestamp],
    clips: List[dict],
    summary: str,
    elaboration: str,
    associations: List[dict],
    tags: List[str],
    assets: List[dict],
    transcript_path: Optional[str],
) -> str:
    ts_lines = "\n".join([f"- {hms(secs)} ({raw})" for secs, raw in timestamps]) if timestamps else "- (none)"

    assets_lines = "\n".join([f"- {a.get('path') or a.get('url')}" for a in assets]) if assets else "- (none)"

    clips_md = []
    for c in clips or []:
        clips_md.append(f"### {hms(int(c['center_sec']))}\n\n{c['text']}\n")

    assoc_md = []
    for a in associations or []:
        t = a.get("timestamp_sec")
        assoc_md.append(f"- {hms(int(t)) if t is not None else '(n/a)'}: {a.get('note','').strip()}")

    raw_msgs = "\n".join(
        [
            f"- {m.get('timestampUtc') or m.get('timestamp')}: {m.get('content','').strip()}"
            for m in capture_messages
        ]
    )

    tags_line = ", ".join(tags) if tags else ""

    meta_lines = [
        f"- **Saved:** {created_at}",
        f"- **Kind:** {source_kind}",
        f"- **Source:** {source_url or '(none)'}",
    ]
    if source_author:
        meta_lines.append(f"- **Author/Channel:** {source_author}")
    if source_id:
        meta_lines.append(f"- **Source ID:** {source_id}")
    if tags_line:
        meta_lines.append(f"- **Tags:** {tags_line}")
    if transcript_path:
        meta_lines.append(f"- **Transcript:** {transcript_path}")

    md = f"""# {title}

{"\n".join(meta_lines)}

## Your capture (raw)

{raw_msgs}

## Your notes (as-sent)

{notes_text.strip() or '(none)'}

## Timestamps you flagged

{ts_lines}

## Summary

{summary.strip() or '(summary pending)'}

## Elaboration (fill the gaps)

{elaboration.strip() or '(none)'}

## Clips (±60s around each timestamp)

{"\n".join(clips_md) if clips_md else "(none)"}

## Associations (why you saved it)

{"\n".join(assoc_md) if assoc_md else "(none)"}

## Assets

{assets_lines}
"""
    return md


# -------------------------
# Commands
# -------------------------


def cmd_extract(args: argparse.Namespace) -> None:
    data = json.load(sys.stdin)
    messages = data.get("messages") or data

    user_id = str(args.user_id)
    trigger_re = re.compile(r"^\s*/?vault\s*$", re.IGNORECASE)

    # Normalize order to chronological
    messages_sorted = sorted(messages, key=lambda m: int(m.get("timestampMs") or 0))

    # Find the last trigger message from user
    end_idx = None
    for i in range(len(messages_sorted) - 1, -1, -1):
        m = messages_sorted[i]
        author_id = str((m.get("author") or {}).get("id"))
        if author_id == user_id and trigger_re.match(m.get("content") or ""):
            end_idx = i
            break

    if end_idx is None:
        raise SystemExit("No /vault trigger message found in provided messages")

    # Find previous /vault (to delimit entries)
    prev_trigger_idx = None
    for i in range(end_idx - 1, -1, -1):
        m = messages_sorted[i]
        author_id = str((m.get("author") or {}).get("id"))
        if author_id == user_id and trigger_re.match(m.get("content") or ""):
            prev_trigger_idx = i
            break

    lower_bound = (prev_trigger_idx + 1) if prev_trigger_idx is not None else max(0, end_idx - int(args.fallback_messages))

    # Within the window, find the most recent URL(s)
    primary_url = None
    primary_url_idx = None
    youtube_url = None
    youtube_url_idx = None

    for i in range(end_idx - 1, lower_bound - 1, -1):
        m = messages_sorted[i]
        author_id = str((m.get("author") or {}).get("id"))
        if author_id != user_id:
            continue
        content = m.get("content") or ""

        if youtube_url is None:
            yus = find_youtube_urls(content)
            if yus:
                youtube_url = yus[-1]
                youtube_url_idx = i

        if primary_url is None:
            us = find_urls(content)
            if us:
                primary_url = us[-1]
                primary_url_idx = i

        if youtube_url is not None and primary_url is not None:
            break

    # Choose capture start: prefer YouTube URL, otherwise any URL, otherwise just the window start
    if youtube_url_idx is not None:
        start_idx = youtube_url_idx
    elif primary_url_idx is not None:
        start_idx = primary_url_idx
    else:
        start_idx = lower_bound

    capture = [
        m for m in messages_sorted[start_idx:end_idx]
        if str((m.get("author") or {}).get("id")) == user_id
    ]

    # Extract timestamps + notes + attachments
    ts: List[Timestamp] = []
    notes_parts: List[str] = []
    assets: List[dict] = []
    urls_all: List[str] = []

    # Also include time param on YouTube URL
    if youtube_url:
        t_param = parse_youtube_time_param(youtube_url)
        if t_param is not None:
            ts.append((t_param, "(from URL time param)"))

    for m in capture:
        content = (m.get("content") or "").strip()
        if content:
            urls_all.extend(find_urls(content))

            # Strip messages that are only a URL from the notes body
            only_url = False
            if primary_url and content.strip() == primary_url and len(find_urls(content)) == 1:
                only_url = True
            if not only_url:
                notes_parts.append(content)

            ts.extend(parse_timestamps_freeform(content))

        for a in m.get("attachments") or []:
            assets.append({
                "url": a.get("url") or a.get("proxy_url"),
                "filename": a.get("filename"),
                "size": a.get("size"),
                "content_type": a.get("content_type"),
            })

    # De-dupe timestamps
    seen = set()
    ts_dedup: List[Timestamp] = []
    for secs, raw in sorted(ts, key=lambda x: x[0]):
        if secs not in seen:
            seen.add(secs)
            ts_dedup.append((int(secs), raw))

    # De-dupe URLs
    urls_unique: List[str] = []
    seen_u = set()
    for u in urls_all:
        if u not in seen_u:
            seen_u.add(u)
            urls_unique.append(u)

    source_hint = "note"
    if youtube_url:
        source_hint = "youtube"
    elif primary_url:
        source_hint = "web"

    out = {
        "primary_url": primary_url,
        "youtube_url": youtube_url,
        "urls": urls_unique,
        "source_hint": source_hint,
        "timestamps": [{"sec": s, "raw": r} for s, r in ts_dedup],
        "notes_text": "\n\n".join(notes_parts).strip(),
        "capture_messages": capture,
        "assets": assets,
        "range": {
            "start_message_id": messages_sorted[start_idx].get("id"),
            "end_message_id": messages_sorted[end_idx].get("id"),
        },
    }

    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)


def cmd_fetch(args: argparse.Namespace) -> None:
    req = json.load(sys.stdin)
    url = req.get("youtube_url") or req.get("url") or req.get("primary_url")
    if not url:
        raise SystemExit("No URL provided for fetch")
    video_id = parse_video_id(url)
    if not video_id:
        raise SystemExit(f"Could not parse YouTube video id from url: {url}")

    # Metadata: try watch page first, then oEmbed fallback
    title = f"YouTube {video_id}"
    channel = ""
    pr = None
    try:
        pr = fetch_youtube_player_response(video_id)
        title = (pr.get("videoDetails") or {}).get("title") or title
        channel = (pr.get("videoDetails") or {}).get("author") or channel
    except Exception:
        pr = None

    oe = fetch_youtube_oembed(video_id)
    if oe:
        title = oe.get("title") or title
        channel = oe.get("author_name") or channel

    cache_dir = args.cache_dir
    ensure_dir(cache_dir)
    transcript_txt = os.path.join(cache_dir, f"{video_id}.transcript.txt")
    transcript_json = os.path.join(cache_dir, f"{video_id}.captions.json")

    window = int(args.window_sec)
    ts_list = [int(t["sec"]) for t in (req.get("timestamps") or [])]

    transcript_available = False
    error: Optional[str] = None
    clips: List[dict] = []

    # Optional cookies for yt-dlp fallback
    cookies_file = args.cookies_file or os.environ.get('IDEA_VAULT_YTDLP_COOKIES')

    # TranscriptAPI key (no cookies required)
    transcriptapi_key = os.environ.get('IDEA_VAULT_TRANSCRIPTAPI_KEY')

    try:
        segs: List[TranscriptSeg] = []

        # Primary: captionTracks → timedtext json3
        if pr:
            track = pick_caption_track(pr)
            if track:
                cj = fetch_caption_json(track["baseUrl"])
                segs = parse_transcript(cj)
                if segs:
                    transcript_available = True
                    write_transcript_txt(segs, transcript_txt)
                    with open(transcript_json, "w", encoding="utf-8") as f:
                        json.dump(cj, f)

        # Fallback 1: TranscriptAPI (reliable in datacenter environments)
        if not transcript_available and transcriptapi_key:
            raw, segs = None, []
            meta = None
            raw, segs, meta = transcriptapi_fetch(url, transcriptapi_key)
            if segs:
                transcript_available = True
                write_transcript_txt(segs, transcript_txt)
                with open(transcript_json, "w", encoding="utf-8") as f:
                    json.dump({"source": "transcriptapi", "raw": raw}, f)
                if meta:
                    title = meta.get('title') or title
                    channel = meta.get('author_name') or channel

        # Fallback 2: yt-dlp to VTT (may require cookies)
        if not transcript_available:
            vtt_path = ytdlp_fetch_subtitles_vtt(url, cache_dir, video_id, cookies_file=cookies_file)
            segs = parse_vtt(vtt_path)
            if not segs:
                raise RuntimeError('yt-dlp produced subtitles, but parsing yielded no text')
            transcript_available = True
            write_transcript_txt(segs, transcript_txt)
            with open(transcript_json, "w", encoding="utf-8") as f:
                json.dump({"source": "yt-dlp", "vtt": vtt_path}, f)

        if transcript_available:
            for t in ts_list:
                clips.append({
                    "center_sec": t,
                    "window_sec": window,
                    "text": build_clip(segs, t, window),
                })

    except Exception as e:
        error = str(e)
        with open(transcript_txt, "w", encoding="utf-8") as f:
            f.write("(No transcript available for this video.)\n")
        with open(transcript_json, "w", encoding="utf-8") as f:
            json.dump({"error": error}, f)

    preview_chars = int(args.preview_chars)
    with open(transcript_txt, "r", encoding="utf-8") as f:
        preview = f.read(preview_chars)

    out = {
        "url": url,
        "video_id": video_id,
        "title": title,
        "channel": channel,
        "transcript_available": transcript_available,
        "error": error,
        "transcript_txt": transcript_txt,
        "transcript_json": transcript_json,
        "clips": clips,
        "transcript_preview": preview,
    }
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)


def parse_iso_date(s: str) -> dt.datetime:
    # Accept YYYY-MM-DD or full ISO
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return dt.datetime.fromisoformat(s + "T00:00:00+00:00")
    # If timezone missing, assume UTC
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(?:\.\d+)?)?", s):
        return dt.datetime.fromisoformat(s + "+00:00")
    return dt.datetime.fromisoformat(s)


def cmd_query(args: argparse.Namespace) -> None:
    vault_dir = args.vault_dir
    index_path = os.path.join(vault_dir, "index.json")
    idx = load_index(index_path)
    entries = idx.get('entries') or []

    # Filters
    q = (args.text or '').strip().lower()
    channel_q = (args.channel or '').strip().lower()
    tag_q = (args.tag or '').strip().lower()
    kind_q = (args.kind or '').strip().lower() if getattr(args, 'kind', None) else ''
    priority_q = (args.priority or '').strip().lower() if getattr(args, 'priority', None) else ''
    starred_only = bool(getattr(args, 'starred', False))

    since_dt = parse_iso_date(args.since).astimezone(dt.timezone.utc) if args.since else None
    until_dt = parse_iso_date(args.until).astimezone(dt.timezone.utc) if args.until else None

    def matches(e: dict) -> bool:
        if since_dt or until_dt:
            try:
                created = parse_iso_date(e.get('created_at') or '').astimezone(dt.timezone.utc)
            except Exception:
                created = None
            if created is not None:
                if since_dt and created < since_dt:
                    return False
                if until_dt and created > until_dt:
                    return False

        if kind_q:
            if kind_q != (e.get('kind') or '').lower():
                return False

        if priority_q:
            if priority_q != (e.get('priority') or '').lower():
                return False

        if starred_only:
            if not bool(e.get('starred')):
                return False

        if channel_q:
            if channel_q not in (e.get('channel') or '').lower():
                return False

        if tag_q:
            tags = [t.lower() for t in (e.get('tags') or [])]
            if tag_q not in tags:
                return False

        if q:
            hay = " ".join([
                (e.get('title') or ''),
                (e.get('channel') or ''),
                (e.get('url') or ''),
                (e.get('note_preview') or ''),
            ]).lower()
            if q not in hay:
                # optional fulltext search in the markdown entry
                if args.fulltext and e.get('path') and os.path.exists(e['path']):
                    try:
                        body = open(e['path'], 'r', encoding='utf-8', errors='ignore').read().lower()
                        if q not in body:
                            return False
                    except Exception:
                        return False
                else:
                    return False

        return True

    # Sort newest first
    entries = sorted(entries, key=lambda e: e.get('created_at',''), reverse=True)
    entries = [e for e in entries if matches(e)]

    limit = int(args.limit)
    entries = entries[:limit]

    json.dump({
        'count': len(entries),
        'entries': entries,
    }, sys.stdout, indent=2, ensure_ascii=False)


def state_path(vault_dir: str, name: str) -> str:
    ensure_dir(os.path.join(vault_dir, 'state'))
    safe = slugify(name) or 'state'
    return os.path.join(vault_dir, 'state', f"{safe}.json")


def load_state(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(path: str, data: dict) -> None:
    ensure_dir(os.path.dirname(path))
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def cmd_channel_monitor(args: argparse.Namespace) -> None:
    """Return new videos since last run and update state."""
    vault_dir = args.vault_dir
    api_key = os.environ.get('IDEA_VAULT_TRANSCRIPTAPI_KEY')
    if not api_key:
        raise SystemExit('IDEA_VAULT_TRANSCRIPTAPI_KEY is not set')

    channel = args.channel or CHANNEL_HANDLE_DEFAULT
    st_path = state_path(vault_dir, args.state_name or channel)
    st = load_state(st_path)
    seen_list = st.get('seen_video_ids') or []
    seen = set(seen_list)

    data = transcriptapi_channel_latest(channel, api_key)
    results = data.get('results') or []

    # Bootstrap behavior: on first run, seed state but do NOT emit a flood of old uploads.
    if not seen_list:
        for it in results:
            vid = it.get('videoId')
            if vid:
                seen.add(vid)
        st['channel'] = channel
        st['seen_video_ids'] = list(seen)[-5000:]
        st['last_run_utc'] = utc_now_iso()
        st['bootstrapped_utc'] = st.get('bootstrapped_utc') or utc_now_iso()
        save_state(st_path, st)
        json.dump({
            'channel': channel,
            'state_path': st_path,
            'new_count': 0,
            'new_videos': [],
            'bootstrapped': True,
        }, sys.stdout, indent=2, ensure_ascii=False)
        return

    new_items = []
    for it in results:
        vid = it.get('videoId')
        if not vid:
            continue
        if vid in seen:
            continue
        new_items.append(it)

    # Update state (mark seen regardless of downstream processing; will re-run next day only if missing)
    for it in new_items:
        vid = it.get('videoId')
        if vid:
            seen.add(vid)

    st['channel'] = channel
    st['seen_video_ids'] = list(seen)[-5000:]
    st['last_run_utc'] = utc_now_iso()
    save_state(st_path, st)

    json.dump({
        'channel': channel,
        'state_path': st_path,
        'new_count': len(new_items),
        'new_videos': list(reversed(new_items)),  # oldest-first
    }, sys.stdout, indent=2, ensure_ascii=False)


def cmd_annotate(args: argparse.Namespace) -> None:
    vault_dir = args.vault_dir
    index_path = os.path.join(vault_dir, "index.json")
    idx = load_index(index_path)
    entries = idx.get('entries') or []

    # pick entry
    target = None
    if args.last:
        if entries:
            target = sorted(entries, key=lambda e: e.get('created_at',''), reverse=True)[0]
    elif args.id:
        for e in entries:
            if e.get('id') == args.id:
                target = e
                break
    elif args.path:
        for e in entries:
            if e.get('path') == args.path:
                target = e
                break

    if not target:
        raise SystemExit('No matching entry found (use --last, --id, or --path)')

    # update tags
    tags = list(target.get('tags') or [])
    add_tags = args.add_tag or []
    remove_tags = args.remove_tag or []

    def norm(t: str) -> str:
        return t.strip()

    for t in add_tags:
        t = norm(t)
        if t and t not in tags:
            tags.append(t)

    for t in remove_tags:
        t = norm(t)
        if t in tags:
            tags.remove(t)

    if args.set_tags is not None:
        tags = [norm(t) for t in args.set_tags.split(',') if norm(t)]

    target['tags'] = tags

    # starred
    if args.star is not None:
        if args.star == 'toggle':
            target['starred'] = not bool(target.get('starred'))
        else:
            target['starred'] = True if args.star == 'true' else False

    # priority
    if args.priority is not None:
        target['priority'] = args.priority

    # persist
    # de-dupe by id and replace
    new_entries = []
    for e in entries:
        if e.get('id') == target.get('id'):
            continue
        new_entries.append(e)
    new_entries.append(target)
    idx['entries'] = sorted(new_entries, key=lambda e: e.get('created_at',''), reverse=False)[-2000:]
    save_index(index_path, idx)

    json.dump({'ok': True, 'entry': target, 'index_path': index_path}, sys.stdout, indent=2, ensure_ascii=False)


def _find_existing_entry(entries: List[dict], *, kind: str, source_id: Optional[str], url: Optional[str]) -> Optional[dict]:
    kind = (kind or '').lower()
    if kind == 'youtube' and source_id:
        for e in entries:
            # new schema
            if (e.get('kind') or '').lower() == 'youtube' and (e.get('source_id') or e.get('video_id')) == source_id:
                return e
            # legacy schema
            if (e.get('video_id') == source_id) or (isinstance(e.get('id'), str) and e['id'].startswith(f"yt:{source_id}:")):
                return e
    if kind == 'web' and url:
        for e in entries:
            if (e.get('kind') or '').lower() == 'web' and (e.get('url') == url):
                return e
    return None


def find_saved_transcript_txt(vault_dir: str, video_id: str) -> Optional[str]:
    troot = os.path.join(vault_dir, 'transcripts')
    if not os.path.isdir(troot):
        return None
    # Search newest years first
    years = sorted([d for d in os.listdir(troot) if os.path.isdir(os.path.join(troot, d))], reverse=True)
    for y in years:
        cand = os.path.join(troot, y, f"{video_id}.transcript.txt")
        if os.path.exists(cand):
            return cand
        # Sometimes different naming; fall back to prefix match
        for fn in os.listdir(os.path.join(troot, y)):
            if fn.startswith(video_id) and fn.endswith('.transcript.txt'):
                return os.path.join(troot, y, fn)
    return None


def clips_from_transcript_txt(path: str, timestamps: List[int], window_sec: int = 60) -> List[dict]:
    # Parse lines like "MM:SS text" or "HH:MM:SS text"
    def to_sec(ts: str) -> int:
        parts = ts.split(':')
        if len(parts) == 2:
            m, s = map(int, parts)
            return m * 60 + s
        h, m, s = map(int, parts)
        return h * 3600 + m * 60 + s

    rows: List[Tuple[int, str]] = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            m = re.match(r'^(\d{2}:\d{2}(?::\d{2})?)\s+(.*)$', line.strip())
            if not m:
                continue
            rows.append((to_sec(m.group(1)), m.group(2)))

    clips = []
    for t in timestamps:
        start = max(0, int(t) - window_sec)
        end = int(t) + window_sec
        texts = [txt for sec, txt in rows if start <= sec <= end]
        clip = re.sub(r"\s+", " ", " ".join(texts)).strip()
        clips.append({"center_sec": int(t), "window_sec": window_sec, "text": clip})
    return clips


def _append_addendum(md_path: str, *, created_at: str, notes_text: str, timestamps: List[Timestamp], clips: List[dict], summary: str, elaboration: str, associations: List[dict]) -> None:
    ts_lines = "\n".join([f"- {hms(secs)} ({raw})" for secs, raw in timestamps]) if timestamps else "- (none)"
    clips_md = []
    for c in clips or []:
        clips_md.append(f"#### {hms(int(c['center_sec']))}\n\n{c['text']}\n")
    assoc_md = []
    for a in associations or []:
        t = a.get('timestamp_sec')
        assoc_md.append(f"- {hms(int(t)) if t is not None else '(n/a)'}: {a.get('note','').strip()}")

    block = f"""

## Addendum — {created_at}

### Notes (as-sent)

{notes_text.strip() or '(none)'}

### New timestamps

{ts_lines}

### New clips

{"\n".join(clips_md) if clips_md else "(none)"}

### Addendum summary

{summary.strip() or '(none)'}

### Addendum elaboration

{elaboration.strip() or '(none)'}

### Addendum associations

{"\n".join(assoc_md) if assoc_md else "(none)"}
"""

    with open(md_path, 'a', encoding='utf-8') as f:
        f.write(block)


def _delegate_to_save(vault_dir: str, req: dict) -> None:
    """Call the `save` subcommand in a fresh process (avoids stdin re-read issues)."""
    cmd = [sys.executable, __file__, 'save', '--vault-dir', vault_dir]
    p = subprocess.run(cmd, input=json.dumps(req).encode('utf-8'), capture_output=True)
    if p.returncode != 0:
        tail = (p.stderr or p.stdout or b'')[-1200:]
        raise SystemExit(tail.decode('utf-8', errors='ignore'))
    sys.stdout.buffer.write(p.stdout)


def cmd_upsert(args: argparse.Namespace) -> None:
    """Save or append to an existing entry if the same YouTube video/web URL already exists."""
    req = json.load(sys.stdin)
    vault_dir = args.vault_dir
    ensure_dir(vault_dir)

    created_at = req.get('created_at') or utc_now_iso()
    capture = req['capture']

    src = req.get('source')
    yt = req.get('youtube')

    if not src and yt:
        src = {
            'kind': 'youtube',
            'url': (capture.get('youtube_url') or capture.get('primary_url') or capture.get('url')),
            'title': yt.get('title'),
            'author': yt.get('channel') or yt.get('author_name') or '',
            'id': yt.get('video_id'),
            'transcript_txt': yt.get('transcript_txt'),
            'transcript_json': yt.get('transcript_json'),
            'clips': yt.get('clips') or [],
        }

    if not src:
        hint = capture.get('source_hint')
        kind = hint if hint in ('youtube', 'web', 'note') else ('web' if capture.get('primary_url') else 'note')
        src = {
            'kind': kind,
            'url': capture.get('primary_url'),
            'title': None,
            'author': None,
            'id': None,
            'clips': [],
        }

    kind = (src.get('kind') or 'note').lower()
    url = src.get('url')
    source_id = src.get('id')

    # Only upsert for youtube/web. Notes always create a new entry.
    if kind not in ('youtube', 'web'):
        _delegate_to_save(vault_dir, req)
        return

    index_path = os.path.join(vault_dir, 'index.json')
    idx = load_index(index_path)
    entries = idx.get('entries') or []

    existing = _find_existing_entry(entries, kind=kind, source_id=source_id, url=url)
    if not existing:
        _delegate_to_save(vault_dir, req)
        return

    # Append addendum
    notes_text_full = (capture.get('notes_text') or '').strip()
    timestamps = [(t["sec"], t["raw"]) for t in (capture.get("timestamps") or [])]
    clips = src.get('clips') or []
    summary = req.get('summary') or ''
    elaboration = req.get('elaboration') or ''
    associations = req.get('associations') or []

    md_path = existing.get('path')
    if not md_path or not os.path.exists(md_path):
        # If the old file went missing, just save new.
        _delegate_to_save(vault_dir, req)
        return

    _append_addendum(md_path, created_at=created_at, notes_text=notes_text_full, timestamps=timestamps, clips=clips, summary=summary, elaboration=elaboration, associations=associations)

    # Update index entry (tags union + note preview + timestamps union + updated_at)
    tags = list(existing.get('tags') or [])
    for t in (req.get('tags') or []):
        if t and t not in tags:
            tags.append(t)
    existing['tags'] = tags

    note_preview = re.sub(r"\s+", " ", notes_text_full).strip()
    if len(note_preview) > 280:
        note_preview = note_preview[:280] + '…'
    existing['note_preview'] = note_preview or existing.get('note_preview')

    ts_existing = set(existing.get('timestamps') or [])
    for s, _ in timestamps:
        ts_existing.add(int(s))
    existing['timestamps'] = sorted(ts_existing)

    existing['updated_at'] = created_at

    # Persist index
    new_entries = []
    for e in entries:
        if e.get('id') == existing.get('id'):
            continue
        new_entries.append(e)
    new_entries.append(existing)
    idx['entries'] = sorted(new_entries, key=lambda e: e.get('created_at',''), reverse=False)[-2000:]
    save_index(index_path, idx)

    json.dump({'ok': True, 'mode': 'append', 'entry_path': md_path, 'entry': existing, 'index_path': index_path}, sys.stdout, indent=2, ensure_ascii=False)


def cmd_save(args: argparse.Namespace) -> None:
    req = json.load(sys.stdin)

    vault_dir = args.vault_dir
    ensure_dir(vault_dir)

    created_at = req.get("created_at") or utc_now_iso()

    capture = req["capture"]

    # New shape: req["source"]. Back-compat: req["youtube"].
    src = req.get('source')
    yt = req.get('youtube')

    # Determine source kind/url/title/author/id
    if not src and yt:
        src = {
            'kind': 'youtube',
            'url': (capture.get('youtube_url') or capture.get('primary_url') or capture.get('url')),
            'title': yt.get('title'),
            'author': yt.get('channel') or yt.get('author_name') or '',
            'id': yt.get('video_id'),
            'transcript_txt': yt.get('transcript_txt'),
            'transcript_json': yt.get('transcript_json'),
            'clips': yt.get('clips') or [],
        }

    if not src:
        hint = capture.get('source_hint')
        kind = hint if hint in ('youtube', 'web', 'note') else ('web' if capture.get('primary_url') else 'note')
        src = {
            'kind': kind,
            'url': capture.get('primary_url'),
            'title': None,
            'author': None,
            'id': None,
            'clips': [],
        }

    source_kind = (src.get('kind') or 'note').strip().lower()
    source_url = src.get('url')
    source_author = src.get('author') or ''
    source_id = src.get('id')

    timestamps = [(t["sec"], t["raw"]) for t in (capture.get("timestamps") or [])]
    clips = src.get('clips') or req.get('clips') or []

    notes_text_full = (capture.get('notes_text') or '').strip()

    # Title fallback
    title = (src.get('title') or '').strip()
    if not title:
        first_line = ''
        for line in notes_text_full.splitlines():
            if line.strip():
                first_line = line.strip()
                break
        if first_line:
            title = first_line
        elif source_url:
            title = f"Link: {source_url}"
        else:
            title = "Vault note"

    summary = req.get("summary") or ""
    elaboration = req.get('elaboration') or ""
    tags = req.get("tags") or []
    associations = req.get("associations") or []

    # Move transcript (if present) to transcripts/YYYY
    year = dt.datetime.now(dt.timezone.utc).strftime("%Y")
    transcript_txt_dst = None
    transcript_json_dst = None
    transcript_path_for_md = None

    transcript_txt_src = src.get('transcript_txt')
    transcript_json_src = src.get('transcript_json')

    if transcript_txt_src and transcript_json_src and os.path.exists(transcript_txt_src) and os.path.exists(transcript_json_src):
        transcripts_dir = os.path.join(vault_dir, "transcripts", year)
        ensure_dir(transcripts_dir)
        transcript_txt_dst = os.path.join(transcripts_dir, os.path.basename(transcript_txt_src))
        transcript_json_dst = os.path.join(transcripts_dir, os.path.basename(transcript_json_src))
        shutil.copy2(transcript_txt_src, transcript_txt_dst)
        shutil.copy2(transcript_json_src, transcript_json_dst)
        transcript_path_for_md = transcript_txt_dst

    # Download assets (attachments) into assets/YYYY/MM
    assets_out: List[dict] = []
    assets = capture.get("assets") or []
    if assets:
        mm = dt.datetime.now(dt.timezone.utc).strftime("%m")
        assets_dir = os.path.join(vault_dir, "assets", year, mm)
        ensure_dir(assets_dir)
        for a in assets:
            url_a = a.get("url")
            if not url_a:
                continue
            fn = a.get("filename") or slugify(url_a.split("/")[-1])
            out_path = os.path.join(assets_dir, fn)
            try:
                download_asset(url_a, out_path)
                assets_out.append({"url": url_a, "path": out_path, "filename": fn})
            except Exception as e:
                assets_out.append({"url": url_a, "error": str(e), "filename": fn})

    # Write entry
    date_prefix = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    entries_dir = os.path.join(vault_dir, "entries", year)
    ensure_dir(entries_dir)

    entry_slug = slugify(title)
    suffix = None
    if source_kind == 'youtube' and source_id:
        suffix = source_id
    elif source_url:
        suffix = slugify(source_url)[:24]

    fname = f"{date_prefix}__{entry_slug}" if entry_slug else date_prefix
    if suffix:
        fname += f"__{suffix}"
    entry_path = os.path.join(entries_dir, f"{fname}.md")

    md = render_entry_md(
        created_at=created_at,
        title=title,
        source_kind=source_kind,
        source_url=source_url,
        source_author=source_author or None,
        source_id=source_id,
        capture_messages=capture.get("capture_messages") or [],
        notes_text=notes_text_full,
        timestamps=timestamps,
        clips=clips,
        summary=summary,
        elaboration=elaboration,
        associations=associations,
        tags=tags,
        assets=assets_out,
        transcript_path=transcript_path_for_md,
    )

    with open(entry_path, "w", encoding="utf-8") as f:
        f.write(md)

    # Update index
    index_path = os.path.join(vault_dir, "index.json")
    idx = load_index(index_path)
    entries = idx.get("entries") or []

    note_preview = re.sub(r"\s+", " ", notes_text_full).strip()
    if len(note_preview) > 280:
        note_preview = note_preview[:280] + '…'

    if source_kind == 'youtube' and source_id:
        entry_id = f"yt:{source_id}:{created_at}"
    elif source_kind == 'web' and source_url:
        entry_id = f"web:{slugify(source_url)[:24]}:{created_at}"
    else:
        entry_id = f"note:{created_at}"

    entry_meta = {
        "id": entry_id,
        "created_at": created_at,
        "kind": source_kind,
        "title": title,
        "channel": source_author or "",
        "url": source_url,
        "source_id": source_id,
        "path": entry_path,
        "tags": tags,
        "timestamps": [s for s, _ in timestamps],
        "note_preview": note_preview,
    }

    # De-dupe index on id/path
    entries = [
        e for e in entries
        if e.get('id') != entry_meta['id'] and e.get('path') != entry_meta['path']
    ]
    entries.append(entry_meta)
    idx["entries"] = entries[-2000:]  # cap
    save_index(index_path, idx)

    out = {
        "entry_path": entry_path,
        "index_path": index_path,
        "entry": entry_meta,
        "assets": assets_out,
        "transcript_txt": transcript_txt_dst,
    }
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_extract = sub.add_parser("extract")
    ap_extract.add_argument("--user-id", required=True)
    ap_extract.add_argument("--fallback-messages", type=int, default=30, help="If no previous /vault found, capture last N messages")
    ap_extract.set_defaults(func=cmd_extract)

    ap_fetch = sub.add_parser("fetch")
    ap_fetch.add_argument("--cache-dir", required=True)
    ap_fetch.add_argument("--window-sec", type=int, default=60)
    ap_fetch.add_argument("--preview-chars", type=int, default=60000)
    ap_fetch.add_argument("--cookies-file", default=None, help="Optional cookies.txt path for yt-dlp fallback")
    ap_fetch.set_defaults(func=cmd_fetch)

    ap_query = sub.add_parser('query')
    ap_query.add_argument('--vault-dir', required=True)
    ap_query.add_argument('--limit', type=int, default=50)
    ap_query.add_argument('--since', default=None, help='ISO timestamp or YYYY-MM-DD (UTC assumed if tz missing)')
    ap_query.add_argument('--until', default=None, help='ISO timestamp or YYYY-MM-DD (UTC assumed if tz missing)')
    ap_query.add_argument('--channel', default=None, help='Filter by channel/author substring')
    ap_query.add_argument('--tag', default=None, help='Filter by exact tag')
    ap_query.add_argument('--kind', default=None, help='Filter by kind (youtube|web|note)')
    ap_query.add_argument('--priority', default=None, help='Filter by priority (e.g. high|med|low)')
    ap_query.add_argument('--starred', action='store_true', help='Only starred entries')
    ap_query.add_argument('--text', default=None, help='Substring search (title/channel/url/note_preview)')
    ap_query.add_argument('--fulltext', action='store_true', help='Also search within entry markdown file')
    ap_query.set_defaults(func=cmd_query)

    ap_annotate = sub.add_parser('annotate')
    ap_annotate.add_argument('--vault-dir', required=True)
    ap_annotate.add_argument('--last', action='store_true', help='Annotate the newest entry')
    ap_annotate.add_argument('--id', default=None, help='Entry id from index.json')
    ap_annotate.add_argument('--path', default=None, help='Entry path')
    ap_annotate.add_argument('--add-tag', action='append', default=None)
    ap_annotate.add_argument('--remove-tag', action='append', default=None)
    ap_annotate.add_argument('--set-tags', default=None, help='Comma-separated tags (overwrites)')
    ap_annotate.add_argument('--star', choices=['true','false','toggle'], default=None)
    ap_annotate.add_argument('--priority', default=None)
    ap_annotate.set_defaults(func=cmd_annotate)

    ap_monitor = sub.add_parser('channel-monitor')
    ap_monitor.add_argument('--vault-dir', required=True)
    ap_monitor.add_argument('--channel', default=None, help='@handle, channel URL, or UC... channel ID')
    ap_monitor.add_argument('--state-name', default='channel-monitor', help='State file name (default: channel-monitor)')
    ap_monitor.set_defaults(func=cmd_channel_monitor)

    ap_upsert = sub.add_parser('upsert')
    ap_upsert.add_argument('--vault-dir', required=True)
    ap_upsert.set_defaults(func=cmd_upsert)

    ap_save = sub.add_parser("save")
    ap_save.add_argument("--vault-dir", required=True)
    ap_save.set_defaults(func=cmd_save)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
