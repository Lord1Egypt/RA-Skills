#!/usr/bin/env python3
"""Shared helpers for the long-video pipeline (standard library only)."""
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

UA = "long-video-generation-skill/1.0"
STATS = {"network": 0, "cached": 0}
ALLOWED_FPS = (24, 25, 30, 50, 60)
SUBDIRS = ("research", "assets", "audio", "build", "out", "cache")
ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")
SAMPLE_RATE = 48000


class Fail(RuntimeError):
    """A problem the user can act on; scripts print it without a traceback."""


# --------------------------------------------------------------------------
# processes
# --------------------------------------------------------------------------
def need_tool(name, hint=""):
    p = shutil.which(name)
    if not p:
        raise Fail(f"'{name}' was not found on PATH. {hint}".strip())
    return p


def run(cmd, cwd=None, input_text=None, timeout=None):
    cmd = [str(c) for c in cmd]
    try:
        r = subprocess.run(cmd, cwd=cwd, input=input_text, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
    except FileNotFoundError:
        raise Fail(f"Command not found: {cmd[0]}") from None
    except subprocess.TimeoutExpired:
        raise Fail(f"{Path(cmd[0]).name} timed out after {timeout}s.") from None
    if r.returncode != 0:
        tail = (r.stderr or r.stdout or "").strip().splitlines()[-12:]
        raise Fail(f"{Path(cmd[0]).name} failed (exit {r.returncode}):\n" + "\n".join(tail))
    return r


def ffmpeg(args, cwd=None):
    need_tool("ffmpeg", "Install FFmpeg (version 5 or newer) from ffmpeg.org or your package manager.")
    return run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"] + [str(a) for a in args], cwd=cwd)


def probe(path):
    need_tool("ffprobe", "Install FFmpeg (it includes ffprobe).")
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height",
             "-of", "json", path])
    try:
        data = json.loads(r.stdout or "{}")
    except ValueError:
        data = {}
    streams = data.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), None)
    a = next((s for s in streams if s.get("codec_type") == "audio"), None)
    try:
        dur = float((data.get("format") or {}).get("duration") or 0)
    except ValueError:
        dur = 0.0
    return {"duration": dur, "width": (v or {}).get("width"), "height": (v or {}).get("height"),
            "has_video": v is not None, "has_audio": a is not None}


# --------------------------------------------------------------------------
# project file
# --------------------------------------------------------------------------
def ensure_dirs(d):
    for s in SUBDIRS:
        (Path(d) / s).mkdir(parents=True, exist_ok=True)


def load_project(d):
    p = Path(d) / "project.json"
    if not p.exists():
        raise Fail(f"No project.json in {d}. Create one with: python scripts/project.py init {d} --title \"...\"")
    try:
        data = json.loads(p.read_text(encoding="utf-8-sig"))
    except ValueError as e:
        raise Fail(f"project.json is not valid JSON: {e}") from None
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise Fail("project.json needs a non-empty 'scenes' list.")
    seen = set()
    for i, s in enumerate(scenes, 1):
        if not isinstance(s, dict) or not ID_RE.match(str(s.get("id", ""))):
            raise Fail(f"Scene {i} needs an 'id' made of letters, digits, '-' or '_'.")
        if s["id"] in seen:
            raise Fail(f"Duplicate scene id '{s['id']}'.")
        seen.add(s["id"])
    try:
        fps = int(data.get("fps", 30))
    except (TypeError, ValueError):
        fps = 0
    if fps not in ALLOWED_FPS:
        raise Fail(f"fps must be one of {ALLOWED_FPS} (whole frame rates keep audio sample-aligned).")
    data["fps"] = fps
    data.setdefault("resolution", "1920x1080")
    data.setdefault("wpm", 150)
    data.setdefault("shot_seconds", 6)
    return data


def save_project(d, data):
    p = Path(d) / "project.json"
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, p)


def parse_resolution(text):
    m = re.fullmatch(r"(\d{3,5})x(\d{3,5})", str(text))
    if not m:
        raise Fail(f"Bad resolution '{text}'; use WIDTHxHEIGHT, e.g. 1920x1080.")
    w, h = int(m.group(1)), int(m.group(2))
    if w % 2 or h % 2:
        raise Fail("Resolution width and height must be even numbers.")
    return w, h


def timeline(project):
    """Scenes with frame-aligned start and duration (so audio and video never drift)."""
    fps = int(project["fps"])
    t, rows = 0.0, []
    for s in project["scenes"]:
        d = s.get("audio_duration")
        if not isinstance(d, (int, float)) or d <= 0:
            raise Fail(f"Scene '{s['id']}' has no audio_duration. Run scripts/voiceover.py first.")
        frames = max(1, math.ceil(d * fps - 1e-6))
        dur = frames / fps
        rows.append({"scene": s, "start": t, "dur": dur, "frames": frames, "raw": float(d)})
        t += dur
    return rows, t


