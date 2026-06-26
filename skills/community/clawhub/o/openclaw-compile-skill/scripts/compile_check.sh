#!/bin/bash
# compile_check.sh — 中转站编译文档自审脚本 v2.4
# 用法：bash compile_check.sh "<中转站文件绝对路径>"
# 输出：逐项 ✅/❌ + 最终 PASS/FAIL
# Maintainer: update this script when checklist rules change.

set -u

VAULT="${OPENCLAW_VAULT:-$(pwd)}"
RAW_DIR="${COMPILE_RAW_DIR:-$VAULT/Knowledge/原材料仓库}"
TRANSIT_DIR="${COMPILE_TRANSIT_DIR:-$VAULT/Knowledge/中转站}"
TRANSIT_FILE="${1:-}"
ERRORS=0
TOTAL=0

if [ "$#" -gt 0 ]; then
  shift
fi
while [ "$#" -gt 0 ]; do
  case "$1" in
    --vault)
      VAULT="$2"
      RAW_DIR="${COMPILE_RAW_DIR:-$VAULT/Knowledge/原材料仓库}"
      TRANSIT_DIR="${COMPILE_TRANSIT_DIR:-$VAULT/Knowledge/中转站}"
      shift 2 ;;
    *)
      echo "未知参数: $1"
      exit 1 ;;
  esac
done

if [ -z "${TRANSIT_FILE:-}" ]; then
  echo "用法：bash compile_check.sh \"<中转站文件绝对路径>\""
  exit 1
fi

if [ ! -f "$TRANSIT_FILE" ]; then
  echo "❌ 文件不存在：$TRANSIT_FILE"
  exit 1
fi

FILENAME=$(basename "$TRANSIT_FILE" .md)

# === 提取 frontmatter（第一个 --- 到第二个 --- 之间） ===
FM=$(awk '/^---$/{n++; next} n==1{print} n>=2{exit}' "$TRANSIT_FILE")
BODY=$(awk '/^---$/{n++; next} n>=2{print}' "$TRANSIT_FILE")

# 从 frontmatter 提取字段值（去引号、去首尾空格）
get_fm() {
  local key="$1"
  echo "$FM" | grep -m1 "^${key}:" | sed "s/^${key}:[[:space:]]*//" | sed 's/^"//;s/"$//' | sed "s/^'//;s/'$//" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' || echo ""
}

# 从 frontmatter 提取原始行（不去引号）
get_fm_raw() {
  local key="$1"
  echo "$FM" | grep -m1 "^${key}:" || echo ""
}

TYPE=$(get_fm "type")
STATUS=$(get_fm "status")
AUTHOR=$(get_fm "author")
SOURCE=$(get_fm "source")
ORIGINAL_RAW=$(get_fm_raw "original")
ORIGINAL=$(get_fm "original" | sed 's/\\//g')
CREATED=$(get_fm "created")
COMPILED_BY_RAW=$(get_fm_raw "compiled_by")
COMPILED_BY=$(get_fm "compiled_by")

check() {
  TOTAL=$((TOTAL + 1))
  local label="$1"
  local pass="$2"
  local detail="${3:-}"
  if [ "$pass" = "1" ]; then
    echo "✅ $label"
  else
    ERRORS=$((ERRORS + 1))
    if [ -n "$detail" ]; then
      echo "❌ $label ($detail)"
    else
      echo "❌ $label"
    fi
  fi
}

normalize_title_for_compare() {
  printf '%s' "$1" \
    | sed 's/[“”]/"/g; s/[‘’]/'\''/g; s/[：]/:/g; s/[，]/,/g; s/[—–－]/-/g' \
    | sed 's/[[:space:]]\+/ /g; s/^[[:space:]]*//; s/[[:space:]]*$//'
}

echo "=== 编译自审：$FILENAME ==="
echo ""

# =============================================
echo "--- Frontmatter ---"
# =============================================

# 1. type = compiled
check "type: compiled" "$([ "$TYPE" = "compiled" ] && echo 1 || echo 0)" "当前: $TYPE"

# 2. status = waiting
check "status: waiting" "$([ "$STATUS" = "waiting" ] && echo 1 || echo 0)" "当前: $STATUS"

# 3. author 非空且 @ 开头
if [ -n "$AUTHOR" ] && [[ "$AUTHOR" == @* ]]; then
  check "author: $AUTHOR" "1"
elif [ -n "$AUTHOR" ]; then
  check "author: $AUTHOR" "0" "应 @开头"
else
  check "author 为空" "0" "必填"
fi

# 4. source 非空
check "source 非空" "$([ -n "$SOURCE" ] && echo 1 || echo 0)"

