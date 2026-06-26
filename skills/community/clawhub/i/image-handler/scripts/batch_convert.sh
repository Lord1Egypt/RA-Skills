#!/bin/bash
# Batch convert all images in a directory

set -e

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <input_dir> <output_format> [output_dir]"
    echo "Examples:"
    echo "  $0 ./photos jpg"
    echo "  $0 ./heics jpg ./converted"
    echo "  $0 ./images png"
    exit 1
fi

INPUT_DIR="$1"
FORMAT="${2,,}"
OUTPUT_DIR="${3:-$INPUT_DIR/converted}"

if [[ ! -d "$INPUT_DIR" ]]; then
    echo "Error: Directory not found: $INPUT_DIR" >&2
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# Map format
case "$FORMAT" in
    jpg|jpeg)
        SIPS_FORMAT="jpeg"
        EXT="jpg"
        ;;
    png)
        SIPS_FORMAT="png"
        EXT="png"
        ;;
    gif)
        SIPS_FORMAT="gif"
        EXT="gif"
        ;;
    tiff|tif)
        SIPS_FORMAT="tiff"
        EXT="tiff"
        ;;
    webp|heic|heif)
        echo "WebP/HEIC batch conversion requires ffmpeg"
        echo "Run: for f in $INPUT_DIR/*; do ffmpeg -i \"\$f\" \"${OUTPUT_DIR}/\$(basename \"\${f%.*}\").${FORMAT}\"; done"
        exit 1
        ;;
    *)
        echo "Error: Unsupported format: $FORMAT" >&2
        exit 1
        ;;
esac

COUNT=0
for f in "$INPUT_DIR"/*.{jpg,jpeg,png,gif,tiff,tif,bmp,heic,heif,webp} 2>/dev/null; do
    [[ -f "$f" ]] || continue

    BASENAME=$(basename "${f%.*}")
    OUTPUT="$OUTPUT_DIR/${BASENAME}.${EXT}"

    sips -s format "$SIPS_FORMAT" "$f" --out "$OUTPUT" >/dev/null 2>&1
    echo "Converted: $f -> $OUTPUT"
    ((COUNT++))
done

echo ""
echo "Done! Converted $COUNT images to $OUTPUT_DIR"