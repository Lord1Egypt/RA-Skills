#!/usr/bin/env sh
# Usage: transcode_mp3.sh INPUT OUTPUT.mp3
set -e
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 INPUT OUTPUT.mp3" >&2
  exit 1
fi
ffmpeg -y -i "$1" -vn -acodec libmp3lame -q:a 2 "$2"
