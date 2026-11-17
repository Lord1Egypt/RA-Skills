#!/bin/bash
# GIF Library Populator
# Downloads reaction GIFs from reliable open-source repos and other stable sources.
# Run: ./populate.sh
# All GIFs go under ~/.openclaw/workspace/gif-library/

set -euo pipefail

BASE="${GIF_LIBRARY_DIR:-$HOME/.openclaw/workspace/gif-library}"
GIF_DIR="$BASE/gifs"
INDEX="$BASE/index.json"

mkdir -p "$GIF_DIR"

download_if_missing() {
    local url="$1"
    local filename="$2"
    local dest="$GIF_DIR/$filename"
    if [ -f "$dest" ] && [ -s "$dest" ]; then
        echo "  ✓ Already have: $filename"
        return 0
    fi
    echo "  ↓ Downloading: $filename"
    if curl -sL --max-time 30 "$url" -o "$dest" 2>/dev/null; then
        local size
        size=$(stat -c%s "$dest" 2>/dev/null || stat -f%z "$dest" 2>/dev/null || echo "0")
        if [ "$size" -gt 100 ]; then
            echo "    Downloaded: $size bytes"
            return 0
        fi
    fi
    echo "    ✗ Failed or too small"
    rm -f "$dest"
    return 1
}

echo "=== Populating GIF Library ==="
echo "Directory: $GIF_DIR"
echo ""

# --- Celebration / Win ---
download_if_missing \
    "https://raw.githubusercontent.com/hhff/reaction/master/WIN.gif" \
    "celebration.gif" || true

# --- Excited / Hyped ---
download_if_missing \
    "https://raw.githubusercontent.com/hhff/reaction/master/Partyyy.gif" \
    "excited.gif" || true

# --- Deal With It / Cool ---
download_if_missing \
    "https://raw.githubusercontent.com/hhff/reaction/master/Perfect%20Gifs.gif" \
    "deal-with-it.gif" || true

# --- Saluting ---
download_if_missing \
    "https://media.giphy.com/media/XreQmk7ETCakw/giphy.gif" \
    "salute.gif" || true

# --- Thinking ---
download_if_missing \
    "https://media.giphy.com/media/3o7aTskHEUdgCQAXde/giphy.gif" \
    "thinking.gif" || true

# --- Respectful Nod ---
download_if_missing \
    "https://media.giphy.com/media/l46Cy1rHbQ92uuLXa/giphy.gif" \
    "nod-respect.gif" || true

# --- Facepalm ---
download_if_missing \
    "https://media.giphy.com/media/Q9aBxHn9i1bbO/giphy.gif" \
    "facepalm.gif" || true

# --- Waiting Patiently ---
download_if_missing \
    "https://media.giphy.com/media/l3V0dy1zqWqXyZBY0/giphy.gif" \
    "waiting-patiently.gif" || true

# --- Deep Dive / Research ---
download_if_missing \
    "https://media.giphy.com/media/26BRv0ThflsHCqDrG/giphy.gif" \
    "deep-dive.gif" || true

# --- Mind Blown ---
download_if_missing \
    "https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif" \
    "mind-blown.gif" || true

# --- Fist Bump ---
download_if_missing \
    "https://media.giphy.com/media/11sBLVxNs7o6NQ/giphy.gif" \
    "fist-bump.gif" || true

# --- Sorry ---
download_if_missing \
    "https://media.giphy.com/media/l2JehGbvVfFExWz SIGN1U/giphy.gif" \
    "sorry.gif" || true

# --- Coffee Cheers ---
download_if_missing \
    "https://media.giphy.com/media/xT9IgzoKnw2LL9Sf mail/photos/giphy.gif" \
    "coffee-cheers.gif" || true

# --- Bookmark / Remember ---
download_if_missing \
    "https://media.giphy.com/media/3o7btZQ1pS5JXjvUAg/giphy.gif" \
    "bookmark-this.gif" || true

# --- Pat on Back (we already have the test file) ---
# Create a placeholder for this until we find a good one
echo ""
echo "=== Summary ==="
count=$(ls -1 "$GIF_DIR"/*.gif 2>/dev/null | wc -l)
echo "Total GIFs in library: $count"
echo "Library ready at: $GIF_DIR"
