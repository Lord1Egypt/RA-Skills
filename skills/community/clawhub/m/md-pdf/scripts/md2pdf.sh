#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  cat >&2 <<'USAGE'
Usage:
  bash scripts/md2pdf.sh <input.md> <output.pdf> [--defaults <yaml>]

Examples:
  bash scripts/md2pdf.sh doc.md doc.pdf
  bash scripts/md2pdf.sh doc.md doc.pdf --defaults assets/defaults/hifi.yaml
USAGE
  exit 1
fi

INPUT="$1"
OUTPUT="$2"
shift 2

if [[ ! -f "$INPUT" ]]; then
  echo "[ERROR] Input file not found: $INPUT" >&2
  exit 1
fi

if ! command -v pandoc >/dev/null 2>&1; then
  echo "[ERROR] pandoc not found. Run: bash scripts/install_deps_ubuntu.sh" >&2
  exit 1
fi

# XeLaTeX check is lightweight; pandoc will still report detailed errors later.
if ! command -v xelatex >/dev/null 2>&1; then
  echo "[ERROR] xelatex not found. Install texlive-xetex." >&2
  exit 1
fi

DEFAULTS_ARGS=()
EXTRA_ARGS=("$@")
for ((i=0; i<${#EXTRA_ARGS[@]}; i++)); do
  if [[ "${EXTRA_ARGS[$i]}" == "--defaults" ]]; then
    if [[ $((i+1)) -ge ${#EXTRA_ARGS[@]} ]]; then
      echo "[ERROR] --defaults requires a file path" >&2
      exit 1
    fi
    DEFAULTS_ARGS=("--defaults" "${EXTRA_ARGS[$((i+1))]}")
    break
  fi
done

if [[ ${#DEFAULTS_ARGS[@]} -gt 0 ]]; then
  pandoc "$INPUT" -o "$OUTPUT" "${DEFAULTS_ARGS[@]}"
else
  pandoc "$INPUT" -o "$OUTPUT" \
    --from=gfm+emoji+autolink_bare_uris+footnotes \
    --pdf-engine=xelatex \
    --toc \
    --number-sections \
    --highlight-style=tango \
    -V CJKmainfont="Noto Sans CJK SC" \
    -V mainfont="DejaVu Serif" \
    -V sansfont="DejaVu Sans" \
    -V monofont="DejaVu Sans Mono" \
    -V geometry:margin=2.2cm \
    -V fontsize=11pt \
    -V linestretch=1.2 \
    -V colorlinks=true \
    -V linkcolor=blue \
    -V urlcolor=blue
fi

echo "[OK] Generated PDF: $OUTPUT"
