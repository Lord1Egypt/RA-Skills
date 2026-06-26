#!/usr/bin/env bash
# Check required binaries for openclaw-video-editor.
# Exits 0 if all are available, 1 if any are missing.

set -u

missing=0
required=(ffmpeg ffprobe python3)

for bin in "${required[@]}"; do
  if command -v "$bin" >/dev/null 2>&1; then
    version=$("$bin" --version 2>&1 | head -n 1 || echo "version unknown")
    printf "  ok   %-9s %s\n" "$bin" "$version"
  else
    printf "  miss %-9s not found in PATH\n" "$bin"
    missing=1
  fi
done

if [ "$missing" -eq 1 ]; then
  echo
  echo "One or more required binaries are missing." >&2
  echo "Install via your platform package manager (apt, brew, choco, etc.)." >&2
  exit 1
fi

echo
echo "All dependencies satisfied."
exit 0
