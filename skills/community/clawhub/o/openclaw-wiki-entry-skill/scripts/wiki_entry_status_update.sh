#!/bin/bash
set -eu

VAULT="${OPENCLAW_VAULT:-${VAULT_ROOT:-$(pwd)}}"
DOC_REL=""
FROM_STATUS=""
TO_STATUS=""

usage() {
  echo "用法: wiki_entry_status_update.sh --doc <doc> --from <status> --to <status> [--vault <vault>]" >&2
}

error() {
  echo "❌ $*" >&2
}

abs_path() {
  local p="$1"
  case "$p" in
    /*) printf '%s' "$p" ;;
    *) printf '%s/%s' "$VAULT" "$p" ;;
  esac
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --doc)
      DOC_REL="$2"; shift 2 ;;
    --from)
      FROM_STATUS="$2"; shift 2 ;;
    --to)
      TO_STATUS="$2"; shift 2 ;;
    --vault)
      VAULT="$2"; shift 2 ;;
    *)
      error "未知参数: $1"
      usage
      exit 1 ;;
  esac
done

if [ -z "$DOC_REL" ] || [ -z "$FROM_STATUS" ] || [ -z "$TO_STATUS" ]; then
  usage
  exit 1
fi

DOC="$(abs_path "$DOC_REL")"

if [ ! -f "$DOC" ]; then
  error "文档不存在: $DOC"
  exit 1
fi

if [ "$(awk 'NR==1 { print; exit }' "$DOC")" != "---" ]; then
  error "无 frontmatter"
  exit 1
fi

if ! awk 'NR>1 && $0=="---" { found=1; exit } END { exit(found ? 0 : 1) }' "$DOC"; then
  error "无 frontmatter"
  exit 1
fi

STATUS_LINE="$(awk '
  NR==1 { in_frontmatter=($0=="---"); next }
  in_frontmatter && $0=="---" { exit }
  in_frontmatter && /^[[:space:]]*status[[:space:]]*:/ { print; exit }
' "$DOC")"

if [ -z "$STATUS_LINE" ]; then
  error "status 字段不存在"
  exit 1
fi

case "$STATUS_LINE" in
  "status: "*) ;;
  *)
    error "status 字段格式不支持: $STATUS_LINE"
    exit 1 ;;
esac

CURRENT_STATUS="${STATUS_LINE#status: }"

case "$CURRENT_STATUS" in
  ""|*" "*|*$'\t'*|*$'\n'*|*#*|*\"*|*"'"*)
    error "status 字段格式不支持: $STATUS_LINE"
    exit 1 ;;
esac

if [ "$CURRENT_STATUS" != "$FROM_STATUS" ]; then
  error "status 当前值为 ${CURRENT_STATUS}，不是 ${FROM_STATUS}"
  exit 1
fi

TMP_DOC="$DOC.tmp.$$"

awk -v to_status="$TO_STATUS" '
  NR==1 && $0=="---" { in_frontmatter=1; print; next }
  in_frontmatter && $0=="---" { in_frontmatter=0; print; next }
  in_frontmatter && !done && /^status: / {
    print "status: " to_status
    done=1
    next
  }
  { print }
  END {
    if (!done) {
      exit 9
    }
  }
' "$DOC" > "$TMP_DOC"

mv "$TMP_DOC" "$DOC"

UPDATED_STATUS="$(awk '
  NR==1 { in_frontmatter=($0=="---"); next }
  in_frontmatter && $0=="---" { exit }
  in_frontmatter && /^status: / { sub(/^status: /, ""); print; exit }
' "$DOC")"

if [ "$UPDATED_STATUS" != "$TO_STATUS" ]; then
  error "回读失败：status 未更新为 $TO_STATUS"
  exit 1
fi

echo "✅ status 已更新"
echo "  Doc: $DOC"
echo "  $FROM_STATUS -> $TO_STATUS"
exit 0
