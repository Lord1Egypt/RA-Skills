#!/bin/bash
# Get comprehensive image metadata

set -e

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <image>"
    exit 1
fi

IMAGE="$1"

if [[ ! -f "$IMAGE" ]]; then
    echo "Error: Image not found: $IMAGE" >&2
    exit 1
fi

EXT="${IMAGE##*.}"
EXT="${EXT,,}"

echo "=== Image: $IMAGE ==="
echo ""

# Basic file info
echo "--- File ---"
ls -lh "$IMAGE" | awk '{print "Size:", $5}'
echo ""

# Image properties
echo "--- Properties ---"
sips -g all "$IMAGE" 2>&1 | tail +2 || echo "Could not read image properties"
echo ""

# For SVG, show first few lines
if [[ "$EXT" == "svg" ]]; then
    echo "--- SVG Content (first 20 lines) ---"
    head -20 "$IMAGE"
fi