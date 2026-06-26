#!/usr/bin/env bash
# Fetch new HN podcast episodes and transcribe them with Whisper.
# Usage: fetch_and_transcribe.sh [--feed URL] [--archive DIR] [--model MODEL] [--limit N]
set -euo pipefail

FEED_URL="https://media.rss.com/hacker-news-morning-brief/feed.xml"
ARCHIVE_DIR="./hn-podcast-archive"
WHISPER_MODEL="turbo"
LIMIT=0  # 0 = no limit

while [[ $# -gt 0 ]]; do
  case $1 in
    --feed)    FEED_URL="$2"; shift 2 ;;
    --archive) ARCHIVE_DIR="$2"; shift 2 ;;
    --model)   WHISPER_MODEL="$2"; shift 2 ;;
    --limit)   LIMIT="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

mkdir -p "$ARCHIVE_DIR"
export WHISPER_MODEL="$WHISPER_MODEL"

STATE_FILE="$ARCHIVE_DIR/state.json"
if [[ ! -f "$STATE_FILE" ]]; then
  echo '{}' > "$STATE_FILE"
fi

# Parse RSS feed and extract episode info using python
python3 - "$FEED_URL" "$ARCHIVE_DIR" "$LIMIT" <<'PYEOF'
import xml.etree.ElementTree as ET
import json, os, subprocess, sys, hashlib, urllib.request, re, datetime

feed_url = sys.argv[1]
archive_dir = sys.argv[2]
limit = int(sys.argv[3])

state_file = os.path.join(archive_dir, "state.json")
with open(state_file) as f:
    state = json.load(f)

# Download feed
req = urllib.request.Request(feed_url, headers={"User-Agent": "hn-podcast-transcriber/1.0"})
with urllib.request.urlopen(req, timeout=30) as resp:
    feed_xml = resp.read()

root = ET.fromstring(feed_xml)
channel = root.find("channel")

processed = 0
for item in channel.findall("item"):
    if limit > 0 and processed >= limit:
        break

    title_el = item.find("title")
    pub_el = item.find("pubDate")
    enclosure = item.find("enclosure")

    if title_el is None or enclosure is None:
        continue

    title = title_el.text or "untitled"
    audio_url = enclosure.get("url", "")
    if not audio_url:
        continue

    # Stable ID from audio URL hash
    ep_id = hashlib.sha256(audio_url.encode()).hexdigest()[:12]

    if state.get(ep_id, {}).get("transcribed"):
        continue

    # Sanitize title for directory name
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')[:80]
    date_str = ""
    if pub_el is not None and pub_el.text:
        try:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(pub_el.text)
            date_str = dt.strftime("%Y-%m-%d")
        except Exception:
            pass

    ep_dir_name = f"{date_str}_{safe_title}" if date_str else safe_title
    ep_dir = os.path.join(archive_dir, ep_dir_name)
    os.makedirs(ep_dir, exist_ok=True)

    # Download audio
    audio_ext = os.path.splitext(audio_url.split("?")[0])[1] or ".mp3"
    audio_path = os.path.join(ep_dir, f"episode{audio_ext}")

    print(f"[{ep_id}] Downloading: {title}")
    urllib.request.urlretrieve(audio_url, audio_path)

    # Save metadata
    meta = {"id": ep_id, "title": title, "audio_url": audio_url, "date": date_str}
    desc_el = item.find("description")
    if desc_el is not None and desc_el.text:
        meta["description"] = desc_el.text[:2000]
    with open(os.path.join(ep_dir, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    # Transcribe with whisper
    whisper_model = os.environ.get("WHISPER_MODEL", "turbo")
    print(f"[{ep_id}] Transcribing with whisper --model {whisper_model}...")
    try:
        result = subprocess.run(
            ["whisper", audio_path, "--model", whisper_model,
             "--output_format", "txt", "--output_dir", ep_dir],
            capture_output=True, text=True, timeout=600
        )
        if result.returncode != 0:
            print(f"[{ep_id}] Whisper error: {result.stderr[:500]}")
            continue
    except FileNotFoundError:
        print("ERROR: whisper not found. Install with: pip install openai-whisper")
        sys.exit(1)

    # Check transcript
    txt_path = os.path.join(ep_dir, "episode.txt")
    if os.path.exists(txt_path):
        with open(txt_path) as f:
            transcript = f.read()
        # Save a clean markdown version
        md_path = os.path.join(ep_dir, "transcript.md")
        with open(md_path, "w") as f:
            f.write(f"# {title}\n\n")
            if date_str:
                f.write(f"**Date:** {date_str}\n\n")
            f.write(f"## Transcript\n\n{transcript}\n")
        print(f"[{ep_id}] ✓ Transcribed ({len(transcript)} chars)")

    state[ep_id] = {"transcribed": True, "title": title, "dir": ep_dir_name}
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    processed += 1

print(f"\nDone. Processed {processed} new episode(s). {len(state)} total in archive.")
PYEOF