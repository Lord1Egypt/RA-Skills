#!/usr/bin/env bash

export SUBSCUT_API_BASE_URL="https://subscut.com"
export SUBSCUT_API_KEY="subscut_your_api_key"

# Basic usage — dynamic reframing, viral captions, 5 clips
npm --prefix .agents/skills/generate-podcast-clips run generate-podcast-clips -- \
  --video-url "https://example.com/podcast.mp4" \
  --max-clips 5 \
  --clip-style viral \
  --format dynamic \
  --captions true

# Hook frame format with title cards, longer clips
npm --prefix .agents/skills/generate-podcast-clips run generate-podcast-clips -- \
  --video-url "https://example.com/interview.mp4" \
  --max-clips 3 \
  --clip-style clean \
  --format hook_frame \
  --min-clip-duration 30 \
  --max-clip-duration 60 \
  --captions true
