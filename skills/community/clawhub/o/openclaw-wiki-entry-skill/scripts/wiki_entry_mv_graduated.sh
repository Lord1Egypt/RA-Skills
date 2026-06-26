#!/bin/bash
set -u

# wiki_entry_mv_graduated.sh — 移动 graduated 文档到已入库目录
# 用途：Step 11 将 status: graduated 的中转站文档移至 Knowledge/已入库/
# 输入：--source-doc <中转站文档相对路径>
# 验证：移动前确认 status==graduated + graduated_to 非空；移动后 Glob 验证
# 退出码：0=成功  1=验证失败  2=参数错误

VAULT="${OPENCLAW_VAULT:-$(pwd)}"
SOURCE_DOC_REL=""
DRY_RUN=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --source-doc)
      SOURCE_DOC_REL="$2"; shift 2 ;;
    --dry-run)
      DRY_RUN=1; shift 1 ;;
    --vault)
      VAULT="$2"; shift 2 ;;
    *)
      echo "❌ 未知参数: $1"
      exit 2 ;;
  esac
done

if [ -z "$SOURCE_DOC_REL" ]; then
  echo "❌ 必须指定 --source-doc <中转站文档相对路径>"
  exit 2
fi

SOURCE_ABS="$VAULT/$SOURCE_DOC_REL"
DEST_DIR="${WIKI_ENTRY_GRADUATED_DIR:-$VAULT/Knowledge/已入库}"
BASENAME="$(basename "$SOURCE_ABS")"
DEST_ABS="$DEST_DIR/$BASENAME"

# --- 前置验证 ---

if [ ! -f "$SOURCE_ABS" ]; then
  echo "❌ 源文件不存在: $SOURCE_ABS"
  exit 1
fi

if [ ! -d "$DEST_DIR" ]; then
  echo "❌ 目标目录不存在: $DEST_DIR"
  exit 1
fi

# 检查 status == graduated
STATUS=$(awk '/^---$/{c++; next} c==1 && /^status:/{print $2; exit}' "$SOURCE_ABS")
if [ "$STATUS" != "graduated" ]; then
  echo "❌ 文档状态不是 graduated（当前: ${STATUS:-空}），不能移动"
  echo "   只有 status: graduated 的文档才能移至已入库"
  exit 1
fi

# 检查 graduated_to 非空
GRAD_TO=$(awk '/^---$/{c++; next} c==1 && /^graduated_to:/{found=1; next} found && /^  - /{print; next} found{exit}' "$SOURCE_ABS")
if [ -z "$GRAD_TO" ]; then
  echo "❌ graduated_to 字段为空，不能移动"
  echo "   必须有 graduated_to 指向目标 Wiki"
  exit 1
fi

# 检查目标是否已存在同名文件
if [ -f "$DEST_ABS" ]; then
  echo "⚠️ 目标已存在同名文件: $DEST_ABS"
  echo "   跳过移动，请手动处理"
  exit 1
fi

# --- 执行移动 ---

if [ "$DRY_RUN" -eq 1 ]; then
  echo "🔍 [DRY RUN] 将移动:"
  echo "   从: $SOURCE_ABS"
  echo "   到: $DEST_ABS"
  echo "   状态: $STATUS"
  echo "   graduated_to: $GRAD_TO"
  exit 0
fi

mv "$SOURCE_ABS" "$DEST_ABS"

# --- 移动后验证 ---

if [ ! -f "$DEST_ABS" ]; then
  echo "❌ 移动后目标文件不存在，移动可能失败"
  exit 1
fi

if [ -f "$SOURCE_ABS" ]; then
  echo "❌ 移动后源文件仍存在，移动可能失败"
  exit 1
fi

# 验证 graduated_to 中的 wikilink 目标文件存在
while IFS= read -r line; do
  # 提取 [[xxx]] 中的 xxx
  wiki_name=$(echo "$line" | grep -oE '\[\[[^]]+\]\]' | sed 's/\[\[//;s/\]\]//')
  [ -z "$wiki_name" ] && continue
  # 在 Knowledge/领域/ 下查找
  if [ ! -f "$VAULT/Knowledge/领域/${wiki_name}.md" ]; then
    echo "⚠️ graduated_to 目标 Wiki 不存在: [[${wiki_name}]]"
  fi
done <<< "$GRAD_TO"

echo "✅ 已移动: $SOURCE_DOC_REL → Knowledge/已入库/$BASENAME"
exit 0
