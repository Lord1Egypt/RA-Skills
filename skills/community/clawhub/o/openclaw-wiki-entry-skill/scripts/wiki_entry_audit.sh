#!/bin/bash
set -u

VAULT="${OPENCLAW_VAULT:-$(pwd)}"
INDEX_FILE_DEFAULT="${WIKI_ENTRY_INDEX_FILE:-$VAULT/Knowledge/_INDEX.md}"
TRANSIT_DIR="${WIKI_ENTRY_TRANSIT_DIR:-$VAULT/Knowledge/中转站}"
DOMAIN_DIR="${WIKI_ENTRY_DOMAIN_DIR:-$VAULT/Knowledge/领域}"
GRADUATED_DIR="${WIKI_ENTRY_GRADUATED_DIR:-$VAULT/Knowledge/已入库}"
RAW_DIR="${WIKI_ENTRY_RAW_DIR:-$VAULT/Knowledge/原材料仓库}"
WIKI_ARG=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --wiki)
      WIKI_ARG="$2"; shift 2 ;;
    --vault)
      VAULT="$2"
      INDEX_FILE_DEFAULT="${WIKI_ENTRY_INDEX_FILE:-$VAULT/Knowledge/_INDEX.md}"
      TRANSIT_DIR="${WIKI_ENTRY_TRANSIT_DIR:-$VAULT/Knowledge/中转站}"
      DOMAIN_DIR="${WIKI_ENTRY_DOMAIN_DIR:-$VAULT/Knowledge/领域}"
      GRADUATED_DIR="${WIKI_ENTRY_GRADUATED_DIR:-$VAULT/Knowledge/已入库}"
      RAW_DIR="${WIKI_ENTRY_RAW_DIR:-$VAULT/Knowledge/原材料仓库}"
      shift 2 ;;
    *)
      echo "未知参数: $1"
      exit 2 ;;
  esac
done

resolve_wiki() {
  local p="$1"
  if [ -z "$p" ]; then
    echo ""
    return
  fi
  case "$p" in
    /*) echo "$p" ;;
    *) echo "$VAULT/$p" ;;
  esac
}

trim() { printf '%s' "$1" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'; }

audit_one() {
  local wiki="$1"
  local wiki_base index_file table_count fm_count idx_count today fail
  wiki_base="$(basename "$wiki" .md)"
  index_file="$INDEX_FILE_DEFAULT"
  today="$(date +%Y-%m-%d)"
  fail=0

  echo "=== 审计 $(basename "$wiki") ==="

  if [ ! -f "$wiki" ]; then
    echo "❌ Wiki 不存在: $wiki"
    return 1
  fi

  table_count=$(awk '
    /^### 外部来源/ {in_ext=1; next}
    in_ext && /^### / {in_ext=0}
    in_ext && /^\|/ {
      if ($0 ~ /^\|[: -]+\|/) next
      if ($0 ~ /^\| 来源 \| 作者 \| 核心贡献 \| 状态 \|/) next
      c++
    }
    END{print c+0}
  ' "$wiki")

  fm_count=$(awk '/^---$/{n++; next} n==1{print} n>=2{exit}' "$wiki" | grep -m1 '^sources_count:' | sed -E 's/^sources_count:[[:space:]]*//' | tr -d ' ')
  fm_count="$(trim "${fm_count:-0}")"
  [ -z "$fm_count" ] && fm_count=0

  idx_count=0
  if [ -f "$index_file" ]; then
    line=$(grep -F "[[${wiki_base}]]" "$index_file" | head -n1 || true)
    if [ -n "$line" ]; then
      idx_field=$(echo "$line" | awk -F'|' '{print $4}')
      idx_count=$(echo "$idx_field" | grep -oE '[0-9]+' | head -n1)
      idx_count="${idx_count:-0}"
    fi
  fi

  if [ "$table_count" = "$fm_count" ]; then
    echo "✓ 来源表行数 = sources_count ($table_count)"
  else
    echo "✗ 来源表行数($table_count) != sources_count($fm_count)"
    fail=1
  fi

  if [ "$fm_count" = "$idx_count" ]; then
    echo "✓ sources_count = _INDEX 来源数 ($fm_count)"
  else
    echo "✗ sources_count($fm_count) != _INDEX($idx_count)"
    fail=1
  fi

  if grep -q "^last_updated:[[:space:]]*$today" "$wiki" || grep -q "^updated:[[:space:]]*$today" "$wiki"; then
    echo "✓ last_updated/updated 为今日"
  else
    echo "✗ last_updated/updated 非今日 ($today)"
    fail=1
  fi

  # 检查来源表 wikilink 目标存在
  missing=0
  while IFS= read -r target; do
    t="$(echo "$target" | sed 's/\[\[//;s/\]\]//')"
    [ -z "$t" ] && continue
    if [[ "$t" == Knowledge/* ]]; then
      p="$VAULT/$t"
      [[ "$p" != *.md ]] && p="$p.md"
    else
      p1="$TRANSIT_DIR/$t.md"
      p2="$GRADUATED_DIR/$t.md"
      p3="$RAW_DIR/$t.md"
      p4="$DOMAIN_DIR/$t.md"
      p5="$VAULT/Knowledge/$t"
      if [ -f "$p1" ]; then p="$p1";
      elif [ -f "$p2" ]; then p="$p2";
      elif [ -f "$p3" ]; then p="$p3";
      elif [ -f "$p4" ]; then p="$p4";
      elif [ -d "$p5" ]; then p="$p5";
      else p=""; fi
    fi
    if [ -z "${p:-}" ] || { [ ! -f "$p" ] && [ ! -d "$p" ]; }; then
      echo "✗ wikilink 目标不存在: [[${t}]]"
      missing=1
    fi
  done < <(awk '
    /^### 外部来源/ {in_ext=1; next}
    in_ext && /^### / {in_ext=0}
    in_ext && /^\|/ {
      if ($0 ~ /^\|[: -]+\|/) next
      if ($0 ~ /^\| 来源 \| 作者 \| 核心贡献 \| 状态 \|/) next
      print
    }
  ' "$wiki" | grep -o '\[\[[^]]*\]\]' || true)

  if [ "$missing" -eq 0 ]; then
    echo "✓ 来源表 wikilink 目标存在"
  else
    fail=1
  fi

  # 演进记录格式
  bad_evo=0
  awk '
    /^### 演进记录/ {in_evo=1; next}
    in_evo && /^## / {in_evo=0}
    in_evo && /^\|/ {
      if ($0 ~ /^\|[: -]+\|/) next
      if ($0 ~ /^\| 日期 \| 事件 \|/) next
      if ($0 !~ /^\|[[:space:]]*[0-9]{4}-[0-9]{2}-[0-9]{2}[[:space:]]*\|/) { bad=1 }
    }
    END{ if (bad==1) exit 1 }
  ' "$wiki" || bad_evo=1

  if [ "$bad_evo" -eq 0 ]; then
    echo "✓ 演进记录格式"
  else
    echo "✗ 演进记录格式异常"
    fail=1
  fi

  if [ "$fail" -eq 0 ]; then
    echo "RESULT: PASS"
    return 0
  else
    echo "RESULT: FAIL"
    return 1
  fi
}

if [ -n "$WIKI_ARG" ]; then
  WIKI="$(resolve_wiki "$WIKI_ARG")"
  audit_one "$WIKI"
  exit $?
fi

any_fail=0
for w in "$DOMAIN_DIR"/*.md; do
  [ -f "$w" ] || continue
  audit_one "$w" || any_fail=1
  echo ""
done

if [ "$any_fail" -eq 0 ]; then
  exit 0
else
  exit 1
fi
