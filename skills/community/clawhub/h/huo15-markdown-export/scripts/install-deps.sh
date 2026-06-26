#!/usr/bin/env bash
# install-deps.sh — 一键装齐依赖
#
# - npm install(必装,渲染 + puppeteer + juice)
# - 检测 pandoc(导 docx 必需,可选)
# - 检测 weasyprint(pandoc 路线 PDF 用,可选)

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

cd "$ROOT"

echo "→ 装 node 依赖(markdown-it / puppeteer / juice / katex / highlight.js / mermaid)..."
if [[ ! -f package.json ]]; then echo "× 找不到 package.json"; exit 1; fi
if command -v npm >/dev/null; then
  npm install --no-audit --no-fund --loglevel=error
else
  echo "× 没装 npm。装 node: https://nodejs.org/  或 brew install node"
  exit 2
fi
echo "✓ node 依赖装完"

echo
echo "→ 检测 pandoc(导 Word docx 用)..."
if command -v pandoc >/dev/null; then
  echo "  ✓ pandoc $(pandoc --version | head -1 | awk '{print $2}')"
else
  echo "  ⚠ 未装 pandoc(只影响 md2docx)"
  echo "    macOS:  brew install pandoc"
  echo "    Ubuntu: sudo apt install pandoc"
fi

echo
echo "→ 检测 weasyprint(pandoc 路线 PDF 用,可选)..."
if command -v weasyprint >/dev/null; then
  echo "  ✓ weasyprint"
else
  echo "  ⚠ 未装 weasyprint(只影响 md2pdf --engine pandoc;默认 puppeteer 路线不需要)"
  echo "    pip install weasyprint"
fi

echo
echo "全部就绪。试一发:"
echo "  node $SCRIPT_DIR/md2html.js $ROOT/examples/sample.md"
echo "  node $SCRIPT_DIR/md2pdf-puppet.js $ROOT/examples/sample.md"
