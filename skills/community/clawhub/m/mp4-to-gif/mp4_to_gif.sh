#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: $0 -i INPUT [-o OUTPUT] [-w WIDTH] [-f FPS]"
    echo "  -i  Input MP4 file (required)"
    echo "  -o  Output GIF file (default: input with .gif extension)"
    echo "  -w  Width in pixels (default: 480)"
    echo "  -f  Frames per second (default: 15)"
    exit 1
}

WIDTH=480
FPS=15
INPUT=""
OUTPUT=""

while getopts "i:o:w:f:h" opt; do
    case $opt in
        i) INPUT="$OPTARG" ;;
        o) OUTPUT="$OPTARG" ;;
        w) WIDTH="$OPTARG" ;;
        f) FPS="$OPTARG" ;;
        *) usage ;;
    esac
done

[ -z "$INPUT" ] && usage
[ ! -f "$INPUT" ] && echo "File not found: $INPUT" >&2 && exit 1
[ -z "$OUTPUT" ] && OUTPUT="${INPUT%.*}.gif"

PALETTE=$(mktemp /tmp/palette_XXXXXX.png)
trap 'rm -f "$PALETTE"' EXIT

echo "Generating palette..."
ffmpeg -y -i "$INPUT" -vf "fps=$FPS,scale=${WIDTH}:-1:flags=lanczos,palettegen=stats_mode=diff" "$PALETTE" 2>/dev/null

echo "Converting to GIF..."
ffmpeg -y -i "$INPUT" -i "$PALETTE" -lavfi "fps=$FPS,scale=${WIDTH}:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" "$OUTPUT" 2>/dev/null

if [ -f "$OUTPUT" ]; then
    SIZE=$(du -h "$OUTPUT" | cut -f1)
    echo "Done: $OUTPUT ($SIZE)"
else
    echo "Conversion failed." >&2
    exit 1
fi
