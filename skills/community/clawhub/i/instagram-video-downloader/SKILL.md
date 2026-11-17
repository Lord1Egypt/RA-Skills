---
name: instagram-video-downloader
description: Instagram Video Downloader — paste an Instagram video link and get a watermark-free video download URL instantly. Use when you need to download Instagram videos, save IG videos, or get Instagram video direct links. Triggers: Instagram video download, IG video download, Ins video download, Instagram video parser, download Instagram video, reel download.
---

# Instagram Video Downloader

Parse Instagram video links via the [redfox.hk](https://redfox.hk/settings/api-keys?source=clawhub) API and return watermark-free video download URLs.

---

## Overview

- **Platform Support**: Instagram
- **Content Type**: Video (MP4 direct download link)
- **Input**: Paste an Instagram video link (one link per request; batch upload not supported)
- **Output**: Returns the video download URL directly — copy it into your browser or download tool to save
- **Link Display Rule**: Download and cover links must be displayed in full; never use `...` or any form of truncation

---

## Usage

### Example Command

Download an Instagram video:

```bash
python3 "$SKILL_PATH/scripts/downloader.py" "https://www.instagram.com/reel/xxxxx/"
```

### First-Time Setup

Configure your API Key first, then run:

```bash
# Set environment variable
export REDFOX_API_KEY=ak_your_key

# Parse the video and get the download link
python3 "$SKILL_PATH/scripts/downloader.py" "https://www.instagram.com/reel/xxxxx/"
```

> Visit [redfox.hk](https://redfox.hk/settings/api-keys?source=clawhub) to register and get your API Key.

### Ongoing Usage

Configuration options (choose one):

| Method | Command |
|------|------|
| **Environment Variable** (recommended) | `export REDFOX_API_KEY=ark_your_key` |
| **CLI Argument** | `python3 "$SKILL_PATH/scripts/downloader.py" "<link>" --api-key ark_your_key` |
| **Config File** | `echo '{"api_key":"ark_your_key"}' > ~/.qoder/apis/redfox.json` |

---

## Key Features

| Feature | Description |
|------|------|
| **Watermark-Free Direct Link** | API automatically returns a watermark-free video download URL |
| **Paste & Parse** | Just paste the post link — no extra steps needed |
| **Adaptive URL Recognition** | Supports both Reel and regular post links on instagram.com |
| **Instant Results** | Parsing completes and returns the download URL immediately — copy and use |

---

## Common Use Cases

| Scenario | Example Link | Description |
|------|----------|------|
| Save IG videos | `https://www.instagram.com/reel/xxxxx/` | Get a watermark-free video download URL |
| Offline Reel collection | `https://www.instagram.com/reel/xxxxx/` | Parse and copy the link to download and save |
| Content remixing | Any Instagram video link | Download clips for editing and creative use |
| Asset backup | Any Instagram video link | Back up your favorite videos locally |

### Supported Link Formats

| Platform | Link Format | Example |
|------|----------|------|
| Instagram Reel | `https://www.instagram.com/reel/<shortcode>/` | Reel short video |
| Instagram Post | `https://www.instagram.com/p/<shortcode>/` | Regular post video |

---

## FAQ

**Q: How do I get my API Key?**
A: Visit [redfox.hk](https://redfox.hk/settings/api-keys?source=clawhub) to register and obtain your token.

**Q: Does the downloaded video have a watermark?**
A: No. The API returns a watermark-free video direct URL.

**Q: Can I upload multiple links at once?**
A: No. Only one link can be parsed per request. Batch upload will cause parsing failure.

**Q: What if parsing fails?**
A: Make sure the link is complete, the post still exists, and the account is public. Private accounts or deleted posts cannot be parsed.

---

## Learn More

This tool is built on the [redfox.hk](https://redfox.hk/settings/api-keys?source=clawhub) `parseWork/videoDownload/instagram` API. Visit the official website for more API capabilities and documentation.
