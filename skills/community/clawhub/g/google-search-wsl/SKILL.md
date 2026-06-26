---
name: google-search-wsl
description: Google search via Chrome browser in WSL environment. Use when user needs web search, news lookup, or information retrieval. Suitable for: (1) trending news search, (2) information lookup, (3) web research. Automatically launches Chrome in WSL and controls it via CDP protocol.
---

# Google Search (WSL Chrome)

Perform Google searches through Chrome browser in WSL.

## Prerequisites

- `google-chrome-stable` or `google-chrome` installed in WSL
- WSLg available (or X11 forwarding configured)
- OpenClaw browser tool enabled

## Quick Start

### 1. Launch Chrome

Run the startup script:

```bash
bash ~/.openclaw/scripts/google-search-chrome.sh
```

Or start manually:

```bash
export DISPLAY=:0
google-chrome-stable --remote-debugging-port=9222 \
  --remote-allow-origins='*' \
  --user-data-dir="$HOME/.openclaw/chrome-debug-profile" \
  --lang=zh-CN \
  --disable-gpu \
  --disable-dev-shm-usage &
```

### 2. Verify Chrome is Running

```bash
curl -s http://127.0.0.1:9222/json/version
```

Should return Chrome version information.

### 3. Search Using Browser Tool

```
browser action=open url="https://www.google.com/search?q=your+search+term" profile=user
browser action=snapshot targetId=<returned-targetId>
```

## Troubleshooting

### Chrome Won't Start (Missing X server)

Ensure WSLg is available, or set the `DISPLAY` environment variable:

```bash
export DISPLAY=:0
# Or check WSLg
ls /mnt/wslg/.X11-unix/
```

### Port 9222 Already in Use

Check and kill the occupying process:

```bash
lsof -i :9222
kill <PID>
```

### Empty Search Results

- Check network connection
- Try using a proxy (if `HTTP_PROXY` is configured)
- Wait for the page to fully load before taking a snapshot

## Tips

- Chinese keywords in search URLs will be automatically encoded
- Use `snapshot` to get page content, then extract the needed information
- For news search, use the `tbm=nws` parameter: `/search?q=keyword&tbm=nws`