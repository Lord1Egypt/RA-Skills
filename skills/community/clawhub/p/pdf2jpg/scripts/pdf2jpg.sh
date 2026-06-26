#!/usr/bin/env bash
set -euo pipefail

pdf="${1:-}"
first="${2:-}"
last="${3:-}"

if [[ -z "$pdf" ]]; then
  read -rp "PDF 文件名: " pdf
fi

if [[ ! -f "$pdf" ]]; then
  echo "文件不存在: $pdf" >&2
  exit 1
fi

if ! command -v pdftoppm >/dev/null 2>&1; then
  echo "缺少依赖: pdftoppm（请安装 poppler-utils）" >&2
  exit 1
fi

out_prefix="${pdf%.*}"
cmd=(pdftoppm -jpeg -jpegopt quality=85,optimize=y,progressive=y)
[[ -n "$first" ]] && cmd+=(-f "$first")
[[ -n "$last" ]] && cmd+=(-l "$last")
cmd+=("$pdf" "$out_prefix")
"${cmd[@]}"