def words(text):
    return re.findall(r"[^\W_]+(?:['’][^\W_]+)*", text or "", re.UNICODE)


def est_seconds(text, wpm):
    return len(words(text)) * 60.0 / max(wpm, 60)


def sha(obj):
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:16]


def slug(text, n=40):
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")[:n] or "x"


def fmt_clock(sec):
    s = int(round(sec))
    h, r = divmod(s, 3600)
    m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def fmt_srt(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# --------------------------------------------------------------------------
# network
# --------------------------------------------------------------------------
def is_cached(url, cache_dir, ttl=86400):
    """True when http_json would answer this URL from the on-disk cache (no network request)."""
    if not cache_dir:
        return False
    cp = Path(cache_dir) / (hashlib.sha1(url.encode("utf-8")).hexdigest() + ".json")
    return cp.exists() and time.time() - cp.stat().st_mtime < ttl


def http_json(url, headers=None, cache_dir=None, ttl=86400, timeout=30, retries=2):
    """GET JSON with an on-disk cache. Never prints the URL (it can contain an API key)."""
    cp = None
    if cache_dir:
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        cp = Path(cache_dir) / (hashlib.sha1(url.encode("utf-8")).hexdigest() + ".json")
        if cp.exists() and time.time() - cp.stat().st_mtime < ttl:
            try:
                obj = json.loads(cp.read_text(encoding="utf-8"))
                STATS["cached"] += 1
                return obj["body"], obj.get("headers", {})
            except (ValueError, KeyError):
                pass
    host = urllib.parse.urlsplit(url).netloc
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json", **(headers or {})})
    body, hdrs = None, {}
    for attempt in range(retries + 1):
        try:
            STATS["network"] += 1
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = json.loads(r.read().decode("utf-8", "replace"))
                hdrs = {k.lower(): v for k, v in r.headers.items()}
            break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                raise Fail(f"{host}: HTTP 429, rate limit reached. Wait, then rerun; cached results are reused.") from None
            if e.code in (401, 403):
                raise Fail(f"{host}: HTTP {e.code}, the API refused the request. Check the API key.") from None
            if e.code >= 500 and attempt < retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise Fail(f"{host}: HTTP {e.code}.") from None
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if attempt < retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise Fail(f"Cannot reach {host} ({getattr(e, 'reason', e)}). If you are in a sandbox, outbound access "
                       "may be blocked; run this step on your own machine.") from None
        except ValueError:
            raise Fail(f"{host} returned something that is not JSON.") from None
    if cp is not None and body is not None:
        cp.write_text(json.dumps({"body": body, "headers": hdrs}, ensure_ascii=False), encoding="utf-8")
    return body, hdrs


def http_bytes(url, headers=None, data=None, timeout=120):
    host = urllib.parse.urlsplit(url).netloc
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **(headers or {})})
    try:
        STATS["network"] += 1
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", "replace")[:300]
        except OSError:
            pass
        raise Fail(f"{host}: HTTP {e.code}. {detail}".strip()) from None
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise Fail(f"Cannot reach {host} ({getattr(e, 'reason', e)}).") from None


def download(url, dest, headers=None, timeout=90, max_mb=1500):
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")
    host = urllib.parse.urlsplit(url).netloc
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    try:
        STATS["network"] += 1
        total = 0
        with urllib.request.urlopen(req, timeout=timeout) as r, open(tmp, "wb") as f:
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_mb * (1 << 20):
                    raise Fail(f"{host}: file is larger than {max_mb} MB; skipped.")
                f.write(chunk)
    except urllib.error.HTTPError as e:
        tmp.unlink(missing_ok=True)
        raise Fail(f"{host}: HTTP {e.code} while downloading.") from None
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        tmp.unlink(missing_ok=True)
        raise Fail(f"Cannot download from {host} ({getattr(e, 'reason', e)}).") from None
    except Fail:
        tmp.unlink(missing_ok=True)
        raise
    os.replace(tmp, dest)
    return dest


# --------------------------------------------------------------------------
# fonts and filter paths
# --------------------------------------------------------------------------
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def find_font(explicit=None):
    if explicit:
        return explicit if Path(explicit).exists() else None
    for c in FONT_CANDIDATES:
        if Path(c).exists():
            return c
    if shutil.which("fc-match"):
        try:
            out = subprocess.run(["fc-match", "-f", "%{file}", "sans:bold"], capture_output=True, text=True,
                                 timeout=10).stdout.strip()
            if out and Path(out).exists():
                return out
        except (OSError, subprocess.SubprocessError):
            pass
    return None


def esc_filter_path(p):
    """Escape a path for use inside an ffmpeg filter option."""
    return str(p).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")


def has_rtl(text):
    return bool(re.search(r"[\u0590-\u08FF\uFB1D-\uFDFF\uFE70-\uFEFF]", text or ""))
