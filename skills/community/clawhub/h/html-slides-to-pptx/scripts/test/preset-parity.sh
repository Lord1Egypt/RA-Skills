#!/bin/bash
# preset-parity.sh — 预设与默认 theme.css 的 CSS 变量名集合一致性校验
# 任何漂移(新增/漏写/拼写差异)都会以非零退出。改主题变量时必须 5 套预设同步。
set -euo pipefail
DIR="$(cd "$(dirname "$0")/../.." && pwd)/assets"
DEFAULT="$DIR/theme.css"
fail=0

vars_of() { grep -oE '^\s*--[a-z0-9-]+\s*:' "$1" | tr -d ' :' | sort; }

for preset in "$DIR"/presets/*.css; do
  name="$(basename "$preset")"
  if diff <(vars_of "$DEFAULT") <(vars_of "$preset") > /dev/null; then
    echo "✅ $name 变量名与默认一致"
  else
    echo "❌ $name 变量名漂移:"
    diff <(vars_of "$DEFAULT") <(vars_of "$preset") | sed 's/^/   /'
    fail=1
  fi
done
exit $fail
