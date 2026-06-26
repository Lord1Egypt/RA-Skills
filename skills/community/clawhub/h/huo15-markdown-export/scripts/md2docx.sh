#!/usr/bin/env bash
# md2docx.sh — markdown → Word docx (走 Pandoc)
#
# 默认带火一五品牌的 reference.docx(若存在),否则走 Pandoc 内置默认。
# 自动加 TOC、保留中文字体设置。
#
# 用法:
#   ./md2docx.sh <input.md> [output.docx] [--no-toc] [--reference path/to/custom.docx]

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

INPUT="${1:-}"
[[ -z "$INPUT" ]] && { echo "用法: md2docx.sh <input.md> [output.docx] [--no-toc] [--reference custom.docx]"; exit 1; }
shift

OUT=""
TOC=1
REFDOC="$ROOT/templates/reference.docx"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-toc) TOC=0; shift ;;
    --reference) REFDOC="$2"; shift 2 ;;
    --*) echo "未知选项: $1"; exit 1 ;;
    *) OUT="$1"; shift ;;
  esac
done

OUT="${OUT:-${INPUT%.md}.docx}"

command -v pandoc >/dev/null || {
  cat >&2 <<EOF
× pandoc 未安装。
  macOS:  brew install pandoc
  Ubuntu: sudo apt install pandoc
  其他:   https://pandoc.org/installing.html
EOF
  exit 2
}

PANDOC_ARGS=(--standalone --from=gfm+footnotes+task_lists --to=docx)
[[ $TOC -eq 1 ]] && PANDOC_ARGS+=(--toc --toc-depth=3)
[[ -f "$REFDOC" ]] && PANDOC_ARGS+=(--reference-doc="$REFDOC")

pandoc "${PANDOC_ARGS[@]}" "$INPUT" -o "$OUT"

echo "✓ $OUT  (toc=$TOC  reference=${REFDOC#$ROOT/})"
[[ -f "$REFDOC" ]] || echo "  提示: 没找到 templates/reference.docx,用了 Pandoc 内置默认。自定义品牌样式见 templates/README.md"
