#!/usr/bin/env bash
# pandoc-convert.sh — Quick document conversion wrapper
# Usage: pandoc-convert.sh <input> <output> [options...]
#
# Examples:
#   pandoc-convert.sh report.md report.docx
#   pandoc-convert.sh slides.md slides.pptx --toc
#   pandoc-convert.sh readme.md readme.pdf --pdf-engine xelatex

set -euo pipefail

INPUT="${1:?Usage: pandoc-convert.sh <input> <output> [options...]}"
OUTPUT="${2:?Usage: pandoc-convert.sh <input> <output> [options...]}"
shift 2

# Auto-detect standalone for non-fragment formats
STANDALONE=false
case "$OUTPUT" in
  *.docx|*.odt|*.epub|*.epub3|*.epub2|*.pptx|*.pdf|*.rtf|*.icml)
    STANDALONE=true
    ;;
  *.html|*.htm)
    if [[ " $@ " != *" -s "* ]] && [[ " $@ " != *" --standalone "* ]] && [[ " $@ " != *" --embed-resources "* ]]; then
      STANDALONE=true
    fi
    ;;
esac

PANDOC_OPTS=()
if $STANDALONE; then
  PANDOC_OPTS+=("-s")
fi

# Auto-add PDF engine if none specified
if [[ "$OUTPUT" == *.pdf ]]; then
  if [[ " $@ " != *" --pdf-engine "* ]]; then
    if command -v xelatex &>/dev/null; then
      PANDOC_OPTS+=("--pdf-engine=xelatex")
    elif command -v lualatex &>/dev/null; then
      PANDOC_OPTS+=("--pdf-engine=lualatex")
    fi
  fi
fi

PANDOC_OPTS+=("$@")
pandoc "$INPUT" -o "$OUTPUT" "${PANDOC_OPTS[@]}"
echo "✅ Converted: $INPUT → $OUTPUT"
