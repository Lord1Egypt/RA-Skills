#!/bin/bash
set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT="${OPENCLAW_VAULT:-$(pwd)}"
WIKI_REL=""
SOURCE_DOC_REL=""
SOURCE_ROW=""
EVOLUTION_ROW=""
PATH_TYPE=""
INDEX_REL="${WIKI_ENTRY_INDEX_FILE:-Knowledge/_INDEX.md}"
INDEX_CATEGORY=""
CHECK_CONTRADICTIONS=0
CONTRADICTION_DECISION=""
INDEX_UPDATE_SCRIPT="$SCRIPT_DIR/_shared/index_update.sh"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --wiki)
      WIKI_REL="$2"; shift 2 ;;
    --source-doc)
      SOURCE_DOC_REL="$2"; shift 2 ;;
    --source-row)
      SOURCE_ROW="$2"; shift 2 ;;
    --evolution-row)
      EVOLUTION_ROW="$2"; shift 2 ;;
    --path)
      PATH_TYPE="$2"; shift 2 ;;
    --index-file)
      INDEX_REL="$2"; shift 2 ;;
    --index-category)
      INDEX_CATEGORY="$2"; shift 2 ;;
    --check-contradictions)
      CHECK_CONTRADICTIONS=1; shift 1 ;;
    --contradiction-decision)
      CONTRADICTION_DECISION="$2"; shift 2 ;;
    --vault)
      VAULT="$2"; shift 2 ;;
    *)
      echo "未知参数: $1"
      exit 1 ;;
  esac
done

if [ -z "$WIKI_REL" ] || [ -z "$SOURCE_DOC_REL" ] || [ -z "$SOURCE_ROW" ] || [ -z "$EVOLUTION_ROW" ] || [ -z "$PATH_TYPE" ]; then
  echo "用法: wiki_entry_meta_writeback.sh --wiki <wiki> --source-doc <doc> --source-row <row> --evolution-row <row> --path <A|B> [--index-file <index>] [--index-category <分类>] [--check-contradictions --contradiction-decision <text>]"
  exit 1
fi

case "$PATH_TYPE" in
  A|B) ;;
  *) echo "--path 只能是 A 或 B"; exit 1 ;;
esac

if [ "$PATH_TYPE" = "A" ] && [ -z "$INDEX_CATEGORY" ]; then
  echo "❌ A 路径必须提供 --index-category"
  exit 1
fi

