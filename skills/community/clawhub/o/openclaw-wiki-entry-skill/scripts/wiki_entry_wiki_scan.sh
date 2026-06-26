#!/bin/bash
set -u

VAULT="${OPENCLAW_VAULT:-$(pwd)}"
WIKI_REL=""
KEYWORDS=""
MIN_MATCH=1

while [ "$#" -gt 0 ]; do
  case "$1" in
    --wiki)
      WIKI_REL="$2"; shift 2 ;;
    --keywords)
      KEYWORDS="$2"; shift 2 ;;
    --min-match)
      MIN_MATCH="$2"; shift 2 ;;
    --vault)
      VAULT="$2"; shift 2 ;;
    *)
      echo "未知参数: $1"
      exit 1 ;;
  esac
done

if [ -z "$WIKI_REL" ] || [ -z "$KEYWORDS" ]; then
  echo "用法: wiki_entry_wiki_scan.sh --wiki <Knowledge/领域/xxx.md> --keywords \"词1,词2\" [--min-match 1]"
  exit 1
fi

WIKI="$WIKI_REL"
case "$WIKI" in
  /*) ;;
  *) WIKI="$VAULT/$WIKI" ;;
esac

if [ ! -f "$WIKI" ]; then
  echo "❌ Wiki 不存在: $WIKI"
  exit 1
fi

echo "=== wiki_scan ==="
echo "Wiki: $WIKI"
echo "Keywords: $KEYWORDS"

hits=0
IFS=',' read -r -a kws <<< "$KEYWORDS"
for kw in "${kws[@]}"; do
  k="$(printf '%s' "$kw" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  [ -z "$k" ] && continue
  echo ""
  echo "[关键词] $k"
  m=$(grep -n -i -- "$k" "$WIKI" || true)
  if [ -n "$m" ]; then
    echo "$m"
    hits=$((hits + 1))
  else
    echo "(无命中)"
  fi
done

echo ""
echo "命中关键词数: $hits"
if [ "$hits" -lt "$MIN_MATCH" ]; then
  echo "❌ 命中不足（< $MIN_MATCH），建议 BLOCK 并回到 Step 3 重决策"
  exit 1
fi

echo "✅ 命中通过"
exit 0
