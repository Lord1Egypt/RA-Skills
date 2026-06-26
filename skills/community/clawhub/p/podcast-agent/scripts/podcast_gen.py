#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
podcast-gen — 播客生成器 / Podcast Generator

搜索文章 → 生成对话体脚本 → TTS 合成音频
Search articles → Generate dialogue script → Synthesize podcast audio.

Usage:
  python podcast-gen.py search --query "..." [--count 3]
  python podcast-gen.py fetch --url "..."
  python podcast-gen.py tts --script script.json --output podcast.mp3
  python podcast-gen.py voices
"""

import json, sys, time, argparse, os, asyncio, subprocess, re, socket, ipaddress
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse, quote_plus

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def validate_url(url):
    """Validate URL is safe to fetch (block SSRF/internal access)."""
    parsed = urlparse(url)

    # Only allow http/https
    if parsed.scheme not in ("http", "https"):
        return False, f"Blocked scheme: {parsed.scheme}"

    hostname = parsed.hostname
    if not hostname:
        return False, "No hostname"

    # Block obvious internal hostnames
    blocked_hosts = {"localhost", "127.0.0.1", "0.0.0.0", "::1", "metadata.google.internal",
                     "169.254.169.254"}  # AWS/GCP metadata
    if hostname.lower() in blocked_hosts:
        return False, f"Blocked internal host: {hostname}"

    # Resolve and check IP ranges
    try:
        addr_infos = socket.getaddrinfo(hostname, None)
        for info in addr_infos:
            ip = ipaddress.ip_address(info[4][0])
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                return False, f"Blocked private/internal IP: {ip}"
    except socket.gaierror:
        return False, f"Cannot resolve: {hostname}"

    return True, "OK"


def get_output_dir():
    d = Path(__file__).parent.parent / "output"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ────────────────────────────────────────
# Search (agent will call web_search separately)
# ────────────────────────────────────────

def cmd_search(args):
    """Output search instructions for the agent."""
    print(json.dumps({
        "action": "web_search",
        "query": args.query,
        "count": args.count or 3,
        "instruction": f"Use web_search tool to find articles about: {args.query}"
    }, ensure_ascii=False))


def cmd_fetch(args):
    """Fetch article content from URL."""
    import urllib.request
    url = args.url

    # SSRF protection
    safe, reason = validate_url(url)
    if not safe:
        print(json.dumps({"url": url, "error": f"Security: {reason}"}, ensure_ascii=False))
        return

    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()

        # Try to detect encoding
        content_type = resp.headers.get("Content-Type", "")
        charset = "utf-8"
        if "charset=" in content_type:
            charset = content_type.split("charset=")[-1].strip()

        text = data.decode(charset, errors="replace")

        # Strip HTML tags for text extraction
        text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        # Take first 8000 chars (enough for a podcast segment)
        if len(text) > 8000:
            text = text[:8000] + "\n[...truncated]"

        result = {
            "url": url,
            "content": text,
            "length": len(text),
        }
        print(json.dumps(result, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"url": url, "error": str(e)}, ensure_ascii=False))


# ────────────────────────────────────────
# TTS Synthesis
# ────────────────────────────────────────

VOICES = {
    "A": "zh-CN-XiaoxiaoNeural",   # Female, warm - host
    "B": "zh-CN-YunyangNeural",    # Male, professional - expert
}

# English fallback voices
VOICES_EN = {
    "A": "en-US-JennyNeural",      # Female
    "B": "en-US-GuyNeural",        # Male
}


def cmd_voices():
    """List available voices."""
    print("🎤 可用语音:\n")
    print("  中文:")
    print(f"    A (主持人): {VOICES['A']} - Female, Warm")
    print(f"    B (专家):   {VOICES['B']} - Male, Professional")
    print(f"  English:")
    print(f"    A (Host):   {VOICES_EN['A']} - Female")
    print(f"    B (Expert): {VOICES_EN['B']} - Male")


def clean_ssml(text):
    """Clean text for SSML, escape special characters."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    return text


async def generate_segment(voice, text, output_path, rate="+0%", pitch="+0Hz"):
    """Generate a single audio segment using edge-tts."""
    import edge_tts

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
    )
    await communicate.save(output_path)


