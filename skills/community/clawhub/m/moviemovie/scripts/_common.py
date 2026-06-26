"""Shared constants and helpers for moviemovie scripts."""

import json
import os
import platform
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# ---------------------------------------------------------------------------
# Trackers (for building magnet links from info_hash)
# ---------------------------------------------------------------------------
TRACKERS = [
    "udp://tracker.opentrackr.org:1337",
    "udp://open.stealth.si:80/announce",
    "udp://tracker.torrent.eu.org:451",
    "udp://open.demonii.com:1337/announce",
    "udp://tracker.openbittorrent.com:6969/announce",
]

# ---------------------------------------------------------------------------
# API URLs
# ---------------------------------------------------------------------------
APIBAY_API = "https://apibay.org"
BITSEARCH_URL = "https://bitsearch.to"
TORRENTDL_URL = "https://www.torrentdownload.info"
YTS_DOMAINS = [
    "https://yts.mx/api/v2",
    "https://yts.torrentbay.st/api/v2",
]
TORRENTCLAW_API = "https://torrentclaw.com/api/v1"

# apibay category codes
CAT_MOVIES_HD = "207"
CAT_MOVIES_ALL = "201"

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

# ---------------------------------------------------------------------------
# Skill root discovery (multi-platform)
# ---------------------------------------------------------------------------
SEARCH_DIRS = [
    os.environ.get("CLAUDE_PLUGIN_ROOT", ""),
    os.environ.get("CLAUDE_SKILL_DIR", ""),
    os.environ.get("OPENCLAW_SKILL_ROOT", ""),
    os.environ.get("GEMINI_EXTENSION_DIR", ""),
    os.path.expanduser("~/.claude/skills/moviemovie"),
    os.path.expanduser("~/.agents/skills/moviemovie"),
]


def find_skill_root():
    """Find the moviemovie skill installation directory."""
    # Check if we're running from the scripts/ dir already
    here = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(here)
    if os.path.isfile(os.path.join(parent, "SKILL.md")):
        return parent
    for d in SEARCH_DIRS:
        if d and os.path.isfile(os.path.join(d, "SKILL.md")):
            return d
    return None


# ---------------------------------------------------------------------------
# HTTP helpers (stdlib only, with retry + exponential backoff)
# ---------------------------------------------------------------------------
def http_get(url, headers=None, timeout=10, retries=3):
    """HTTP GET with retry and exponential backoff. Returns bytes or None."""
    hdrs = {"User-Agent": BROWSER_UA}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except Exception:
            if attempt < retries - 1:
                time.sleep(1.5 ** attempt)
    return None


def http_get_json(url, headers=None, timeout=10, retries=3):
    """HTTP GET and parse JSON. Returns dict/list or None."""
    raw = http_get(url, headers=headers, timeout=timeout, retries=retries)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Magnet link builder
# ---------------------------------------------------------------------------
def build_magnet(info_hash, name="", trackers=None):
    """Build a full magnet link from info_hash."""
    if trackers is None:
        trackers = TRACKERS
    h = info_hash.upper().strip()
    dn = urllib.parse.quote(name) if name else ""
    parts = [f"magnet:?xt=urn:btih:{h}"]
    if dn:
        parts.append(f"dn={dn}")
    for t in trackers:
        parts.append(f"tr={urllib.parse.quote(t)}")
    return "&".join(parts)


# ---------------------------------------------------------------------------
# Torrent result data structure
# ---------------------------------------------------------------------------
def make_result(info_hash, name, size_bytes=0, seeders=0, leechers=0,
                source="", magnet="", imdb=""):
    """Create a standardized torrent result dict."""
    h = info_hash.upper().strip()
    if not magnet:
        magnet = build_magnet(h, name)
    size_gb = round(size_bytes / (1024 ** 3), 2) if size_bytes else 0
    quality = parse_quality(name)
    return {
        "info_hash": h,
        "name": name,
        "size_bytes": int(size_bytes),
        "size_gb": size_gb,
        "seeders": int(seeders),
        "leechers": int(leechers),
        "quality": quality,
        "source": source,
        "magnet": magnet,
        "imdb": imdb,
    }


