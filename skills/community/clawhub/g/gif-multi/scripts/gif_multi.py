#!/usr/bin/env python3
"""Giphy Multi — Search Giphy and convert GIFs per messaging platform.

Usage:
  python3 gif_multi.py --discover                # Scan active channels
  python3 gif_multi.py "<query>" --channel <ch>  # Search + convert
  python3 gif_multi.py --mode <natural|on_request>
  python3 gif_multi.py --check                   # Verify setup
"""
import argparse, json, os, subprocess, sys, time, urllib.request, urllib.parse

# ──── Channel profiles ────────────────────────────────────────────────
CHANNEL_PROFILES = {
    # Standard MP4 (H.264 yuv420p) — works on most platforms
    "telegram":   {"format": "mp4",  "max_bytes": 50_000_000},
    "signal":     {"format": "mp4",  "max_bytes": 50_000_000},
    "imessage":   {"format": "mp4",  "max_bytes": 50_000_000},
    "matrix":     {"format": "mp4",  "max_bytes": 50_000_000},
    "line":       {"format": "mp4",  "max_bytes": 50_000_000},
    "zalo":       {"format": "mp4",  "max_bytes": 50_000_000},
    "msteams":    {"format": "mp4",  "max_bytes": 50_000_000},
    "googlechat": {"format": "mp4",  "max_bytes": 50_000_000},
    "feishu":     {"format": "mp4",  "max_bytes": 50_000_000},
    "nextcloud-talk": {"format": "mp4", "max_bytes": 50_000_000},
    "synology-chat":  {"format": "mp4", "max_bytes": 50_000_000},
    "tlon":       {"format": "mp4",  "max_bytes": 50_000_000},
    # WhatsApp — specific profile
    "whatsapp":   {"format": "mp4_whatsapp", "max_bytes": 16_000_000},
    # Discord — plan limits
    "discord":    {"format": "mp4_discord",  "max_bytes": 25_000_000},
    # Slack — prefers small sizes
    "slack":      {"format": "gif_optimized", "max_bytes": 5_000_000},
    # Channels without media support
    "irc":        {"format": "text_only"},
    "nostr":      {"format": "text_only"},
    "twitch":     {"format": "text_only"},
    "clickclack": {"format": "text_only"},
}

# ──── Helpers ──────────────────────────────────────────────────────────

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")

SETUP_HELP = """
━━━ Giphy API Key ━━━

1. Go to https://developers.giphy.com → "Create an App"
2. Select "API" (free, 1,000 requests/day)
3. Copy your API Key

4. Add it to your config (openclaw.json):
   { "skills": { "entries": { "gif-multi": { "env": { "GIPHY_API_KEY": "your_key" } } } } }

   Or add it to ~/.openclaw/.env:
   echo 'GIPHY_API_KEY=your_key' >> ~/.openclaw/.env

   Or set as an environment variable:
   export GIPHY_API_KEY=your_key
━━━━━━━━━━━━━━━━━━━━
"""


def get_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return None


def save_config(cfg, path=None):
    path = path or CONFIG_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)
    return path


def _cleanup_source(path):
    """Delete source GIF after conversion."""
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except OSError:
        pass


def _purge_old(out_dir, max_age=600):
    """Delete cached files older than max_age seconds (default 10 min)."""
    now = time.time()
    try:
        if os.path.exists(out_dir):
            for f in os.listdir(out_dir):
                fp = os.path.join(out_dir, f)
                if os.path.isfile(fp) and (now - os.path.getmtime(fp)) > max_age:
                    os.remove(fp)
    except OSError:
        pass


