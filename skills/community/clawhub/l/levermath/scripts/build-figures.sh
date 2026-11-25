#!/usr/bin/env bash
# 将基础模板的 TikZ 源编译两遍，再把 PDF 转成可内联的 SVG。
set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p build/figures src/assets/figures

for tex in templates/basic/figures/*.tex; do
  name=$(basename "$tex" .tex)
  for _ in 1 2; do
    xelatex -interaction=nonstopmode -halt-on-error \
      -output-directory=build/figures "$tex" >/dev/null
  done
  pdftocairo -svg "build/figures/$name.pdf" "src/assets/figures/$name.svg"
  sed -i '1{/<?xml/d;}' "src/assets/figures/$name.svg"
  printf '%s -> %s\n' "$tex" "src/assets/figures/$name.svg"
done
