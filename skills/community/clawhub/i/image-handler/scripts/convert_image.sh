#!/bin/bash
# Convert image between formats

set -e

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <input> <output> [quality=85]"
    echo "Examples:"
    echo "  $0 photo.heic photo.jpg"
    echo "  $0 image.png image.webp 90"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"
QUALITY="${3:-85}"

if [[ ! -f "$INPUT" ]]; then
    echo "Error: Input file not found: $INPUT" >&2
    exit 1
fi

OUT_EXT="${OUTPUT##*.}"
OUT_EXT="${OUT_EXT,,}"

# Map extension to sips format
case "$OUT_EXT" in
    jpg|jpeg)
        FORMAT="jpeg"
        FORMAT_OPTS="-s formatOptions $QUALITY"
        ;;
    png)
        FORMAT="png"
        FORMAT_OPTS=""
        ;;
    gif)
        FORMAT="gif"
        FORMAT_OPTS=""
        ;;
    tiff|tif)
        FORMAT="tiff"
        FORMAT_OPTS=""
        ;;
    bmp)
        FORMAT="bmp"
        FORMAT_OPTS=""
        ;;
    webp|heic|heif)
        # sips doesn't support WebP/HEIC output, use ffmpeg
        ffmpeg -y -i "$INPUT" "$OUTPUT"
        echo "Converted: $INPUT -> $OUTPUT (via ffmpeg)"
        exit 0
        ;;
    *)
        echo "Error: Unsupported output format: $OUT_EXT" >&2
        exit 1
        ;;
esac

sips -s format "$FORMAT" $FORMAT_OPTS "$INPUT" --out "$OUTPUT" >/dev/null 2>&1

echo "Converted: $INPUT -> $OUTPUT"
ls -lh "$OUTPUT" | awk '{print "Output size:", $5}'