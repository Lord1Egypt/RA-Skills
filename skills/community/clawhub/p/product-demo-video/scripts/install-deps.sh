#!/bin/bash
# Install all dependencies for product demo video creation
set -e

echo "📦 Installing dependencies..."

# Puppeteer (headless Chrome automation)
npm i -g puppeteer 2>/dev/null && echo "✅ Puppeteer" || echo "⚠️ Puppeteer (may already exist)"

# edge-tts (Microsoft Neural TTS - free)
pip3 install edge-tts 2>/dev/null && echo "✅ edge-tts" || echo "⚠️ edge-tts"

# Pillow (text overlays)
pip3 install Pillow 2>/dev/null && echo "✅ Pillow" || echo "⚠️ Pillow (may already exist)"

# FFmpeg (static build if not available)
if ! command -v ffmpeg &>/dev/null; then
  echo "📥 Downloading FFmpeg static build..."
  curl -sL https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -o /tmp/ffmpeg.tar.xz
  tar xf /tmp/ffmpeg.tar.xz -C /tmp/
  cp /tmp/ffmpeg-*-amd64-static/ffmpeg /usr/local/bin/
  cp /tmp/ffmpeg-*-amd64-static/ffprobe /usr/local/bin/
  rm -rf /tmp/ffmpeg.tar.xz /tmp/ffmpeg-*-amd64-static
  echo "✅ FFmpeg"
else
  echo "✅ FFmpeg (already installed)"
fi

# Fonts for text overlays
if ! fc-list | grep -qi "noto.*sans.*bold" 2>/dev/null; then
  if command -v dnf &>/dev/null; then
    dnf install -y google-noto-sans-fonts 2>/dev/null && echo "✅ Noto Sans fonts"
  elif command -v apt-get &>/dev/null; then
    apt-get install -y fonts-noto-core 2>/dev/null && echo "✅ Noto Sans fonts"
  fi
else
  echo "✅ Noto Sans fonts (already installed)"
fi

# Chromium
if ! command -v chromium-browser &>/dev/null && ! command -v google-chrome &>/dev/null; then
  echo "⚠️ Chromium/Chrome not found. Install manually:"
  echo "   dnf install -y chromium  # RHEL/Rocky"
  echo "   apt install -y chromium  # Debian/Ubuntu"
else
  echo "✅ Chromium"
fi

echo ""
echo "🎬 All dependencies ready!"
