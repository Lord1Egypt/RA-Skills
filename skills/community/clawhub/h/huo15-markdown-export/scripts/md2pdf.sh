#!/usr/bin/env bash
# md2pdf.sh — PDF 导出统一入口(优先 puppeteer,fallback pandoc)
#
# 大多数情况直接用 puppeteer 路线即可;只有需要 LaTeX 排版/学术 PDF 时才走 pandoc + xelatex。
#
# 用法:
#   ./md2pdf.sh <input.md> [output.pdf] [--engine puppeteer|pandoc] [--theme typora-newsprint]
#
# 透传给 md2pdf-puppet.js 的参数:--paper / --margin / --no-mermaid / --print-urls / --header / --footer

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

INPUT="${1:-}"
[[ -z "$INPUT" ]] && { echo "用法: md2pdf.sh <input.md> [output.pdf] [--engine puppeteer|pandoc] [--theme name]"; exit 1; }
shift || true

# 解析 engine
ENGINE="puppeteer"
ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --engine) ENGINE="$2"; shift 2 ;;
    *) ARGS+=("$1"); shift ;;
  esac
done

case "$ENGINE" in
  puppeteer)
    if [[ ! -d "$ROOT/node_modules" ]]; then
      echo "× node_modules 缺失,先跑: bash $SCRIPT_DIR/install-deps.sh" >&2
      exit 2
    fi
    exec node "$SCRIPT_DIR/md2pdf-puppet.js" "$INPUT" "${ARGS[@]}"
    ;;
  pandoc)
    command -v pandoc >/dev/null || { echo "× pandoc 未安装。macOS: brew install pandoc"; exit 2; }
    OUT="${ARGS[0]:-${INPUT%.md}.pdf}"
    [[ "${ARGS[0]:-}" == --* ]] || ARGS=("${ARGS[@]:1}") 2>/dev/null || true
    THEME="apple-tech"
    for ((i=0; i<${#ARGS[@]}; i++)); do
      [[ "${ARGS[$i]}" == "--theme" ]] && THEME="${ARGS[$((i+1))]}"
    done
    CSS="$ROOT/themes/${THEME}.css"
    [[ -f "$CSS" ]] || CSS="$ROOT/themes/typora-newsprint.css"

    if command -v weasyprint >/dev/null; then
      pandoc "$INPUT" -o "$OUT" --pdf-engine=weasyprint --css="$CSS" --highlight-style=tango --standalone
    elif command -v xelatex >/dev/null; then
      pandoc "$INPUT" -o "$OUT" --pdf-engine=xelatex -V CJKmainfont="PingFang SC" -V mainfont="Source Serif Pro" --highlight-style=tango
    else
      echo "× pandoc 模式需要 weasyprint 或 xelatex。建议: pip install weasyprint" >&2
      exit 2
    fi
    echo "✓ $OUT  (engine=pandoc theme=$THEME)"
    ;;
  *)
    echo "× 未知 engine: $ENGINE(可选 puppeteer|pandoc)"; exit 1 ;;
esac
