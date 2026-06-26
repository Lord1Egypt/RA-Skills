#!/bin/bash
set -u

# wiki_entry_xref_sync.sh — 双向「相关主题」补链
# 用途：确保 Wiki A 链到 B 时，B 也链到 A
# 输入：--wiki <当前Wiki相对路径>
# 输出：补链结果（已存在/已补充/目标不存在）
# 退出码：0=全部对称  1=有补链动作  2=参数错误

VAULT="${OPENCLAW_VAULT:-$(pwd)}"
WIKI_REL=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --wiki)
      WIKI_REL="$2"; shift 2 ;;
    --vault)
      VAULT="$2"; shift 2 ;;
    *)
      echo "❌ 未知参数: $1"
      exit 2 ;;
  esac
done

if [ -z "$WIKI_REL" ]; then
  echo "❌ 必须指定 --wiki <Wiki相对路径>"
  exit 2
fi

WIKI_ABS="$VAULT/$WIKI_REL"

if [ ! -f "$WIKI_ABS" ]; then
  echo "❌ Wiki 文件不存在: $WIKI_ABS"
  exit 2
fi

WIKI_DIR="${WIKI_ENTRY_DOMAIN_DIR:-$VAULT/Knowledge/领域}"
WIKI_BASENAME="$(basename "$WIKI_ABS" .md)"
HAD_FIX=0

# 提取「相关主题」章节中的 wikilink 目标
extract_related_links() {
  local file="$1"
  local in_section=0
  while IFS= read -r line; do
    # 进入「相关主题」章节
    if echo "$line" | grep -q '^## 相关主题'; then
      in_section=1
      continue
    fi
    # 遇到下一个 ## 章节就退出
    if [ "$in_section" -eq 1 ] && echo "$line" | grep -q '^## '; then
      break
    fi
    if [ "$in_section" -eq 1 ]; then
      # 提取 [[xxx]] 中的 xxx
      echo "$line" | grep -oE '\[\[[^]]+\]\]' | sed 's/\[\[//;s/\]\]//'
    fi
  done < "$file"
}

echo "=== 双向链接检查: $WIKI_BASENAME ==="
echo ""

# 获取当前 Wiki 的相关主题链接
LINKS=$(extract_related_links "$WIKI_ABS")

if [ -z "$LINKS" ]; then
  echo "ℹ️ $WIKI_BASENAME 无「相关主题」链接，跳过"
  exit 0
fi

while IFS= read -r target_name; do
  [ -z "$target_name" ] && continue

  # 查找目标文件
  TARGET_FILE="$WIKI_DIR/${target_name}.md"

  if [ ! -f "$TARGET_FILE" ]; then
    echo "⚠️ 目标不存在: [[${target_name}]]（文件 $TARGET_FILE 未找到）"
    continue
  fi

  # 检查目标文件是否反向链接回来
  if grep -q "\[\[$WIKI_BASENAME\]\]" "$TARGET_FILE"; then
    echo "✅ [[${target_name}]] ↔ [[$WIKI_BASENAME]] 已对称"
  else
    # 检查目标文件是否有「相关主题」章节
    if grep -q '^## 相关主题' "$TARGET_FILE"; then
      # 在「相关主题」章节末尾追加反向链接
      # 找到「相关主题」后的下一个 ## 或文件末尾，在其前插入
      awk -v link="- [[$WIKI_BASENAME]] — 交叉引用（自动补链）" '
        /^## 相关主题/ { in_sec=1; print; next }
        in_sec && /^## / { print link; print ""; in_sec=0 }
        { print }
        END { if (in_sec) print link }
      ' "$TARGET_FILE" > "${TARGET_FILE}.tmp" && mv "${TARGET_FILE}.tmp" "$TARGET_FILE"
    else
      # 没有「相关主题」章节，在文件末尾追加
      printf '\n## 相关主题\n- [[%s]] — 交叉引用（自动补链）\n' "$WIKI_BASENAME" >> "$TARGET_FILE"
    fi
    echo "🔧 已补链: [[${target_name}]] → 新增 [[$WIKI_BASENAME]]"
    HAD_FIX=1
  fi
done <<< "$LINKS"

echo ""
if [ "$HAD_FIX" -eq 1 ]; then
  echo "RESULT: FIXED（有补链动作）"
  exit 1
else
  echo "RESULT: PASS（全部对称）"
  exit 0
fi