raw_rel_prefix="$RAW_DIR"
case "$raw_rel_prefix" in
  "$VAULT"/*)
    raw_rel_prefix="${raw_rel_prefix#$VAULT/}" ;;
esac
transit_rel_prefix="$TRANSIT_DIR"
case "$transit_rel_prefix" in
  "$VAULT"/*)
    transit_rel_prefix="${transit_rel_prefix#$VAULT/}" ;;
esac

# 5. original 非空且格式为带路径 wikilink
if echo "$ORIGINAL" | grep -q '^\[\[.*\]\]$'; then
  check "original 带路径格式" "1"
elif [ -n "$ORIGINAL" ]; then
  check "original 格式错误" "0" "应为带路径 wikilink，当前: $ORIGINAL"
else
  check "original 为空" "0" "必填"
fi

# 6. created 非空
check "created 非空" "$([ -n "$CREATED" ] && echo 1 || echo 0)"

# 7. compiled_by 为带引号的非空字符串
if echo "$COMPILED_BY_RAW" | grep -qE '^compiled_by:[[:space:]]*"[^"]+"[[:space:]]*$'; then
  check "compiled_by: \"$COMPILED_BY\"" "1"
elif [ -n "$COMPILED_BY" ]; then
  check "compiled_by 值存在但未加引号" "0" "应为 compiled_by: \"$COMPILED_BY\""
else
  check "compiled_by 错误" "0" "当前为空，必须是带引号的非空字符串"
fi

# 8. tags 存在，允许空数组
TAGS_LINE=$(echo "$FM" | grep -m1 "^tags:" || echo "")
if [ -z "$TAGS_LINE" ]; then
  check "tags 存在" "0" "缺失"
else
  check "tags 存在（允许 []）" "1"
fi

# 9. keywords 非空数组
KW_LINE=$(echo "$FM" | grep -m1 "^keywords:" || echo "")
if [ -z "$KW_LINE" ]; then
  check "keywords 存在" "0" "缺失"
elif echo "$KW_LINE" | grep -qE '^\s*keywords:\s*\[\s*\]\s*$'; then
  check "keywords 非空" "0" "为空数组 []"
else
  check "keywords 非空" "1"
fi

# 10. related_wiki 存在且扁平（无 [["  嵌套）
RW_LINE=$(echo "$FM" | grep -m1 "^related_wiki:" || echo "")
if [ -z "$RW_LINE" ]; then
  check "related_wiki 存在" "0" "缺失"
elif echo "$RW_LINE" | grep -q '\[\["'; then
  check "related_wiki 扁平" "0" '检测到嵌套 [["'
else
  check "related_wiki 存在且扁平" "1"
fi

echo ""

# =============================================
echo "--- YAML 格式 ---"
# =============================================

# 11. 第一行是 ---
FIRST_LINE=$(head -1 "$TRANSIT_FILE")
check "第一行 ---" "$([ "$FIRST_LINE" = "---" ] && echo 1 || echo 0)" "当前: $FIRST_LINE"

# 12. frontmatter 内部无 <!-- --> 注释
if echo "$FM" | grep -q '<!--'; then
  # 找到注释所在行号（在 frontmatter 内部）
  COMMENT_LINE=$(echo "$FM" | grep -n '<!--' | head -1 | cut -d: -f1)
  check "frontmatter 无注释" "0" "行 ~$((COMMENT_LINE + 1))"
else
  check "frontmatter 无注释" "1"
fi

# 13. 无非标准字段
WHITELIST="type|status|source|author|original|created|compiled_by|tags|keywords|related_wiki|graduated_to|pending_topics"
NON_STANDARD=$(echo "$FM" | grep -E '^[a-zA-Z_]+:' | sed 's/:.*//' | grep -vE "^($WHITELIST)$" || echo "")
if [ -z "$NON_STANDARD" ]; then
  check "无非标准字段" "1"
else
  check "无非标准字段" "0" "发现: $NON_STANDARD"
fi

echo ""

# =============================================
echo "--- 标题 ---"
# =============================================

# 14. H1 存在且以文件名开头（允许英文标题后接中文副标题）
H1=$(echo "$BODY" | grep -m1 '^# ' | sed 's/^# //' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' || echo "")
if [ -z "$H1" ]; then
  check "H1 存在" "0" "未找到 # 标题"
else
  H1_NORM="$(normalize_title_for_compare "$H1")"
  FILENAME_NORM="$(normalize_title_for_compare "$FILENAME")"
  case "$H1_NORM" in
    "$FILENAME_NORM"*)
      check "H1 以文件名开头" "1" ;;
    *)
      check "H1 以文件名开头" "0" "H1: $H1 | 文件名: $FILENAME" ;;
  esac
fi

