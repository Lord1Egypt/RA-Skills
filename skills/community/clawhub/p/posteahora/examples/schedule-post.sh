#!/usr/bin/env bash
# Upload media and schedule an Instagram reel for a future time.
set -euo pipefail

# 1. Upload the video and capture the returned public URL.
URL=$(posteahora upload ./reel.mp4 --json | node -e 'process.stdin.on("data",d=>{try{console.log(JSON.parse(d).publicUrl)}catch{}})')

# 2. Schedule the post.
posteahora post "New reel is up 🎬" \
  --to instagram:REPLACE_INSTAGRAM_ID \
  --post-type reel \
  --media "$URL" \
  --at 2026-07-20T09:00:00Z
