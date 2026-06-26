#!/bin/bash
set -eu

VAULT="${OPENCLAW_VAULT:-${VAULT_ROOT:-$(pwd)}}"
WIKI_REL=""
SECTION=""
CONTENT_TEXT=""
CONTENT_FILE=""
MODE="append"

usage() {
  echo "用法: wiki_entry_content_write.sh --wiki <wiki> --section <heading> (--content <text> | --content-file <file>) [--mode <append|replace>] [--vault <vault>]" >&2
}

error() {
  echo "❌ $*" >&2
}

warn() {
  echo "⚠️  $*" >&2
}

abs_path() {
  local p="$1"
  case "$p" in
    /*) printf '%s' "$p" ;;
    *) printf '%s/%s' "$VAULT" "$p" ;;
  esac
}

normalize_file() {
  local input_file="$1"
  local output_file="$2"

  awk '
    { lines[++n] = $0 }
    END {
      start = 1
      while (start <= n && lines[start] ~ /^[[:space:]]*$/) {
        start++
      }
      end = n
      while (end >= start && lines[end] ~ /^[[:space:]]*$/) {
        end--
      }
      for (i = start; i <= end; i++) {
        print lines[i]
      }
    }
  ' "$input_file" > "$output_file"
}

section_info() {
  local file_path="$1"
  awk -v section="$SECTION" '
    $0 == section {
      count++
      if (start == 0) {
        start = NR
      }
    }
    END {
      if (start == 0) {
        print "0 0"
      } else {
        print start, count
      }
    }
  ' "$file_path"
}

section_end_line() {
  local file_path="$1"
  local start_line="$2"
  local target_level="$3"

  awk -v start_line="$start_line" -v target_level="$target_level" '
    function heading_level(line) {
      if (line ~ /^#+ /) {
        match(line, /^#+ /)
        return RLENGTH - 1
      }
      return 0
    }

    NR <= start_line { next }

    {
      current_level = heading_level($0)
      if (current_level > 0 && current_level <= target_level) {
        print NR - 1
        found = 1
        exit
      }
    }

    END {
      if (!found) {
        print NR
      }
    }
  ' "$file_path"
}

extract_body() {
  local file_path="$1"
  local start_line="$2"
  local end_line="$3"
  local output_file="$4"

  if [ "$end_line" -le "$start_line" ]; then
    : > "$output_file"
    return
  fi

  awk -v start_line="$start_line" -v end_line="$end_line" '
    NR > start_line && NR <= end_line { print }
  ' "$file_path" > "$output_file"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --wiki)
      WIKI_REL="$2"; shift 2 ;;
    --section)
      SECTION="$2"; shift 2 ;;
    --content)
      CONTENT_TEXT="$2"; shift 2 ;;
    --content-file)
      CONTENT_FILE="$2"; shift 2 ;;
    --mode)
      MODE="$2"; shift 2 ;;
    --vault)
      VAULT="$2"; shift 2 ;;
    *)
      error "未知参数: $1"
      usage
      exit 1 ;;
  esac
done

if [ -z "$WIKI_REL" ] || [ -z "$SECTION" ]; then
  usage
  exit 1
fi

if [ -n "$CONTENT_TEXT" ] && [ -n "$CONTENT_FILE" ]; then
  error "不能同时提供 --content 和 --content-file"
  exit 1
fi

if [ -z "$CONTENT_TEXT" ] && [ -z "$CONTENT_FILE" ]; then
  error "必须提供 --content 或 --content-file"
  exit 1
fi

case "$MODE" in
  append|replace) ;;
  *)
    error "--mode 只能是 append 或 replace"
    exit 1 ;;
esac

case "$SECTION" in
  \#*" "*) ;;
  *)
    error "章节标题格式不支持: $SECTION"
    exit 1 ;;
esac

SECTION_MARKS="${SECTION%% *}"
SECTION_LEVEL="${#SECTION_MARKS}"
WIKI="$(abs_path "$WIKI_REL")"

if [ ! -f "$WIKI" ]; then
  error "Wiki 不存在: $WIKI"
  exit 1
fi

WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/wiki-entry-content.XXXXXX")"
trap 'rm -rf "$WORK_DIR"' EXIT

RAW_CONTENT_FILE="$WORK_DIR/raw-content.txt"
NORMALIZED_CONTENT_FILE="$WORK_DIR/content-normalized.txt"
EXISTING_BODY_FILE="$WORK_DIR/existing-body.txt"
NORMALIZED_EXISTING_BODY_FILE="$WORK_DIR/existing-body-normalized.txt"
NEW_BODY_FILE="$WORK_DIR/new-body.txt"
UPDATED_BODY_FILE="$WORK_DIR/updated-body.txt"
UPDATED_BODY_NORMALIZED_FILE="$WORK_DIR/updated-body-normalized.txt"
TMP_WIKI="$WIKI.tmp.$$"

if [ -n "$CONTENT_FILE" ]; then
  if [ ! -f "$CONTENT_FILE" ]; then
    error "content-file 不存在: $CONTENT_FILE"
    exit 1
  fi
  cp "$CONTENT_FILE" "$RAW_CONTENT_FILE"
else
  printf '%s\n' "$CONTENT_TEXT" > "$RAW_CONTENT_FILE"
fi

normalize_file "$RAW_CONTENT_FILE" "$NORMALIZED_CONTENT_FILE"

set -- $(section_info "$WIKI")
SECTION_START="$1"
SECTION_COUNT="$2"

if [ "$SECTION_START" -eq 0 ]; then
  error "章节不存在：$SECTION"
  exit 1
fi

if [ "$SECTION_COUNT" -gt 1 ]; then
  warn "存在重复章节：$SECTION"
fi

SECTION_END="$(section_end_line "$WIKI" "$SECTION_START" "$SECTION_LEVEL")"
TOTAL_LINES="$(awk 'END { print NR }' "$WIKI")"

extract_body "$WIKI" "$SECTION_START" "$SECTION_END" "$EXISTING_BODY_FILE"
normalize_file "$EXISTING_BODY_FILE" "$NORMALIZED_EXISTING_BODY_FILE"

case "$MODE" in
  append)
    if [ -s "$NORMALIZED_EXISTING_BODY_FILE" ] && [ -s "$NORMALIZED_CONTENT_FILE" ]; then
      {
        cat "$NORMALIZED_EXISTING_BODY_FILE"
        printf '\n'
        cat "$NORMALIZED_CONTENT_FILE"
      } > "$NEW_BODY_FILE"
    elif [ -s "$NORMALIZED_EXISTING_BODY_FILE" ]; then
      cp "$NORMALIZED_EXISTING_BODY_FILE" "$NEW_BODY_FILE"
    else
      cp "$NORMALIZED_CONTENT_FILE" "$NEW_BODY_FILE"
    fi
    ;;
  replace)
    cp "$NORMALIZED_CONTENT_FILE" "$NEW_BODY_FILE"
    ;;
esac

{
  if [ "$SECTION_START" -gt 1 ]; then
    awk -v end_line="$((SECTION_START - 1))" 'NR <= end_line { print }' "$WIKI"
  fi

  printf '%s\n' "$SECTION"

  if [ -s "$NEW_BODY_FILE" ]; then
    if [ "$MODE" = "replace" ]; then
      printf '\n'
    fi
    cat "$NEW_BODY_FILE"
  fi

  if [ "$SECTION_END" -lt "$TOTAL_LINES" ]; then
    printf '\n'
    awk -v start_line="$((SECTION_END + 1))" 'NR >= start_line { print }' "$WIKI"
  fi
} > "$TMP_WIKI"

mv "$TMP_WIKI" "$WIKI"

set -- $(section_info "$WIKI")
UPDATED_SECTION_START="$1"
UPDATED_SECTION_END="$(section_end_line "$WIKI" "$UPDATED_SECTION_START" "$SECTION_LEVEL")"

extract_body "$WIKI" "$UPDATED_SECTION_START" "$UPDATED_SECTION_END" "$UPDATED_BODY_FILE"
normalize_file "$UPDATED_BODY_FILE" "$UPDATED_BODY_NORMALIZED_FILE"

case "$MODE" in
  append)
    FIRST_CONTENT_LINE="$(awk 'NF { print; exit }' "$NORMALIZED_CONTENT_FILE")"
    if [ -n "$FIRST_CONTENT_LINE" ] && ! grep -Fqx -- "$FIRST_CONTENT_LINE" "$UPDATED_BODY_FILE"; then
      error "回读失败：新增内容未出现在目标章节"
      exit 1
    fi
    ;;
  replace)
    if ! cmp -s "$NORMALIZED_CONTENT_FILE" "$UPDATED_BODY_NORMALIZED_FILE"; then
      error "回读失败：章节内容与期望写入内容不一致"
      exit 1
    fi
    ;;
esac

LAST_BYTE="$(tail -c 1 "$WIKI" || true)"
if [ -n "$LAST_BYTE" ]; then
  error "回读失败：文件未以单个换行结束"
  exit 1
fi

echo "✅ 章节写入完成"
echo "  Wiki: $WIKI"
echo "  Section: $SECTION"
echo "  Mode: $MODE"
exit 0