# 15. 英文标题含中文副标题
# 检测 H1 是否以英文开头（ASCII 字母），如果是则检查是否含中文字符
if [ -n "$H1" ] && echo "$H1" | grep -qE '^[A-Za-z]'; then
  if echo "$H1" | grep -qP '[\x{4e00}-\x{9fff}]' 2>/dev/null || echo "$H1" | grep -q '[一-龥]' 2>/dev/null; then
    check "英文标题含中文副标题" "1"
  else
    check "英文标题含中文副标题" "0" "英文标题必须加中文副标题。格式：英文原标题 — 中文概述（你自己写，10-20字）"
  fi
else
  check "标题非英文开头（跳过副标题检查）" "1"
fi

echo ""

# =============================================
echo "--- 正文结构 ---"
# =============================================

# 16. ## 概述 存在
check "## 概述" "$(echo "$BODY" | grep -q '^## 概述' && echo 1 || echo 0)"

# 17. 对我们的直接价值 存在（允许变体措辞）
check "直接价值" "$(echo "$BODY" | grep -q '直接价值' && echo 1 || echo 0)"

# 18. ## 局限与思考 存在
check "## 局限与思考" "$(echo "$BODY" | grep -q '^## 局限与思考' && echo 1 || echo 0)"

# 19. ## 相关文档 存在
check "## 相关文档" "$(echo "$BODY" | grep -q '^## 相关文档' && echo 1 || echo 0)"

# 20. ## 来源 存在，且内部有作者/原文链接/原材料 wikilink
SOURCE_SECTION=$(echo "$BODY" | awk '/^## 来源/{found=1; next} /^## /{if(found) exit} found{print}')
if [ -z "$SOURCE_SECTION" ]; then
  check "## 来源 存在" "0" "缺失"
else
  HAS_AUTHOR_IN_SRC=$(echo "$SOURCE_SECTION" | grep -ci '作者\|author\|@' 2>/dev/null || true)
  HAS_AUTHOR_IN_SRC=${HAS_AUTHOR_IN_SRC:-0}
  HAS_LINK_IN_SRC=$(echo "$SOURCE_SECTION" | grep -ci 'http\|原文' 2>/dev/null || true)
  HAS_LINK_IN_SRC=${HAS_LINK_IN_SRC:-0}
  HAS_RAW_IN_SRC=$(echo "$SOURCE_SECTION" | grep -ci '\[\[.*原材料\|原材料仓库' 2>/dev/null || true)
  HAS_RAW_IN_SRC=${HAS_RAW_IN_SRC:-0}
  if [ "${HAS_AUTHOR_IN_SRC:-0}" -gt 0 ] && [ "${HAS_LINK_IN_SRC:-0}" -gt 0 ] && [ "${HAS_RAW_IN_SRC:-0}" -gt 0 ]; then
    check "## 来源（含作者+链接+原材料）" "1"
  else
    MISSING=""
    [ "${HAS_AUTHOR_IN_SRC:-0}" -eq 0 ] && MISSING="${MISSING}作者 "
    [ "${HAS_LINK_IN_SRC:-0}" -eq 0 ] && MISSING="${MISSING}原文链接 "
    [ "${HAS_RAW_IN_SRC:-0}" -eq 0 ] && MISSING="${MISSING}原材料wikilink "
    check "## 来源 内容不完整" "0" "缺: $MISSING"
  fi
fi

echo ""

# =============================================
echo "--- 原材料 ---"
# =============================================

