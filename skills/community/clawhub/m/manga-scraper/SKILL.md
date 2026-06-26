---
name: manga-scraper
description: "Download manga chapters from MangaBat (mangabats.com) directly via CDN — bypasses Cloudflare. Triggered when user asks to download/scrape manga chapters or manga images."
metadata:
  openclaw:
    emoji: "📖"
---

# MangaBat Scraper

Download manga chapters directly from MangaBats CDN without hitting Cloudflare protection.
Auto-falls back to Playwright (headless browser) when CDN is IP-blocked.

## How It Works

**CDN Method (default):** MangaBat serves images from `storage.waitst.com` — CDN is unprotected.
Pattern: `https://storage.waitst.com/zin/[slug]/[chapter]/[page].webp`

**Browser Fallback:** If CDN is IP-blocked, script launches Playwright (headless Chromium)
to extract image URLs directly from the chapter page JavaScript.

## Script Location

Locate the script in your skills directory:

```bash
find ~ -name manga_scraper.py 2>/dev/null
```

## Setup Check

```bash
python3 /path/to/manga_scraper.py --help
```

## Setup (One-Time)

**Required for CDN mode only (default):**
```bash
# Nothing! Uses stdlib only — urllib + concurrent.futures
```

**Required for browser fallback (optional):**
```bash
pip install playwright && playwright install chromium
```

## Usage

**Single chapter (CDN, fast):**
```bash
python3 manga_scraper.py "https://www.mangabats.com/manga/[manga-slug]/chapter-5"
```

**Single chapter + force Playwright fallback (for IP-blocked networks):**
```bash
python3 manga_scraper.py "https://www.mangabats.com/manga/[manga-slug]/chapter-5" \
  --fallback-browser
```

**Chapter range (1–10):**
```bash
python3 manga_scraper.py "https://www.mangabats.com/manga/[manga-slug]" \
  --start 1 --end 10 --workers 4
```

**All chapters (auto-detect last by 404 scan):**
```bash
python3 manga_scraper.py "https://www.mangabats.com/manga/[manga-slug]" \
  --all --workers 3
```

**Skip browser fallback (faster, for CI):**
```bash
python3 manga_scraper.py "..." --no-browser
```

**Custom output folder:**
```bash
python3 manga_scraper.py "URL" --output ~/Manga/MyManga
```

## Flags

| Flag | Description |
|------|-------------|
| `--all` | Download all chapters (manga URL, auto-detects last by 404 scan) |
| `--start N` | Start from chapter N |
| `--end N` | End at chapter N |
| `--workers N` | Concurrent downloads, default 3 |
| `--output -o` | Output directory, default `./downloads/` |
| `--fallback-browser` | Force Playwright fallback (for IP-blocked networks) |
| `--no-browser` | Skip Playwright fallback entirely (faster, CI/CD) |

## CDN Fallback Chain

If one CDN fails, script tries the next automatically:

1. `storage.waitst.com` — **current default** (`/zin/[slug]/[ch]/[page].webp`)
2. `img-r1.2xstorage.com` — legacy (`/[slug]/[ch]/[page].webp`)
3. `img-2xcdn.com` — fallback (`/[slug]/[ch]/[page].webp`)

If all CDNs return 403 → auto-activates Playwright fallback (installs Chromium once).

## Output

- Saves to `chapter_NNN/page_000.webp` naming convention
- Resume support: skips existing files
- Some pages may be missing (MangaBat sometimes removes individual pages — placeholder is ~14 bytes, skipped automatically)
- Image format: `.webp`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `0/0 downloaded` — all 403 | IP blocked. Use `--fallback-browser` or activate VPN |
| `0/0 downloaded` — all 000 | No internet. Check connection |
| `playwright` import error | Run: `pip install playwright && playwright install chromium` |
| Missing pages (14 bytes each) | Normal — MangaBat removes pages from CDN sometimes |
| Script breaks in future | Run with `--fallback-browser` — browser always works |

## Notes

- Script is pure Python stdlib (urllib + concurrent.futures) for CDN mode
- Playwright fallback requires Chromium (~150MB download, one-time)
- Be respectful: use `--workers 3` or lower for batch downloads
- Mangabat rotates CDNs every few months — current CDN is `storage.waitst.com`