abs_path() {
  local p="$1"
  case "$p" in
    /*) printf '%s' "$p" ;;
    *) printf '%s/%s' "$VAULT" "$p" ;;
  esac
}

replace_line() {
  local file="$1"
  local pattern="$2"
  local replacement="$3"
  awk -v pattern="$pattern" -v replacement="$replacement" '
    $0 ~ pattern { print replacement; next }
    { print }
  ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
}

WIKI="$(abs_path "$WIKI_REL")"
SOURCE_DOC="$(abs_path "$SOURCE_DOC_REL")"
INDEX_FILE="$(abs_path "$INDEX_REL")"

if [ ! -f "$WIKI" ]; then
  echo "❌ Wiki 不存在: $WIKI"
  exit 1
fi
if [ ! -f "$SOURCE_DOC" ]; then
  echo "❌ source doc 不存在: $SOURCE_DOC"
  exit 1
fi
if [ ! -f "$INDEX_FILE" ]; then
  echo "❌ index 不存在: $INDEX_FILE"
  exit 1
fi
if [ ! -f "$INDEX_UPDATE_SCRIPT" ]; then
  echo "❌ index_update.sh 不存在: $INDEX_UPDATE_SCRIPT"
  exit 1
fi

if [ "$CHECK_CONTRADICTIONS" -eq 1 ]; then
  if grep -q '⚡矛盾' "$WIKI" 2>/dev/null; then
    if [ -z "$CONTRADICTION_DECISION" ]; then
      echo "❌ 检测到 ⚡矛盾，但未提供 --contradiction-decision"
      exit 2
    fi
    echo "⚠️  矛盾检测：已提供裁决说明"
  fi
fi

TODAY="$(date +%Y-%m-%d)"
WIKI_BASE="$(basename "$WIKI" .md)"
SOURCE_BASE="$(basename "$SOURCE_DOC" .md)"

# 1) 来源表插入（幂等）
if grep -Fq "$SOURCE_ROW" "$WIKI"; then
  echo "↺ 来源行已存在，跳过插入"
else
  awk -v row="$SOURCE_ROW" '
    BEGIN{in_tbl=0;inserted=0}
    {print}
    /^### 外部来源/ {in_tbl=1; next}
    in_tbl && /^\|[: -]+\|/ && inserted==0 {print row; inserted=1; next}
    in_tbl && /^### / && inserted==0 {print row; inserted=1; in_tbl=0}
    END{if(inserted==0) print row}
  ' "$WIKI" > "$WIKI.tmp" && mv "$WIKI.tmp" "$WIKI"
  echo "✅ 已写入来源行"
fi

# 2) 演进记录插入（幂等）
if grep -Fq "$EVOLUTION_ROW" "$WIKI"; then
  echo "↺ 演进行已存在，跳过插入"
else
  awk -v row="$EVOLUTION_ROW" '
    BEGIN{in_tbl=0;inserted=0}
    {print}
    /^### 演进记录/ {in_tbl=1; next}
    in_tbl && /^\|[: -]+\|/ && inserted==0 {print row; inserted=1; next}
    in_tbl && /^## / && inserted==0 {print row; inserted=1; in_tbl=0}
    END{if(inserted==0) print row}
  ' "$WIKI" > "$WIKI.tmp" && mv "$WIKI.tmp" "$WIKI"
  echo "✅ 已写入演进行"
fi

# 3) 计算来源表行数并回写 sources_count
count=$(awk '
  /^### 外部来源/ {in_ext=1; next}
  in_ext && /^### / {in_ext=0}
  in_ext && /^\|/ {
    if ($0 ~ /^\|[: -]+\|/) next
    if ($0 ~ /^\| 来源 \| 作者 \| 核心贡献 \| 状态 \|/) next
    c++
  }
  END{print c+0}
' "$WIKI")

if grep -q '^sources_count:' "$WIKI"; then
  replace_line "$WIKI" '^sources_count:' "sources_count: $count"
else
  awk -v c="$count" '
    BEGIN{done=0}
    /^---$/ && done==0 {print; next}
    /^---$/ && done==0 && NR>1 {print "sources_count: " c; done=1; print; next}
    {print}
  ' "$WIKI" > "$WIKI.tmp" && mv "$WIKI.tmp" "$WIKI"
fi

# 4) 回写 last_updated
if grep -q '^last_updated:' "$WIKI"; then
  replace_line "$WIKI" '^last_updated:' "last_updated: $TODAY"
else
  if grep -q '^updated:' "$WIKI"; then
    replace_line "$WIKI" '^updated:' "updated: $TODAY"
  fi
fi

# 5) 回写 source doc 的 graduated_to/status
if grep -q '^status:' "$SOURCE_DOC"; then
  replace_line "$SOURCE_DOC" '^status:' 'status: graduated'
else
  awk 'NR==1{print; print "status: graduated"; next} {print}' "$SOURCE_DOC" > "$SOURCE_DOC.tmp" && mv "$SOURCE_DOC.tmp" "$SOURCE_DOC"
fi

if grep -q '^graduated_to:' "$SOURCE_DOC"; then
  awk -v wiki="[[Knowledge/领域/'"$WIKI_BASE"']]" '
    BEGIN{in_grad=0;done=0}
    /^graduated_to:/ {print; in_grad=1; next}
    in_grad && /^  - / {
      if (index($0, wiki)>0) done=1
      print; next
    }
    in_grad && /^[^ ]/ {
      if (done==0) print "  - \"" wiki "\""
      in_grad=0
      print
      next
    }
    {print}
    END{ if(in_grad==1 && done==0) print "  - \"" wiki "\"" }
  ' "$SOURCE_DOC" > "$SOURCE_DOC.tmp" && mv "$SOURCE_DOC.tmp" "$SOURCE_DOC"
else
  awk -v wiki="[[Knowledge/领域/$WIKI_BASE]]" '
    BEGIN{inserted=0}
    {
      if (!inserted && /^status:/) {
        print
        print "graduated_to:"
        print "  - \"" wiki "\""
        inserted=1
        next
      }
      print
    }
    END{
      if (!inserted) {
        print "graduated_to:"
        print "  - \"" wiki "\""
      }
    }
  ' "$SOURCE_DOC" > "$SOURCE_DOC.tmp" && mv "$SOURCE_DOC.tmp" "$SOURCE_DOC"
fi

# 6) 更新 _INDEX
if [ "$PATH_TYPE" = "A" ]; then
  bash "$INDEX_UPDATE_SCRIPT" add \
    --vault "$VAULT" \
    --index-file "$INDEX_REL" \
    --wiki "$WIKI_BASE" \
    --category "$INDEX_CATEGORY" \
    --sources "$count" \
    --date "$TODAY"
else
  bash "$INDEX_UPDATE_SCRIPT" update \
    --vault "$VAULT" \
    --index-file "$INDEX_REL" \
    --wiki "$WIKI_BASE" \
    --sources "$count" \
    --date "$TODAY"
fi

# 7) 回读验证
ok=1

if ! grep -Fq "$SOURCE_ROW" "$WIKI"; then
  echo "❌ 回读失败：来源行不存在"
  ok=0
fi
if ! grep -Fq "$EVOLUTION_ROW" "$WIKI"; then
  echo "❌ 回读失败：演进行不存在"
  ok=0
fi
if ! grep -q "^sources_count:[[:space:]]*$count" "$WIKI"; then
  echo "❌ 回读失败：sources_count 未同步"
  ok=0
fi
if ! grep -q "^last_updated:[[:space:]]*$TODAY" "$WIKI" && ! grep -q "^updated:[[:space:]]*$TODAY" "$WIKI"; then
  echo "❌ 回读失败：last_updated/updated 未同步"
  ok=0
fi
if ! grep -q '^status:[[:space:]]*graduated' "$SOURCE_DOC"; then
  echo "❌ 回读失败：source doc status 未改为 graduated"
  ok=0
fi
if ! grep -q '^graduated_to:' "$SOURCE_DOC"; then
  echo "❌ 回读失败：source doc 缺 graduated_to"
  ok=0
fi

if [ "$ok" -ne 1 ]; then
  exit 1
fi

echo "✅ meta_writeback 完成"
echo "  Wiki: $WIKI"
echo "  Source doc: $SOURCE_DOC"
echo "  sources_count: $count"
exit 0
