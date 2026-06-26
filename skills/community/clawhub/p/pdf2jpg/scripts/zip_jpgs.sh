#!/usr/bin/env bash
set -euo pipefail

pdf="${1:-}"
out="${2:-}"

if [[ -z "$pdf" ]]; then
  read -rp "PDF 文件名: " pdf
fi

if [[ ! -f "$pdf" ]]; then
  echo "文件不存在: $pdf" >&2
  exit 1
fi

base="${pdf%.*}"
zip_path="${out:-${base}-jpgs.zip}"

shopt -s nullglob
images=("${base}"-*.jpg)
shopt -u nullglob

if (( ${#images[@]} == 0 )); then
  echo "未找到图片: ${base}-*.jpg" >&2
  exit 1
fi

cd "$(dirname "$pdf")"
zip -q -j "$zip_path" "${images[@]}"
echo "$zip_path"
