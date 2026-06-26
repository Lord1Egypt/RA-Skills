#!/usr/bin/env bash
# md2slide.sh — Markdown → Marp スライド変換（Mermaid + Tailwind CSS対応）
# Usage: md2slide.sh <input.md> [format: pdf|pptx|html] [output_dir]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
THEME_DIR="$(cd "${SCRIPT_DIR}/../theme" && pwd)"
INPUT="${1:?Usage: md2slide.sh <input.md> [pdf|pptx|html] [output_dir]}"
FORMAT="${2:-pdf}"
OUTDIR="${3:-.}"
BASENAME="$(basename "${INPUT}" .md)"
OUTPUT="${OUTDIR}/${BASENAME}.${FORMAT}"

mkdir -p "${OUTDIR}"

TMPMD="$(mktemp /tmp/marp_XXXXXX.md)"
IMGDIR="$(mktemp -d /tmp/marp_img_XXXXXX)"

# Pre-process: mermaid blocks → PNG
python3 "${SCRIPT_DIR}/mermaid_preprocess.py" "${INPUT}" "${TMPMD}" "${IMGDIR}"

# Inject Tailwind CSS script tags after frontmatter (if not already present)
if ! grep -q 'tailwindcss' "${TMPMD}"; then
  python3 -c "
import re
content = open('${TMPMD}').read()
tailwind_tags = '''<script src=\"${THEME_DIR}/js/tailwindcss-3.0.16.js\"></script>
<script src=\"${THEME_DIR}/js/tailwind.config.js\"></script>
'''
# Insert after frontmatter closing ---
match = re.match(r'(---\n.*?\n---\n)', content, re.DOTALL)
if match:
    pos = match.end()
    content = content[:pos] + '\n' + tailwind_tags + '\n' + content[pos:]
else:
    content = tailwind_tags + '\n' + content
open('${TMPMD}', 'w').write(content)
"
fi

# Convert with Marp
case "${FORMAT}" in
  pdf)  marp "${TMPMD}" --pdf -o "${OUTPUT}" --allow-local-files --html --theme-set "${THEME_DIR}/frexida.css" < /dev/null ;;
  pptx) marp "${TMPMD}" --pptx -o "${OUTPUT}" --allow-local-files --html --theme-set "${THEME_DIR}/frexida.css" < /dev/null ;;
  html) marp "${TMPMD}" -o "${OUTPUT}" --allow-local-files --html --theme-set "${THEME_DIR}/frexida.css" < /dev/null ;;
  *)    echo "Unknown format: ${FORMAT}"; exit 1 ;;
esac

rm -rf "${TMPMD}" "${IMGDIR}"
echo "✅ ${OUTPUT}"