async def generate_podcast_async(script_file, output_file, lang="zh"):
    """Generate a full podcast from a script file."""
    import edge_tts

    script = json.loads(Path(script_file).read_text(encoding="utf-8"))

    voices = VOICES if lang == "zh" else VOICES_EN

    output_dir = Path(output_file).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    segments = []
    total_duration = 0

    print(f"🎙️ 生成播客: {len(script.get('segments', []))} 个片段")

    for i, seg in enumerate(script.get("segments", [])):
        speaker = seg.get("speaker", "A")
        text = seg.get("text", "").strip()
        if not text:
            continue

        voice = voices.get(speaker, voices["A"])

        # Adjust style based on role
        rate = "+5%" if speaker == "A" else "+0%"
        pitch = "+0Hz"

        seg_file = output_dir / f"seg_{i:03d}_{speaker}.mp3"

        print(f"  [{i+1}/{len(script['segments'])}] {speaker}: {text[:40]}...")

        await generate_segment(voice, text, str(seg_file), rate=rate, pitch=pitch)
        segments.append(str(seg_file))

    if not segments:
        print("❌ 没有有效片段")
        return

    # Combine segments using ffmpeg
    print(f"\n🔗 合并 {len(segments)} 个片段...")

    # Create concat file
    concat_file = output_dir / "concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(f"file '{Path(seg).absolute()}'\n")

    # Check if ffmpeg is available
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        # Use ffmpeg to concatenate
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            str(output_file)
        ], capture_output=True, check=True)
        print(f"✅ 播客已生成: {output_file}")
    except (FileNotFoundError, subprocess.CalledProcessError):
        # No ffmpeg, just copy the first file or merge with built-in
        print("⚠️ ffmpeg 未安装，使用 Python 合并（质量稍降）")
        await merge_audio_python(segments, output_file)
        print(f"✅ 播客已生成: {output_file}")

    # Cleanup segment files
    for seg in segments:
        try:
            Path(seg).unlink(missing_ok=True)
        except:
            pass
    try:
        concat_file.unlink(missing_ok=True)
    except:
        pass

    # Print stats
    file_size = Path(output_file).stat().st_size
    print(f"   文件大小: {file_size / 1024:.0f} KB")


async def merge_audio_python(segments, output_file):
    """Merge audio segments using Python (fallback when no ffmpeg)."""
    import edge_tts

    # Simple approach: re-generate combined text
    # For better quality, ffmpeg is recommended
    combined_text = []
    script_parts = []

    for seg_path in segments:
        # Read the segment filename to extract speaker info
        name = Path(seg_path).stem
        combined_text.append(seg_path)

    # Alternative: just concatenate the raw bytes (MP3 frames)
    # This is a simplified approach
    output_data = b""
    for seg in segments:
        try:
            with open(seg, "rb") as f:
                output_data += f.read()
        except:
            continue

    with open(output_file, "wb") as f:
        f.write(output_data)


def cmd_tts(args):
    """Generate podcast audio from script."""
    script_file = args.script
    output = args.output or str(get_output_dir() / f"podcast_{int(time.time())}.mp3")
    lang = args.lang or "zh"

    if not Path(script_file).exists():
        print(f"❌ Script file not found: {script_file}")
        return

    asyncio.run(generate_podcast_async(script_file, output, lang))


# ────────────────────────────────────────
# Main
# ────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="podcast-gen",
        description="Podcast Generator / 播客生成器",
    )
    sub = parser.add_subparsers(dest="command")

    # search
    p = sub.add_parser("search", help="Search for articles (outputs instructions)")
    p.add_argument("--query", required=True)
    p.add_argument("--count", type=int, default=3)

    # fetch
    p = sub.add_parser("fetch", help="Fetch article content from URL")
    p.add_argument("--url", required=True)

    # tts
    p = sub.add_parser("tts", help="Generate podcast audio from script")
    p.add_argument("--script", required=True, help="Path to script JSON")
    p.add_argument("--output", default=None, help="Output audio file path")
    p.add_argument("--lang", default="zh", choices=["zh", "en"])

    # voices
    sub.add_parser("voices", help="List available voices")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    cmds = {
        "search": cmd_search,
        "fetch": cmd_fetch,
        "tts": cmd_tts,
        "voices": lambda a: cmd_voices(),
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
