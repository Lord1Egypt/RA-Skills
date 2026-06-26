#!/bin/bash
set -u

VAULT="${OPENCLAW_VAULT:-$(pwd)}"
SKILL=""
TOPIC=""
WINDOW_DAYS=30
INCLUDE_CONTRADICTIONS=0
RECENT_COLLECTIONS="${QH_RECENT_COLLECTIONS:-knowledge openclaw}"
EVOLUTION_COLLECTIONS="${QH_EVOLUTION_COLLECTIONS:-openclaw}"

usage() {
  echo "用法: query_history.sh --skill <wiki-entry|compile> --topic \"<关键词>\" [--window <N>] [--include-contradictions] [--vault <path>]"
}

is_positive_int() {
  case "$1" in
    ''|*[!0-9]*) return 1 ;;
    0) return 1 ;;
    *) return 0 ;;
  esac
}

normalize_qmd_entry() {
  local explicit="${QH_QMD_ENTRY:-${COMPILE_QMD_ENTRY:-}}"
  if [ -n "$explicit" ]; then
    echo "$explicit"
  else
    echo ""
  fi
}

ensure_qmd_ready() {
  local qmd_entry="$1"
  local help

  if [ -z "$qmd_entry" ]; then
    echo "⚠️ QMD 未配置，跳过历史检索"
    echo "RESULT: QMD_SKIPPED"
    return 10
  fi

  if [ ! -x "$qmd_entry" ]; then
    echo "⚠️ QMD 不可用，跳过历史检索: $qmd_entry"
    echo "RESULT: QMD_SKIPPED"
    return 10
  fi

  help="$($qmd_entry --help 2>/dev/null)"
  if [ $? -ne 0 ] || [ -z "$help" ]; then
    echo "⚠️ QMD 不可用，跳过历史检索：无法读取帮助信息"
    echo "RESULT: QMD_SKIPPED"
    return 10
  fi

  printf '%s\n' "$help" | grep -q "search" || {
    echo "⚠️ QMD 不可用，跳过历史检索：缺少 search 命令"
    echo "RESULT: QMD_SKIPPED"
    return 10
  }
  printf '%s\n' "$help" | grep -q "get" || {
    echo "⚠️ QMD 不可用，跳过历史检索：缺少 get 命令"
    echo "RESULT: QMD_SKIPPED"
    return 10
  }
  printf '%s\n' "$help" | grep -q -- "--files" || {
    echo "⚠️ QMD 不可用，跳过历史检索：缺少 --files 输出选项"
    echo "RESULT: QMD_SKIPPED"
    return 10
  }
  printf '%s\n' "$help" | grep -q -- "-c, --collection" || {
    echo "⚠️ QMD 不可用，跳过历史检索：缺少 --collection 选项"
    echo "RESULT: QMD_SKIPPED"
    return 10
  }

  return 0
}

cutoff_date() {
  python3 - "$1" <<'PY'
from datetime import date, timedelta
import sys
n = int(sys.argv[1])
print((date.today() - timedelta(days=n)).isoformat())
PY
}

extract_date_from_uri() {
  local uri="$1"
  if [[ "$uri" =~ ([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
    echo "${BASH_REMATCH[1]}"
    return 0
  fi
  echo ""
}

extract_date_from_doc() {
  local doc="$1"
  local raw
  raw="$(printf '%s\n' "$doc" | grep -m1 -E '^(date|created|last_updated):' | sed -E 's/^[^:]+:[[:space:]]*//')"
  raw="$(printf '%s' "$raw" | sed -E 's/^"//;s/"$//')"
  raw="${raw:0:10}"
  if [[ "$raw" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    echo "$raw"
  else
    echo ""
  fi
}

extract_summary_from_doc() {
  local doc="$1"
  local summary

  summary="$(printf '%s\n' "$doc" | grep -m1 -E '^# ' | sed -E 's/^# +//')"
  if [ -n "$summary" ]; then
    echo "$summary"
    return 0
  fi

  summary="$(printf '%s\n' "$doc" | grep -vE '^(Folder Context:|---$|[[:space:]]*$|date:|day:|month:|type:|tags:|keywords:|created:|last_updated:|status:|topic:|maintained_by:|[[:space:]]*-[[:space:]])' | head -n1)"
  if [ -n "$summary" ]; then
    echo "$summary"
  else
    echo "(无摘要)"
  fi
}

trim_quotes() {
  local s="$1"
  s="${s#\"}"
  s="${s%\"}"
  echo "$s"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --skill)
      SKILL="$2"; shift 2 ;;
    --topic)
      TOPIC="$2"; shift 2 ;;
    --window)
      WINDOW_DAYS="$2"; shift 2 ;;
    --include-contradictions)
      INCLUDE_CONTRADICTIONS=1; shift 1 ;;
    --vault)
      VAULT="$2"; shift 2 ;;
    *)
      echo "未知参数: $1"
      usage
      exit 1 ;;
  esac
done

if [ -z "$SKILL" ] || [ -z "$TOPIC" ]; then
  usage
  exit 1
fi

case "$SKILL" in
  wiki-entry|compile) ;;
  *)
    echo "--skill 只能是 wiki-entry 或 compile"
    usage
    exit 1 ;;
