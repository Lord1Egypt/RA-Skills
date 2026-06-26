#!/usr/bin/env bash
# fetch_arxiv.sh — Download and extract arXiv paper source
#
# Usage: ./fetch_arxiv.sh <arxiv_url> <output_dir>
# Example: ./fetch_arxiv.sh https://arxiv.org/abs/1706.03762 /tmp/papyrus_paper

set -euo pipefail

ARXIV_URL="${1:-}"
OUTPUT_DIR="${2:-/tmp/papyrus_paper}"

if [ -z "$ARXIV_URL" ]; then
    echo "Usage: $0 <arxiv_url> <output_dir>"
    exit 1
fi

# Extract paper ID from URL (e.g., 1706.03762 from https://arxiv.org/abs/1706.03762)
PAPER_ID=$(echo "$ARXIV_URL" | grep -oE '[0-9]{4}\.[0-9]{4,5}(v[0-9]+)?' | head -1)
if [ -z "$PAPER_ID" ]; then
    echo "Error: Could not extract paper ID from URL: $ARXIV_URL"
    exit 1
fi

echo "📥 Fetching arXiv paper: $PAPER_ID"

mkdir -p "$OUTPUT_DIR"

# Download e-print source (LaTeX tar.gz)
SOURCE_URL="https://arxiv.org/e-print/${PAPER_ID}"
echo "   Source: $SOURCE_URL"
curl -sL "$SOURCE_URL" -o "$OUTPUT_DIR/source.tar.gz"

# Extract
echo "📦 Extracting..."
tar -xzf "$OUTPUT_DIR/source.tar.gz" -C "$OUTPUT_DIR" 2>/dev/null || true

# List contents
echo "📂 Contents:"
find "$OUTPUT_DIR" -maxdepth 2 -type f | sort | while read -r f; do
    size=$(wc -c < "$f" | tr -d ' ')
    rel="${f#$OUTPUT_DIR/}"
    printf "   %8s  %s\n" "$size b" "$rel"
done

echo "✅ Done. Source extracted to: $OUTPUT_DIR"
