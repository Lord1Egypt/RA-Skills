# Setup & Requirements

## Prerequisites

- Node.js 14 or later
- npm or yarn package manager
- ~200MB disk space for Puppeteer (includes Chromium)

## Installation

### 1. Install Puppeteer

```bash
npm install puppeteer
```

This automatically downloads a compatible version of Chromium.

### 2. Alternative: Use System Chromium

If you already have Chrome/Chromium installed, save bandwidth by using the system version:

```bash
npm install puppeteer
export PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
export PUPPETEER_EXECUTABLE_PATH=/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome  # macOS
# Or on Linux:
# export PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
```

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `PUPPETEER_EXECUTABLE_PATH` | Path to Chrome/Chromium binary | `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` |
| `PUPPETEER_SKIP_CHROMIUM_DOWNLOAD` | Skip downloading Chromium | `true` |
| `PUPPETEER_TIMEOUT` | Default timeout (ms) | `30000` |

## Headless Mode Issues

On some systems, headless mode may fail. If you see browser errors:

```bash
# Try launching with minimal sandbox:
# Modify html-to-pdf.js to use:
# const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
```

## macOS Specific

If you get "Permission denied" errors:

```bash
# Allow unsigned app
xattr -d com.apple.quarantine /path/to/chrome
```

## Linux Specific

Additional dependencies may be required:

```bash
# Ubuntu/Debian
sudo apt-get install -y libgconf-2-4 \
  libnss3 libxss1 libasound2 libappindicator1 libindicator7 xdg-utils fonts-liberation

# Fedora
sudo dnf install -y mesa-libGL nss atk at-spi2-atk gtk3 ipa-gothic-fonts
```

## Testing

Verify Puppeteer works:

```bash
node -e "const puppeteer = require('puppeteer'); puppeteer.launch().then(b => b.close()).then(() => console.log('✅ Puppeteer OK'))"
```

If successful, you'll see `✅ Puppeteer OK`.