def get_api_key():
    api_key = os.environ.get("GIPHY_API_KEY", "")
    if api_key:
        return api_key
    # Fallback: read OpenClaw .env directly (when skills.entries.*.env is not set)
    env_path = os.path.expanduser("~/.openclaw/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("GIPHY_API_KEY="):
                    return line.split("=", 1)[1].strip().strip("\"'")
    return None


# ──── Check ────────────────────────────────────────────────────────────

def run_check():
    """Verify everything is configured correctly."""
    issues = []

    # API key
    key = get_api_key()
    if key:
        masked = key[:4] + "…" + key[-4:] if len(key) > 8 else "***"
        print(f"✅ GIPHY_API_KEY: {masked}")
    else:
        issues.append("❌ GIPHY_API_KEY not found")
        print(SETUP_HELP)

    # openclaw CLI
    r = subprocess.run(["openclaw", "--version"], capture_output=True, text=True, timeout=10)
    if r.returncode == 0:
        print(f"✅ OpenClaw: {r.stdout.strip()}")
    else:
        issues.append("❌ openclaw CLI is not available")

    # bins requeridos
    for bin_name in ("python3", "ffmpeg", "curl"):
        r = subprocess.run(["which", bin_name], capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            print(f"✅ {bin_name}")
        else:
            issues.append(f"❌ {bin_name} is not available in PATH")

    # Active channels
    config = get_config()
    if config and config.get("channels"):
        chs = ", ".join(config["channels"].keys())
        print(f"✅ Active channels: {chs}")
        print(f"✅ Mode: {config.get('mode', 'natural')}")
    else:
        print("ℹ️  Run --discover to detect active channels")

    if issues:
        print(f"\n⚠️  {len(issues)} issue(s) found:")
        for i in issues:
            print(f"   {i}")
    else:
        print("\n✨ All set. Enjoy your GIFs!")


# ──── Discovery ──────────────────────────────────────────────────────────

def discover_channels():
    """Run `openclaw plugins list --json` and extract active channels."""
    result = subprocess.run(
        ["openclaw", "plugins", "list", "--json"],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode != 0:
        print(json.dumps({"error": f"openclaw CLI failed: {result.stderr.strip()}"}))
        sys.exit(1)

    try:
        raw = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON parse error: {e}"}))
        sys.exit(1)

    plugins = raw if isinstance(raw, list) else raw.get("plugins", [])

    active = {}
    for p in plugins:
        if p.get("channelIds") and p.get("enabled") is True:
            cid = p["channelIds"][0]
            profile = CHANNEL_PROFILES.get(cid, {"format": "mp4", "max_bytes": 50_000_000})
            active[cid] = {"format": profile["format"]}

    config = get_config() or {}
    config["channels"] = active
    config.setdefault("mode", "natural")

    saved = save_config(config)
    return config, saved


# ──── Giphy search ──────────────────────────────────────────────────────

def search_giphy(query, rating="g"):
    api_key = get_api_key()
    if not api_key:
        return {"error": "GIPHY_API_KEY not found", "help": SETUP_HELP}

    encoded = urllib.parse.quote(query)
    url = f"https://api.giphy.com/v1/gifs/search?api_key={api_key}&q={encoded}&limit=3&rating={rating}"

    req = urllib.request.Request(url, headers={"User-Agent": "openclaw-gif-multi/1.0"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())

    if not data.get("data"):
        return {"error": f"No results for '{query}'"}

    g = data["data"][0]
    return {
        "gif_url": g["images"]["downsized"]["url"],
        "gif_id": g.get("id", "unknown"),
        "title": g.get("title", query),
    }


# ──── Channel conversion ────────────────────────────────────────────────

def convert(gif_path, channel, out_dir):
    profile = CHANNEL_PROFILES.get(channel, {"format": "mp4", "max_bytes": 50_000_000})
    fmt = profile.get("format", "mp4")

    # Unique per-channel filename with timestamp — no topic/thread collisions
    safe_ch = channel.replace("/", "_").replace(" ", "_")
    ts = int(time.time() * 1000)
    out_base = os.path.join(out_dir, f"gif_{safe_ch}_{ts}")

    if fmt == "text_only":
        _cleanup_source(gif_path)
        return {"channel": channel, "format": "text_only",
                "message": f"Channel {channel} does not support animated GIFs."}

    if fmt == "gif_optimized":
        out_path = out_base + ".gif"
        cmd = [
            "ffmpeg", "-y", "-i", gif_path,
            "-vf", "scale=320:-1,fps=10",
            "-fs", str(profile["max_bytes"]),
            out_path
        ]
        subprocess.run(cmd, capture_output=True, text=True)
        _cleanup_source(gif_path)
        _purge_old(out_dir, max_age=600)
        return {"channel": channel, "format": "gif", "path": out_path}

    # MP4 (standard, discord, whatsapp — same flags, profile changes)
    out_path = out_base + ".mp4"
    extra = []
    if fmt == "mp4_whatsapp":
        extra = ["-profile:v", "baseline", "-level", "3.0"]
    cmd = [
        "ffmpeg", "-y", "-i", gif_path,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        *extra,
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        "-an", out_path
    ]
    subprocess.run(cmd, capture_output=True, text=True)
    _cleanup_source(gif_path)
    _purge_old(out_dir, max_age=600)

    size = os.path.getsize(out_path)
    max_bytes = profile.get("max_bytes", 50_000_000)
    if size > max_bytes:
        return {"channel": channel, "format": "mp4", "path": out_path,
                "warning": f"File size {size} bytes exceeds the {max_bytes} limit for {channel}"}

    return {"channel": channel, "format": "mp4", "path": out_path}


# ──── Main ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Giphy Multi — cross-platform GIF search and send")
    parser.add_argument("query", nargs="?", default=None, help="Search term")
    parser.add_argument("--channel", default=None, help="Target channel (telegram, whatsapp, etc.)")
    parser.add_argument("--discover", action="store_true", help="Detect active channels via openclaw CLI")
    parser.add_argument("--check", action="store_true", help="Verify configuration")
    parser.add_argument("--mode", choices=["natural", "on_request"], default=None, help="Set usage mode")
    parser.add_argument("--config", default=None, help="Path to config.json (optional)")
    parser.add_argument("--rating", default="g", help="Content rating: g, pg, pg-13, r")
    args = parser.parse_args()

    if args.config:
        global CONFIG_PATH
        CONFIG_PATH = args.config

    if args.check:
        run_check()
        return

    if args.discover:
        config, path = discover_channels()
        print(json.dumps({"ok": True, "channels": list(config["channels"].keys()),
                          "mode": config["mode"], "config_path": path}))
        return

    if args.mode:
        config = get_config()
        if not config:
            print(json.dumps({"error": "No config found. Run --discover first."}))
            sys.exit(1)
        config["mode"] = args.mode
        path = save_config(config)
        print(json.dumps({"ok": True, "mode": args.mode, "config_path": path}))
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)

    channel = args.channel
    if not channel:
        config = get_config()
        if config and config.get("channels"):
            chs = list(config["channels"].keys())
            if len(chs) == 1:
                channel = chs[0]
            else:
                print(json.dumps({"error": "Multiple channels available. Specify --channel."}))
                sys.exit(1)
        else:
            print(json.dumps({"error": "No channels configured. Run --discover first or use --channel."}))
            sys.exit(1)

    result = search_giphy(args.query, args.rating)
    if "error" in result:
        print(json.dumps(result))
        sys.exit(1)

    # Cache in workspace (accessible by message tool)
    out_dir = os.path.join(os.path.dirname(SKILL_DIR), "..", ".gif_cache")
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    _purge_old(out_dir)  # Only old files (>10 min), leave recent ones alone

    gif_path = os.path.join(out_dir, f"source_{channel}.gif")
    urllib.request.urlretrieve(result["gif_url"], gif_path)

    conv = convert(gif_path, channel, out_dir)

    output = {**result, **conv, "query": args.query}
    print(json.dumps(output))


if __name__ == "__main__":
    main()
