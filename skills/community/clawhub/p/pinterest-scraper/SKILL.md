---
name: pinterest-scraper
description: Full-featured Pinterest image scraper with infinite scroll, quality options, Telegram integration, duplicate detection, resume support, and verbose logging. Use when: (1) Scraping Pinterest boards/users/search, (2) Need quality options (originals/736x/474x/236x), (3) Sending images to Telegram, (4) Resuming interrupted scrapes, (5) Avoiding duplicate downloads, (6) Debugging with verbose logs.
version: 1.1.0
changelog: "v1.1.0: Added reasoning framework, decision trees, troubleshooting, self-checks"
metadata:
  openclaw:
    requires:
      bins:
        - python3
      pip:
        - playwright
        - requests
    emoji: "📌"
    category: "utility"
    homepage: https://github.com/KeXu9/pinterest-scraper
---

# Pinterest Scraper

Full-featured Pinterest image scraper with automatic scrolling and multiple output options.

## When This Skill Activates

This skill triggers when user wants to download images from Pinterest.

## Reasoning Framework

| Step | Action | Why |
|------|--------|-----|
| 1 | **EXTRACT** | Parse Pinterest URL to determine board/user/search |
| 2 | **LAUNCH** | Start Playwright browser with stealth options |
| 3 | **SCROLL** | Incrementally load images (Pinterest uses infinite scroll) |
| 4 | **COLLECT** | Extract image URLs with quality selection |
| 5 | **DEDUP** | Hash-based duplicate detection |
| 6 | **DOWNLOAD** | Save images to output folder |
| 7 | **NOTIFY** | Optional: send to Telegram |

---

## Setup

```bash
pip install playwright requests
playwright install chromium
```

---

## Decision Tree

### What are you trying to do?

```
├── Download images from a board/user
│   └── Use: -u "URL" -s [scrolls]
│
├── Get highest quality possible
│   └── Use: -q originals
│
├── Get smaller/faster downloads
│   └── Use: -q 736x or 236x
│
├── Send images to phone
│   └── Use: --telegram --token X --chat Y
│
├── Resume interrupted scrape
│   └── Use: --resume
│
└── Debug issues
    └── Use: -v (verbose logging)
```

### Quality Selection Decision

| Quality | Use Case | File Size |
|---------|----------|-----------|
| originals | Best quality, archiving | Largest |
| 736x | Good balance | Medium |
| 474x | Thumbnail quality | Small |
| 236x | Preview only | Smallest |
| all | Save every version | Largest total |

---

## Usage

### Command Line

```bash
python scrape_pinterest.py -u "URL" [options]
```

| Option | Description | Default |
|--------|-------------|---------|
| `-u, --url` | Pinterest URL (required) | - |
| `-s, --scrolls` | Number of scrolls | 50 |
| `-o, --output` | Output folder | ./pinterest_output |
| `-q, --quality` | Quality: originals/736x/474x/236x/all | originals |
| `-v, --verbose` | Enable verbose logging | false |
| `--telegram` | Send images to Telegram | false |
| `--token` | Telegram bot token | - |
| `--chat` | Telegram chat ID | - |
| `--resume` | Resume from previous scrape | false |
| `--dedup` | Skip duplicates | true |
| `--no-dedup` | Disable deduplication | - |
| `--telegram-only` | Only send existing files | false |

### Common Examples

```bash
# Basic scrape (50 scrolls, originals, current dir)
python scrape_pinterest.py -u "URL"

# Verbose mode (logs to console + scrape.log)
python scrape_pinterest.py -u "URL" -v

# More scrolls, custom output, medium quality
python scrape_pinterest.py -u "URL" -s 100 -o ./output -q 736x -v

# With Telegram delivery
python scrape_pinterest.py -u "URL" --telegram --token "TOKEN" --chat "CHAT_ID"

# Resume interrupted scrape
python scrape_pinterest.py -u "URL" --resume -v

# Show help
python scrape_pinterest.py --help
```

---

## Python API

This tool is CLI-based. Run it from your Python code:

```python
import subprocess
import os

# Run the scraper
result = subprocess.run(
    ['python3', 'scrape_pinterest.py', '-u', 'URL', '-s', '50', '-q', 'originals'],
    cwd='./scripts',
    capture_output=True,
    text=True
)

print(result.returncode)  # 0 = success
print(result.stdout)
```

---

## Features

| Feature | Description |
|---------|-------------|
| Infinite Scroll | Automatic scrolling loads more images |
| Quality Options | originals/736x/474x/236x/all |
| Telegram | Send directly to Telegram |
| Deduplication | Hash-based duplicate detection |
| Resume | Continue from previous scrape |
| URL Types | Boards, user profiles, search results |
| Verbose Logging | -v flag, logs to console + scrape.log |

---

## Verbose Logging

Use `-v` or `--verbose` for detailed logging:

```bash
python scrape_pinterest.py -u "URL" -v
```

**What gets logged:**
- Scroll progress (every 10 scrolls)
- Images found per scroll
- Download progress (X/Y)
- Telegram send status
- Errors and warnings

**Log files:**
- Console: INFO level
- `scrape.log`: DEBUG level (detailed)

---

## Troubleshooting

### Problem: No images downloaded

- **Cause:** Not enough scrolls, Pinterest didn't load
- **Fix:** Increase `-s` value (try 100-200)

### Problem: "Browser not found"

- **Cause:** Playwright not installed
- **Fix:** `playwright install chromium`

### Problem: SSL certificate errors (Mac)

- **Cause:** macOS SSL issues
- **Fix:** Use `verify=False` in requests calls

### Problem: Duplicate images

- **Cause:** Deduplication disabled or failed
- **Fix:** Use `--dedup` flag (default: on)

### Problem: Resume not working

- **Cause:** State file missing or URL changed
- **Fix:** Use same URL as original, check `.scrape_state.json`

### Problem: Telegram not sending

- **Cause:** Invalid token/chat ID, rate limiting
- **Fix:** Verify bot token, check chat ID, Telegram limits 100 images/batch

### Problem: Verbose logs not writing

- **Cause:** File permission issue
- **Fix:** Check write permissions in output directory

---

## Self-Check

- [ ] Pinterest URL is valid (board/user/search)
- [ ] Playwright installed: `playwright install chromium`
- [ ] Quality selected appropriately for use case
- [ ] Output directory exists or is writable
- [ ] For Telegram: token and chat ID correct
- [ ] For resume: using same URL as original scrape

---

## Notes

- Pinterest loads dynamically - scrolling required for more images
- Use `verify=False` for requests (Mac SSL issues)
- State saved to `.scrape_state.json` for resume
- Telegram limited to 100 images per batch
- Verbose mode writes detailed logs to `scrape.log`

---

## Quick Reference

| Task | Command |
|------|---------|
| Basic scrape | `python scrape_pinterest.py -u "URL"` |
| Verbose debug | `python scrape_pinterest.py -u "URL" -v` |
| High quality | `python scrape_pinterest.py -u "URL" -q originals` |
| Fast/small | `python scrape_pinterest.py -u "URL" -q 236x` |
| Send to Telegram | `python scrape_pinterest.py -u "URL" --telegram --token X --chat Y` |
| Resume | `python scrape_pinterest.py -u "URL" --resume` |
| Custom output | `python scrape_pinterest.py -u "URL" -o ./myfolder` |

---