# ---------------------------------------------------------------------------
# Quality / filename parser
# ---------------------------------------------------------------------------
def parse_quality(name):
    """Parse quality info from torrent filename."""
    n = name.upper()
    info = {}

    # Resolution
    if "2160P" in n or "4K" in n or "UHD" in n:
        info["resolution"] = "2160p"
    elif "1080P" in n:
        info["resolution"] = "1080p"
    elif "720P" in n:
        info["resolution"] = "720p"
    elif "480P" in n:
        info["resolution"] = "480p"
    else:
        info["resolution"] = "unknown"

    # Source
    for tag, label in [
        ("BLURAY", "BluRay"), ("BLU-RAY", "BluRay"), ("BDRIP", "BluRay"),
        ("REMUX", "Remux"), ("WEB-DL", "WEB-DL"), ("WEBDL", "WEB-DL"),
        ("WEBRIP", "WEBRip"), ("WEB", "WEB"), ("HDCAM", "CAM"),
        ("HDTS", "TS"), ("TELESYNC", "TS"), ("TS", "TS"), ("CAM", "CAM"),
    ]:
        if tag in n:
            info["source"] = label
            break
    else:
        info["source"] = "unknown"

    # Codec
    for tag, label in [
        ("X265", "x265"), ("H265", "x265"), ("H.265", "x265"), ("HEVC", "x265"),
        ("AV1", "AV1"),
        ("X264", "x264"), ("H264", "x264"), ("H.264", "x264"), ("AVC", "x264"),
    ]:
        if tag in n:
            info["codec"] = label
            break

    # HDR
    for tag in ["DOLBY VISION", "DV", "HDR10+", "HDR10", "HDR"]:
        if tag in n:
            info["hdr"] = tag
            break

    # Audio
    for tag in ["ATMOS", "DTS-HD", "DTS", "TRUEHD", "DD5.1", "AAC", "AC3"]:
        if tag in n:
            info["audio"] = tag
            break

    return info


# ---------------------------------------------------------------------------
# Size tier classification
# ---------------------------------------------------------------------------
def classify_size_tier(size_gb):
    """Classify a torrent into size tier for Top 3 recommendation."""
    if size_gb <= 0:
        return "unknown"
    if 1.0 <= size_gb <= 3.0:
        return "light"      # 📱 轻量版
    elif 3.0 < size_gb <= 5.0:
        return "balanced"   # ⚖️ 均衡版
    elif 10.0 <= size_gb <= 30.0:
        return "premium"    # 🖥️ 发烧版
    elif 5.0 < size_gb < 10.0:
        return "mid"
    else:
        return "other"


def pick_top3(results):
    """Pick Top 3 torrents from different size tiers, preferring 4K."""
    tiers = {"light": [], "balanced": [], "premium": []}
    for r in results:
        tier = classify_size_tier(r["size_gb"])
        if tier in tiers:
            tiers[tier].append(r)

    top3 = []
    labels = [
        ("light", "📱 轻量版 (1-3GB)", "手机/平板/快速下载"),
        ("premium", "🖥️ 发烧版 (10-30GB)", "家庭影院/大屏/收藏"),
        ("balanced", "⚖️ 均衡版 (3-5GB)", "高清观看+合理空间"),
    ]
    for tier_key, label, desc in labels:
        candidates = tiers[tier_key]
        if not candidates:
            continue
        # Prefer 4K, then most seeds
        candidates.sort(key=lambda x: (
            x["quality"].get("resolution", "") == "2160p",
            x["seeders"],
        ), reverse=True)
        best = candidates[0]
        top3.append({**best, "tier_label": label, "tier_desc": desc})

    return top3


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------
def dedupe_results(results):
    """Deduplicate by info_hash, keeping the one with most seeders."""
    seen = {}
    for r in results:
        h = r["info_hash"]
        if h not in seen or r["seeders"] > seen[h]["seeders"]:
            seen[h] = r
    return list(seen.values())


# ---------------------------------------------------------------------------
# Pretty output
# ---------------------------------------------------------------------------
def ok(msg):
    print(f"  \033[32m✅ {msg}\033[0m")

def fail(msg):
    print(f"  \033[31m❌ {msg}\033[0m")

def info(msg):
    print(f"  \033[36mℹ️  {msg}\033[0m")

def warn(msg):
    print(f"  \033[33m⚠️  {msg}\033[0m")
