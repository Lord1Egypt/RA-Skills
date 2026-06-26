#!/usr/bin/env python3
"""
init.py — Initialize the hum data directory.

Creates template files (VOICE.md, CONTENT.md, AUDIENCE.md, CHANNELS.md)
and required folders (feed/, content/, content-samples/, knowledge/, ideas/).
Skips any file or folder that already exists.

Usage:
    python3 init.py
    python3 init.py --data-dir ~/Documents/hum
"""

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS_ROOT))

from config import load_config

FOLDERS = [
    "feed",
    "feed/raw",
    "feed/assets",
    "content",
    "content/drafts",
    "content/published",
    "content/images",
    "content-samples",
    "knowledge",
    "ideas",
    "learn",
]

TEMPLATES = {
    "knowledge/index.md": """\
# Knowledge Sources

Long-form sources crawled by `/hum crawl` and `/hum refresh-feed`.
Each table row defines a source with a Key (used as folder name), Handler, and Feed URL.

Supported handlers: `rss`, `sitemap`, `youtube`, `podcast`

## Blogs & Newsletters

| Key | Handler | Feed URL |
|-----|---------|----------|
<!-- | example-blog | rss | https://example.com/feed.xml | -->

## YouTube Channels (full transcripts)

| Key | Handler | Feed URL |
|-----|---------|----------|
<!-- | example-channel | youtube | https://www.youtube.com/@example | -->

## Podcasts

| Key | Handler | Feed URL |
|-----|---------|----------|
<!-- | example-pod | podcast | https://feeds.example.com/podcast.xml | -->
""",
    "VOICE.md": """\
# Voice

How you want your content to sound. Fill this in with your writing style, tone, and rules.

## Tone
<!-- e.g. conversational but authoritative, dry humour, no fluff -->

## Style rules
<!-- e.g. short paragraphs, no bullet lists in body, never start with "I" -->

## Words to avoid
<!-- e.g. "leverage", "synergy", "thought leader" -->

## Words to use
<!-- e.g. specific jargon, brand terms, named concepts -->

## Visual Style
<!-- Optional. Hum appends this to image generation prompts to match your brand. -->
<!-- e.g. "Clean minimal style, muted navy/white palette, flat illustration, no text overlays" -->
""",
    "CONTENT.md": """\
# Content Pillars

Each pillar defines a theme you create content around. The `keywords` field is used
to classify feed items and brainstorm ideas — add terms your audience would use.

## Example Pillar
A one-line description of what this pillar covers.

Keywords: keyword1, keyword2, keyword3

---

<!-- Copy the template below for each pillar. Delete the example above when done. -->

## [Pillar Name]
[One-line description]

Keywords: [comma-separated keywords and phrases used to classify content]
""",
    "AUDIENCE.md": """\
# Audience

Who you are writing for. Be specific — this shapes every draft.

## Primary audience
<!-- e.g. CFOs and finance leaders at growth-stage tech companies -->

## Secondary audience
<!-- e.g. finance professionals exploring AI tooling -->

## What they care about
<!-- e.g. headcount efficiency, automation ROI, board communication -->

## What they already know
<!-- e.g. assume fluency in financial statements, basic AI awareness -->
""",
    "CHANNELS.md": """\
# Channels

Where you publish and at what frequency. Only active channels should be listed here.

---

## LinkedIn

- **Profile URL:**
- **Account name:**
- **Frequency:** <!-- e.g. 3x/week -->
- **Post types:** Post, Article
- **Notes:** <!-- e.g. no external links in body, always attach an image -->

---

## X

- **Profile URL:**
- **Account name:**
- **Frequency:** <!-- e.g. 2x/week + daily repost -->
- **Post types:** Tweet, Thread
- **Notes:** <!-- e.g. links in replies only, keep threads under 10 tweets -->

---

## Engage Command Settings

### X
- **Follows per session:** 5-10
- **Engagement plays per session:** 3-5
- **Response drafts:** up to 5

### LinkedIn
- **Response drafts:** up to 5
""",
}

JSON_FILES = {
    "feed/feeds.json": [],
    "feed/sources.json": {"feed_sources": []},
    "ideas/ideas.json": {"primary_keywords": [], "secondary_keywords": [], "intersection_bonus": 0, "label": "Hum", "ideas": []},
}


def main():
    parser = argparse.ArgumentParser(description="Initialize hum data directory")
    parser.add_argument("--data-dir", help="Override data directory (default: HUM_DATA_DIR env var or ~/Documents/hum)")
    args = parser.parse_args()

    if args.data_dir:
        data_dir = Path(args.data_dir).expanduser().resolve()
    else:
        cfg = load_config()
        data_dir = cfg["data_dir"]

    print(f"Initializing hum data directory: {data_dir}\n")

    # Create folders
    for folder in FOLDERS:
        path = data_dir / folder
        if path.exists():
            print(f"  exists  {folder}/")
        else:
            path.mkdir(parents=True, exist_ok=True)
            print(f"  created {folder}/")

    print()

    # Create template files
    for filename, content in TEMPLATES.items():
        path = data_dir / filename
        if path.exists():
            print(f"  exists  {filename}")
        else:
            path.write_text(content, encoding="utf-8")
            print(f"  created {filename}")

    print()

    # Create JSON seed files
    for relpath, seed in JSON_FILES.items():
        path = data_dir / relpath
        if path.exists():
            print(f"  exists  {relpath}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(seed, indent=2) + "\n", encoding="utf-8")
            print(f"  created {relpath}")

    print()

    # Copy feed.html viewer
    dashboard_src = Path(__file__).resolve().parent / "dashboard.html"
    dashboard_dst = data_dir / "dashboard.html"
    if dashboard_dst.exists():
        print(f"  exists  dashboard.html")
    elif dashboard_src.exists():
        dashboard_dst.write_bytes(dashboard_src.read_bytes())
        print(f"  created dashboard.html")

    print(f"\nDone. Edit the files in {data_dir} to set up your profile.")
    print(f"Open {data_dir}/dashboard.html in Chrome or Edge to browse your feed.")
    print(f"\nNext: install Python dependencies by running:")
    print(f"  bash setup.sh")


if __name__ == "__main__":
    main()
