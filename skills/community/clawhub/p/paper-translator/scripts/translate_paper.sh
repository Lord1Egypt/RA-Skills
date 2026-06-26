#!/bin/bash
set -euo pipefail
INPUT="${1:-}"
[[ -z "$INPUT" ]] && { echo "Usage: $0 <input.pdf>"; exit 1; }
[[ ! -f "$INPUT" ]] && { echo "File not found: $INPUT"; exit 1; }

command -v uv &>/dev/null || { echo "Installing uv..."; curl -Ls https://astral.sh/uv/install.sh | sh; }
command -v pdf2zh_next &>/dev/null || { echo "Installing pdf2zh-next..."; uv tool install pdf2zh-next; }

# cd to input dir so pdf2zh_next outputs there
cd "$(dirname "$INPUT")"
BASENAME="$(basename "$INPUT" .pdf)"

echo "📄 Translating: $(basename "$INPUT")"
pdf2zh_next "$INPUT" --lang-in en --lang-out zh --qps 10 --pool-max-workers 100 "${@:2}"

# Check result in current dir (input dir)
[[ ! -f "${BASENAME}.zh.mono.pdf" && ! -f "${BASENAME}.zh.dual.pdf" ]] && {
  echo "❌ No output file found in $(pwd)"
  exit 1
}

echo "✅ Done"
for f in "${BASENAME}.zh.mono.pdf" "${BASENAME}.zh.dual.pdf" "${BASENAME}.zh.glossary.csv"; do
  [[ -f "$f" ]] && echo "  📎 $f ($(du -h "$f" | cut -f1))"
done
