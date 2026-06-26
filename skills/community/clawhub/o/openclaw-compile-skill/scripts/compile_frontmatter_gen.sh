#!/bin/bash
set -u

TITLE=""
AUTHOR=""
SOURCE=""
COMPILED_BY=""
RELATED_WIKI=""
TAGS=""
KEYWORDS=""
CREATED="$(date +%Y-%m-%d)"
VAULT="${OPENCLAW_VAULT:-$(pwd)}"
RAW_DIR="${COMPILE_RAW_DIR:-$VAULT/Knowledge/原材料仓库}"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --title)
      TITLE="$2"; shift 2 ;;
    --author)
      AUTHOR="$2"; shift 2 ;;
    --source)
      SOURCE="$2"; shift 2 ;;
    --compiled-by)
      COMPILED_BY="$2"; shift 2 ;;
    --related-wiki)
      RELATED_WIKI="$2"; shift 2 ;;
    --tags)
      TAGS="$2"; shift 2 ;;
    --keywords)
      KEYWORDS="$2"; shift 2 ;;
    --created)
      CREATED="$2"; shift 2 ;;
    --vault)
      VAULT="$2"
      RAW_DIR="${COMPILE_RAW_DIR:-$VAULT/Knowledge/原材料仓库}"
      shift 2 ;;
    *)
      echo "未知参数: $1"
      exit 1 ;;
  esac
done

if [ -z "$TITLE" ] || [ -z "$AUTHOR" ] || [ -z "$SOURCE" ] || [ -z "$COMPILED_BY" ] || [ -z "$KEYWORDS" ]; then
  echo "必填参数缺失：--title --author --source --compiled-by --keywords"
  exit 1
fi

normalize_author() {
  case "$1" in
    @*) printf '%s' "$1" ;;
    *) printf '@%s' "$1" ;;
  esac
}

normalize_csv_list() {
  local raw="$1"
  python3 - <<'PY' "$raw"
import json
import sys
items = [item.strip() for item in sys.argv[1].split(',') if item.strip()]
print(json.dumps(items, ensure_ascii=False))
PY
}

AUTHOR="$(normalize_author "$AUTHOR")"
TAGS_LINE="$(normalize_csv_list "$TAGS")"
KEYWORDS_LINE="$(normalize_csv_list "$KEYWORDS")"
RELATED_WIKI_LINE="$(normalize_csv_list "$RELATED_WIKI")"
RAW_REL="$RAW_DIR/$TITLE"
case "$RAW_REL" in
  "$VAULT"/*)
    RAW_REL="${RAW_REL#$VAULT/}" ;;
esac

cat <<EOF
---
type: compiled
status: waiting
source: "$SOURCE"
author: "$AUTHOR"
original: "[[$RAW_REL]]"
created: $CREATED
compiled_by: "$COMPILED_BY"
tags: $TAGS_LINE
keywords: $KEYWORDS_LINE
related_wiki: $RELATED_WIKI_LINE
---
EOF