# 提取原材料路径（正则存变量，兼容 bash 3.2）
_re_original='\[\[(.*)\]\]'
if [[ "$ORIGINAL" =~ $_re_original ]]; then
  RAW_RELPATH="${BASH_REMATCH[1]}"
  # wikilink 可能不含 .md 扩展名
  [[ "$RAW_RELPATH" != *.md ]] && RAW_RELPATH="${RAW_RELPATH}.md"
  case "$RAW_RELPATH" in
    /*)
      RAW_FILE="$RAW_RELPATH" ;;
    "$raw_rel_prefix"/*)
      RAW_FILE="$VAULT/$RAW_RELPATH" ;;
    *)
      RAW_FILE="$RAW_DIR/$RAW_RELPATH" ;;
  esac

  # 21. 原材料文件存在
  if [ -f "$RAW_FILE" ]; then
    check "原材料文件存在" "1"

    RAW_FM=$(awk '/^---$/{n++; next} n==1{print} n>=2{exit}' "$RAW_FILE")

    # 22. 原材料 type = raw-material
    RAW_TYPE=$(echo "$RAW_FM" | grep -m1 "^type:" | sed 's/^type:[[:space:]]*//' | sed 's/^"//;s/"$//' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' || echo "")
    check "原材料 type: raw-material" "$([ "$RAW_TYPE" = "raw-material" ] && echo 1 || echo 0)" "当前: $RAW_TYPE"

    # 23. 原材料 status = archived
    RAW_STATUS=$(echo "$RAW_FM" | grep -m1 "^status:" | sed 's/^status:[[:space:]]*//' | sed 's/^"//;s/"$//' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' || echo "")
    check "原材料 status: archived" "$([ "$RAW_STATUS" = "archived" ] && echo 1 || echo 0)" "当前: $RAW_STATUS"

    # 24. 原材料 compiled_version 存在且带路径格式
    RAW_CV=$(echo "$RAW_FM" | grep -m1 "^compiled_version:" | sed 's/^compiled_version:[[:space:]]*//' | sed 's/^"//;s/"$//' | sed 's/\\//g' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' || echo "")
    if echo "$RAW_CV" | grep -q '^\[\[.*\]\]$'; then
      check "原材料 compiled_version 带路径" "1"
    elif [ -n "$RAW_CV" ]; then
      check "原材料 compiled_version 格式" "0" "应为带路径 wikilink，当前: $RAW_CV"
    else
      check "原材料 compiled_version" "0" "缺失"
    fi

    # 25. 原材料第一行是 ---
    RAW_FIRST=$(head -1 "$RAW_FILE")
    check "原材料第一行 ---" "$([ "$RAW_FIRST" = "---" ] && echo 1 || echo 0)" "当前: $RAW_FIRST"

  else
    check "原材料文件存在" "0" "不存在: $RAW_FILE"
    # 跳过 22-25
    TOTAL=$((TOTAL + 4))
    ERRORS=$((ERRORS + 4))
    echo "❌ 原材料 type（文件不存在，跳过）"
    echo "❌ 原材料 status（文件不存在，跳过）"
    echo "❌ 原材料 compiled_version（文件不存在，跳过）"
    echo "❌ 原材料第一行 ---（文件不存在，跳过）"
  fi
else
  check "original 格式可解析" "0" "无法提取原材料路径"
  TOTAL=$((TOTAL + 4))
  ERRORS=$((ERRORS + 4))
  echo "❌ 原材料检查全部跳过（original 格式异常）"
fi

echo ""

# =============================================
echo "--- 图片 ---"
# =============================================

# 26. 如果中转站正文含 ![[  图片引用 → 检查原材料 assets/ 目录存在
if echo "$BODY" | grep -q '!\[\['; then
  if [[ "$ORIGINAL" =~ $_re_original ]]; then
    RAW_NAME=$(basename "${BASH_REMATCH[1]}" .md)
    ASSETS_DIR="$RAW_DIR/assets/$RAW_NAME"
    if [ -d "$ASSETS_DIR" ]; then
      check "原材料 assets/ 目录存在" "1"
    else
      check "原材料 assets/ 目录存在" "0" "正文有图片引用但 $ASSETS_DIR 不存在"
    fi
  else
    check "图片检查" "0" "有图片引用但 original 格式异常"
  fi
else
  check "无图片引用（跳过）" "1"
fi

echo ""

# =============================================
echo "--- 反向验证 ---"
# =============================================

# 27. 原材料 compiled_version 指向的中转站文件实际存在
if [ -n "${RAW_CV:-}" ] && echo "$RAW_CV" | grep -q '\[\['; then
  CV_RELPATH=$(echo "$RAW_CV" | sed 's/.*\[\[//;s/\]\].*//')
  [[ "$CV_RELPATH" != *.md ]] && CV_RELPATH="${CV_RELPATH}.md"
  case "$CV_RELPATH" in
    /*)
      CV_FILE="$CV_RELPATH" ;;
    "$transit_rel_prefix"/*)
      CV_FILE="$VAULT/$CV_RELPATH" ;;
    *)
      CV_FILE="$TRANSIT_DIR/$CV_RELPATH" ;;
  esac
  if [ -f "$CV_FILE" ]; then
    check "compiled_version 指向文件存在" "1"
  else
    check "compiled_version 指向文件存在" "0" "不存在: $CV_FILE"
  fi
else
  # RAW_CV 为空或格式不对，#24 已报错，此处跳过不重复扣分
  check "compiled_version 反向验证（跳过，#24 已覆盖）" "1"
fi

echo ""

# =============================================
# 最终结果
# =============================================
if [ "$ERRORS" -eq 0 ]; then
  echo "=== 结果：PASS (0 errors / $TOTAL checks) ==="
else
  echo "=== 结果：FAIL ($ERRORS errors / $TOTAL checks) ==="
  echo ""
  echo "🔴 你必须修复以上所有 ❌ 项。不得以"误报"跳过。"
  echo "🔴 如果不知道怎么修，把本输出完整发给操作者，等指示。"
  echo "🔴 修复后重新运行本脚本，直到 PASS。"
fi

exit "$ERRORS"
