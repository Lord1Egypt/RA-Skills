#!/usr/bin/env bash
# #4b 指针死链的正反例：死链必须判 FAIL（退出码 1），指针齐全必须放过（退出码 0）。
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CHECK="$ROOT/check.py"
TMP=$(mktemp -d)
trap 'rm -rf -- "$TMP"' EXIT

make_skill() {
  local dir="$1"
  mkdir -p "$dir/references"
  cat > "$dir/SKILL.md" <<'MD'
---
name: pointer-fixture
description: 用于验证死链判定的夹具 skill。当需要检查指针是否真实存在时使用。
---

# 指针夹具

细节见 [references/detail.md](references/detail.md)。
MD
}

echo '== 死链应判 FAIL =='
make_skill "$TMP/dead"
if python3 "$CHECK" "$TMP/dead" >/dev/null 2>&1; then
  echo '  ❌ 指针指向不存在的文件却通过了体检'
  exit 1
fi
# 体检失败时退出码非零，先落盘再匹配，避免 pipefail 把正常失败当成管道错误。
DEAD_OUTPUT=$(python3 "$CHECK" "$TMP/dead" 2>&1 || true)
if ! printf '%s' "$DEAD_OUTPUT" | grep -q '指针指向不存在的文件'; then
  echo '  ❌ 失败原因里没有指出死链'
  exit 1
fi
echo '  ✅ 死链被判失败并指名'

echo '== 指针齐全应放过 =='
make_skill "$TMP/alive"
printf '%s\n' '# 细节' '真实存在的参考内容。' > "$TMP/alive/references/detail.md"
if ! python3 "$CHECK" "$TMP/alive" >/dev/null 2>&1; then
  echo '  ❌ 指针齐全的 skill 被误判失败'
  python3 "$CHECK" "$TMP/alive" 2>&1 | grep '✗' || true
  exit 1
fi
echo '  ✅ 指针齐全被放过'

echo '== 教学示例路径不应被当成指针 =='
mkdir -p "$TMP/inline"
printf '%s\n' \
  '---' \
  'name: inline-example' \
  'description: 验证教学示例路径不会误报。当需要检查指针解析边界时使用。' \
  '---' \
  '' \
  'Example: `scripts/rotate_pdf.py` is a hypothetical script.' > "$TMP/inline/SKILL.md"
if ! python3 "$CHECK" "$TMP/inline" >/dev/null 2>&1; then
  echo '  ❌ 教学示例路径被误判为死链'
  exit 1
fi
echo '  ✅ 教学示例路径被放过'

echo '== .json 指针不应被截成 .js =='
mkdir -p "$TMP/json/references"
printf '%s\n' '{}' > "$TMP/json/references/rules.json"
printf '%s\n' \
  '---' \
  'name: json-fixture' \
  'description: 验证扩展名前缀不会截断指针。当需要检查 .json 指针时使用。' \
  '---' \
  '' \
  '规则见 [references/rules.json](references/rules.json)。' > "$TMP/json/SKILL.md"
if ! JSON_OUTPUT=$(python3 "$CHECK" "$TMP/json" 2>&1); then
  echo '  ❌ 存在的 .json 指针被误判为死链'
  printf '%s\n' "$JSON_OUTPUT" | grep '✗' || true
  exit 1
fi
echo '  ✅ .json 指针完整识别'

echo '== 越根路径必须判 FAIL =='
mkdir -p "$TMP/escape"
printf '%s\n' \
  '---' \
  'name: escape-fixture' \
  'description: 验证越根路径不会被放过。当需要检查资源作用域时使用。' \
  '---' \
  '' \
  '[越界资源](references/../../outside.md)' > "$TMP/escape/SKILL.md"
if ESCAPE_OUTPUT=$(python3 "$CHECK" "$TMP/escape" 2>&1); then
  echo '  ❌ 越根路径被错误放行'
  exit 1
fi
if ! printf '%s' "$ESCAPE_OUTPUT" | grep -q '越过 skill 根目录'; then
  echo '  ❌ 越根路径失败原因未说明作用域越界'
  exit 1
fi
echo '  ✅ 越根路径被阻断'

echo
echo '指针死链正反例验证通过。'
