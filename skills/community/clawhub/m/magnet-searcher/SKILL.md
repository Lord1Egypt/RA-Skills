---
name: magnet-searcher
description: Search for movies, TV shows, or other content and find magnet/torrent download links. Use this skill whenever the user asks for movie downloads, torrent links, magnet links, BT downloads, or wants to find download sources for specific content. This skill uses agent-browser to navigate magnet search sites and extract working magnet URLs. Trigger whenever the user says things like "find magnet link for X", "search for movie X torrent", "find the download link for X", "帮我找X的磁力链接", etc.
---

# Magnet Searcher Skill

This skill enables searching for movies, TV shows, and other content, then finding and extracting magnet/torrent download links using the agent-browser tool.

## Prerequisites

### 1. Install agent-browser

```bash
npm install -g agent-browser
```

### 2. Install Chromium

**For Debian/Ubuntu:**
```bash
apt-get install -y chromium
```

**For other Linux distributions:**
```bash
# Try the default install command
agent-browser install
# If that fails (no ARM64 build), use system package manager:
# Fedora: sudo dnf install chromium
# Then use: agent-browser --executable-path /usr/bin/chromium
```

### 3. Verify Chromium is accessible

```bash
which chromium  # Should return /usr/bin/chromium
```

## Core Workflow

### Step 1: Search on a Magnet Site

Open a magnet search site and search for the content:

```bash
# Option 1: BTSOW (often works well)
agent-browser open "https://btsow.pics"
agent-browser fill @e7 "movie name here"  # Fill search box
agent-browser press Enter

# Option 2: 360 search engine (good for Chinese content)
agent-browser open "https://www.so.com/s?q=电影名+磁力链"

# Option 3: Bing search
agent-browser open "https://cn.bing.com/search?q=电影名+磁力链"
```

### Step 2: Navigate to Results

After search results appear:

```bash
# Wait for page to load
agent-browser wait 2000

# Get page snapshot to see results
agent-browser snapshot
```

### Step 3: Click on a Result Page

Find a relevant result (often shows "磁力" or "magnet" in the snippet) and click it:

```bash
agent-browser click @e36  # Use the ref from snapshot
agent-browser wait 3000
```

### Step 4: Extract the Magnet Link

On the detail page, use JavaScript evaluation to find magnet links:

```bash
# Find any magnet link on the page
agent-browser eval "document.querySelector('a[href*=magnet]')?.href"

# If that returns nothing, try these alternatives:
agent-browser eval "document.body.innerText"  # Get all text, then search manually
```

Common magnet link patterns:
- `magnet:?xt=urn:btih:...`
- Magnet links may be displayed as plain text links

### Step 5: Close Browser When Done

```bash
agent-browser close
```

## Common Issues & Solutions

### Baidu requires CAPTCHA
If Baidu shows a security verification, switch to:
- Bing (cn.bing.com)
- 360 (so.com)
- BTSOW (btsow.pics)

### Page navigation times out
Some magnet sites are slow or block bots. Try:
- Waiting longer with `agent-browser wait 5000`
- Trying a different site

### Element refs change after page load
Always get a fresh snapshot after waiting:
```bash
agent-browser wait 2000
agent-browser snapshot
```

### Chromium not found
Use the executable-path flag:
```bash
agent-browser --executable-path /usr/bin/chromium open "https://example.com"
```

## Workflow Summary

```
1. Install agent-browser + Chromium
2. Open magnet search site
3. Fill search box with content name
4. Wait for results
5. Click on relevant result
6. Use JS eval to extract magnet URL
7. Close browser
```

## Example: Finding "巅峰猎杀" (Apex 2026) Magnet

```bash
# Install
npm install -g agent-browser
apt-get install -y chromium

# Search on 360
agent-browser --executable-path /usr/bin/chromium open "https://www.so.com/s?q=巅峰猎杀+磁力链"
agent-browser wait 2000
agent-browser snapshot

# Click on result containing "磁力"
# (Get the ref from snapshot output)
agent-browser click @e36
agent-browser wait 3000

# Extract magnet link
agent-browser eval "document.querySelector('a[href*=magnet]')?.href"

# Result: magnet:?xt=urn:btih:cdeba1f57fbe45bf4f72f8a27908c29857e30614
```

## Important Notes

1. **Legal disclaimer**: Only search for content you have rights to download
2. **时效性**: Magnet links may expire or become unavailable over time
3. **Multiple sources**: If one site fails, try another
4. **Chinese sites**: For Chinese movies/shows, use Chinese search terms and sites work better