esac

if ! is_positive_int "$WINDOW_DAYS"; then
  echo "--window 必须是正整数"
  usage
  exit 1
fi

QMD_ENTRY="$(normalize_qmd_entry)"
CONTRADICTION_FILE="${QH_CONTRADICTION_FILE:-$VAULT/Knowledge/领域/矛盾追踪.md}"
CUTOFF="$(cutoff_date "$WINDOW_DAYS")"

ensure_qmd_ready "$QMD_ENTRY"
qmd_rc=$?
if [ "$qmd_rc" -eq 10 ]; then
  exit 0
fi
if [ "$qmd_rc" -ne 0 ]; then
  exit "$qmd_rc"
fi

TMP_BASE="$TMPDIR/query-history-$$"
RECENT_FILE="$TMP_BASE.recent"
EVO_FILE="$TMP_BASE.evo"
CONTRA_FILE="$TMP_BASE.contra"
RECENT_SEEN="$TMP_BASE.recent.seen"
EVO_SEEN="$TMP_BASE.evo.seen"

: > "$RECENT_FILE"
: > "$EVO_FILE"
: > "$CONTRA_FILE"
: > "$RECENT_SEEN"
: > "$EVO_SEEN"

cleanup() {
  rm -f "$RECENT_FILE" "$EVO_FILE" "$CONTRA_FILE" "$RECENT_SEEN" "$EVO_SEEN"
}
trap cleanup EXIT

ANY_HIT=0

collect_section() {
  local section_file="$1"
  local seen_file="$2"
  local query="$3"
  shift 3
  local collections=("$@")
  local collection out rc line uri doc date summary

  for collection in "${collections[@]}"; do
    out="$($QMD_ENTRY search "$query" -c "$collection" -n 8 --files 2>/dev/null)"
    rc=$?
    if [ "$rc" -ne 0 ]; then
      echo "❌ QMD 检索失败: collection=$collection query=$query"
      echo "RESULT: QMD_UNAVAILABLE"
      return 2
    fi

    while IFS= read -r line; do
      [ -z "$line" ] && continue
      uri="$(printf '%s\n' "$line" | awk -F',' '{print $3}')"
      uri="$(trim_quotes "$uri")"
      [ -z "$uri" ] && continue

      if grep -Fqx "$uri" "$seen_file"; then
        continue
      fi
      echo "$uri" >> "$seen_file"

      doc="$($QMD_ENTRY get "$uri" -l 80 2>/dev/null)"
      date="$(extract_date_from_uri "$uri")"
      if [ -z "$date" ] && [ -n "$doc" ]; then
        date="$(extract_date_from_doc "$doc")"
      fi

      if [ -n "$date" ] && [ "$date" \< "$CUTOFF" ]; then
        continue
      fi

      summary="$(extract_summary_from_doc "$doc")"
      [ -z "$date" ] && date="unknown"

      printf -- "- [%s] %s | %s\n" "$date" "$uri" "$summary" >> "$section_file"
      ANY_HIT=1
    done <<< "$out"
  done

  return 0
}

collect_section "$RECENT_FILE" "$RECENT_SEEN" "$TOPIC" $RECENT_COLLECTIONS || exit $?
collect_section "$EVO_FILE" "$EVO_SEEN" "$TOPIC 演进记录" $EVOLUTION_COLLECTIONS || exit $?

if [ "$INCLUDE_CONTRADICTIONS" -eq 1 ]; then
  if [ -f "$CONTRADICTION_FILE" ]; then
    contra_hits="$(grep -n -F -- "$TOPIC" "$CONTRADICTION_FILE" || true)"
    if [ -n "$contra_hits" ]; then
      while IFS= read -r line; do
        [ -z "$line" ] && continue
        printf -- "- %s\n" "$line" >> "$CONTRA_FILE"
      done <<< "$contra_hits"
      ANY_HIT=1
    fi
  else
    echo "- (矛盾追踪文件不存在: $CONTRADICTION_FILE)" >> "$CONTRA_FILE"
  fi
fi

echo "=== query_history ==="
echo "skill: $SKILL"
echo "topic: $TOPIC"
echo "window_days: $WINDOW_DAYS"
echo "cutoff: $CUTOFF"

echo ""
echo "[recent-memory]"
if [ -s "$RECENT_FILE" ]; then
  cat "$RECENT_FILE"
else
  echo "- (无相关历史)"
fi

echo ""
echo "[wiki-evolution]"
if [ -s "$EVO_FILE" ]; then
  cat "$EVO_FILE"
else
  echo "- (无相关历史)"
fi

if [ "$INCLUDE_CONTRADICTIONS" -eq 1 ]; then
  echo ""
  echo "[contradictions]"
  if [ -s "$CONTRA_FILE" ]; then
    cat "$CONTRA_FILE"
  else
    echo "- (无相关历史)"
  fi
fi

if [ "$ANY_HIT" -eq 1 ]; then
  echo ""
  echo "RESULT: FOUND"
  exit 0
else
  echo ""
  echo "RESULT: EMPTY"
  exit 1
fi
