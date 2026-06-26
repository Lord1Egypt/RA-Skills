#!/bin/bash
# report.sh - Generate daily KinemaTasks report (outputs to stdout)
#
# Usage: report.sh [TASK_DIR]
#   TASK_DIR: defaults to ~/.openclaw/workspace/kinema-tasks
#
# Reads last snapshot, scans active/, generates current status + diff report.
# Output should be sent to chat channel by the calling Agent.

TASK_DIR="${1:-$HOME/.openclaw/workspace/kinema-tasks}"
ACTIVE_DIR="$TASK_DIR/active"
ARCHIVE_DIR="$TASK_DIR/archived"
SNAP_DIR="$TASK_DIR/snapshots"

TODAY=$(TZ=Asia/Shanghai date +%Y-%m-%d)
TODAY_TS=$(TZ=Asia/Shanghai date -d "$TODAY" +%s)
TODAY_DISPLAY=$(TZ=Asia/Shanghai date +"%-m月%-d日")

# --- Helper: status symbol ---
status_sym() {
  case "$1" in
    "In Progress") echo "▶" ;;
    "Done") echo "✓" ;;
    *) echo "○" ;;
  esac
}

# --- Helper: time hint ---
# Prints: "Nd left" / "due today" / "Nd overdue" / "done" / empty
time_hint() {
  local due="$1"
  local is_done="$2"
  [ "$is_done" = "1" ] && echo "done" && return
  [ -z "$due" ] || [ "$due" = "—" ] && return
  local due_ts
  due_ts=$(TZ=Asia/Shanghai date -d "$due" +%s 2>/dev/null) || return
  local diff=$(( (due_ts - TODAY_TS) / 86400 ))

  if [ "$diff" -lt 0 ]; then
    echo "$((-diff))d overdue"
  elif [ "$diff" -eq 0 ]; then
    echo "due today"
  else
    echo "${diff}d left"
  fi
}

# --- Helper: sort key (seconds until due, negative=overdue, 999999999=no due) ---
sort_key() {
  local due="$1"
  [ -z "$due" ] || [ "$due" = "—" ] && echo 999999999 && return
  local due_ts
  due_ts=$(TZ=Asia/Shanghai date -d "$due" +%s 2>/dev/null) || echo 999999999 && return
  echo $(( due_ts - TODAY_TS ))
}

# --- Helper: format date as "Apr 09" ---
fmt_date() {
  local due="$1"
  [ -z "$due" ] || [ "$due" = "—" ] && echo "—" && return
  TZ=Asia/Shanghai date -d "$due" +"%b %d" 2>/dev/null || echo "$due"
}

# --- Find most recent snapshot ---
prev_snap=""
prev_date=""
if [ -d "$SNAP_DIR" ]; then
  prev_snap=$(ls -1 "$SNAP_DIR"/*.md 2>/dev/null | sort -r | head -1)
  [ -n "$prev_snap" ] && prev_date=$(basename "$prev_snap" .md)
fi

# --- Collect active tasks ---
# Format: "tid|title|status|priority|domain|due"
tasks_data=""
if [ -d "$ACTIVE_DIR" ]; then
  for f in "$ACTIVE_DIR"/TASK-*.md; do
    [ -f "$f" ] || continue
    tid=$(basename "$f" .md)
    title=$(grep "^# ${tid}: " "$f" | sed "s/^# ${tid}: //")
    status=$(grep "^| 状态 | " "$f" | sed 's/^| 状态 | \(.*\) |$/\1/')
    priority=$(grep "^| 优先级 | " "$f" | sed 's/^| 优先级 | \(.*\) |$/\1/')
    domain=$(grep "^| 领域 | " "$f" | sed 's/^| 领域 | \(.*\) |$/\1/')
    due=$(grep "^| 截止日期 | " "$f" | sed 's/^| 截止日期 | \(.*\) |$/\1/')
    [ -z "$title" ] && title="(无标题)"
    [ -z "$status" ] && status="Unknown"
    [ -z "$priority" ] && priority="normal"
    [ -z "$domain" ] && domain="—"
    [ -z "$due" ] && due="—"
    tasks_data="${tasks_data}${tid}|${title}|${status}|${priority}|${domain}|${due}
"
  done
fi

# --- Collect cancelled task IDs ---
declare -A cancelled_tasks
if [ -d "$ARCHIVE_DIR" ]; then
  for f in "$ARCHIVE_DIR"/TASK-*.md; do
    [ -f "$f" ] || continue
    tid=$(basename "$f" .md)
    st=$(grep "^| 状态 | " "$f" | sed 's/^| 状态 | \(.*\) |$/\1/')
    [ "$st" = "Cancelled" ] && cancelled_tasks["$tid"]=1
  done
fi

# --- Classify active tasks (not done) ---
declare -a urgent_list normal_list low_list snoozed_list expired_list

while IFS= read -r line; do
  [ -z "$line" ] && continue
  tid=$(echo "$line" | cut -d'|' -f1)
  title=$(echo "$line" | cut -d'|' -f2)
  status=$(echo "$line" | cut -d'|' -f3)
  priority=$(echo "$line" | cut -d'|' -f4)
  domain=$(echo "$line" | cut -d'|' -f5)
  due=$(echo "$line" | cut -d'|' -f6)

  sym=$(status_sym "$status")
  hint=$(time_hint "$due" "0")
  key=$(sort_key "$due")
  date_str=$(fmt_date "$due")

  hint_part=""
  [ -n "$hint" ] && hint_part=" ${hint}"
  entry="${sym} ${tid} ${date_str}${hint_part} ${title} #${domain}"

  if [ "$status" = "Snoozed" ]; then
    snoozed_list+=("${key}|${entry}")
  else
    is_expired=0
    [ "$due" != "—" ] && [ -n "$due" ] && [ "$TODAY" \> "$due" ] && is_expired=1
    if [ "$is_expired" -eq 1 ]; then
      expired_list+=("${key}|${entry}")
    else
      case "$priority" in
        urgent) urgent_list+=("${key}|${entry}") ;;
        normal) normal_list+=("${key}|${entry}") ;;
        low) low_list+=("${key}|${entry}") ;;
      esac
    fi
  fi
done <<< "$tasks_data"

# --- Collect recently done (last 5, separate section) ---
declare -a done_list
if [ -d "$ARCHIVE_DIR" ]; then
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    tid=$(echo "$line" | cut -d'|' -f1)
    title=$(echo "$line" | cut -d'|' -f2)
    priority=$(echo "$line" | cut -d'|' -f4)
    domain=$(echo "$line" | cut -d'|' -f5)
    last_upd=$(echo "$line" | cut -d'|' -f6)
    date_str=$(fmt_date "$last_upd")
    entry="✓ ${tid} ${date_str} done ${title} #${domain}"
    done_list+=("${entry}")
  done < <(
    for f in "$ARCHIVE_DIR"/TASK-*.md; do
      [ -f "$f" ] || continue
      tid=$(basename "$f" .md)
      st=$(grep "^| 状态 | " "$f" | sed 's/^| 状态 | \(.*\) |$/\1/')
      [ "$st" != "Done" ] && continue
      title=$(grep "^# ${tid}: " "$f" | sed "s/^# ${tid}: //")
      priority=$(grep "^| 优先级 | " "$f" | sed 's/^| 优先级 | \(.*\) |$/\1/')
      domain=$(grep "^| 领域 | " "$f" | sed 's/^| 领域 | \(.*\) |$/\1/')
      last_upd=$(grep "^| 最后更新 | " "$f" | sed 's/^| 最后更新 | \(.*\) |$/\1/')
      [ -z "$title" ] && title="(无标题)"
      [ -z "$priority" ] && priority="normal"
      [ -z "$domain" ] && domain="—"
      [ -z "$last_upd" ] && last_upd="—"
      echo "${tid}|${title}|Done|${priority}|${domain}|${last_upd}"
    done | sort -t'|' -k6 -r | head -5
  )
fi

# --- Stats ---
in_progress=0
pending=0
snoozed_count=0
total=0
while IFS= read -r line; do
  [ -z "$line" ] && continue
  st=$(echo "$line" | cut -d'|' -f3)
  total=$((total + 1))
  case "$st" in
    "In Progress") in_progress=$((in_progress + 1)) ;;
    "Pending") pending=$((pending + 1)) ;;
    "Snoozed") snoozed_count=$((snoozed_count + 1)) ;;
  esac
done <<< "$tasks_data"

# --- Build report ---
echo "📋 KinemaTasks Daily Report — ${TODAY_DISPLAY}"
echo ""

# (Summary slot for model to fill)
echo ""

echo "Status: ▶ in_progress ○ pending ✓ done"
echo ""

SEP="───────────────────────────────────────────────────────────────────────"

# Print a section
print_section() {
  local label="$1"
  shift
  local entries=("$@")
  [ ${#entries[@]} -eq 0 ] && return
  echo "● ${label} ${SEP:$((${#label}+2))}"
  # Sort by key ascending
  printf '%s\n' "${entries[@]}" | sort -t'|' -k1 -n | while IFS= read -r line; do
    [ -z "$line" ] && continue
    echo "$line" | sed 's/^[^|]*|//'
  done
  echo ""
}

# For expired: sort by key desc (most overdue first = most negative key)
print_section_desc() {
  local label="$1"
  shift
  local entries=("$@")
  [ ${#entries[@]} -eq 0 ] && return
  echo "● ${label} ${SEP:$((${#label}+2))}"
  printf '%s\n' "${entries[@]}" | sort -t'|' -k1 -rn | while IFS= read -r line; do
    [ -z "$line" ] && continue
    echo "$line" | sed 's/^[^|]*|//'
  done
  echo ""
}

print_section "URGENT" "${urgent_list[@]}"
print_section "NORMAL" "${normal_list[@]}"
print_section "LOW" "${low_list[@]}"
print_section "SNOOZED" "${snoozed_list[@]}"
print_section_desc "EXPIRED" "${expired_list[@]}"

# Recently done (no sort key, already sorted by completion date desc)
if [ ${#done_list[@]} -gt 0 ]; then
  echo "● RECENTLY DONE ${SEP:16}"
  for entry in "${done_list[@]}"; do
    echo "$entry"
  done
  echo ""
fi

echo "${SEP}"
echo ""

# --- Diff section ---
prev_display=""
if [ -n "$prev_snap" ]; then
  prev_display=$(TZ=Asia/Shanghai date -d "$prev_date" +"%-m/%-d" 2>/dev/null || echo "$prev_date")
  echo "📊 昨日变动（${prev_display} → ${TODAY_DISPLAY}）"
else
  echo "📊 昨日变动（首次运行，无历史快照）"
fi
echo ""

if [ -n "$prev_snap" ]; then
  declare -A prev_status prev_priority prev_domain prev_due
  while IFS= read -r line; do
    if [[ "$line" =~ ^\|[[:space:]]TASK- ]]; then
      IFS='|' read -r _ tid _ title _ status _ priority _ domain _ due <<< "$line"
      tid=$(echo "$tid" | tr -d ' ')
      status=$(echo "$status" | tr -d ' ')
      priority=$(echo "$priority" | tr -d ' ')
      domain=$(echo "$domain" | tr -d ' ')
      due=$(echo "$due" | tr -d ' ')
      prev_status["$tid"]="$status"
      prev_priority["$tid"]="$priority"
      prev_domain["$tid"]="$domain"
      prev_due["$tid"]="$due"
    fi
  done < "$prev_snap"

  new_tasks=""
  status_changes=""
  field_changes=""
  cancel_changes=""

  while IFS= read -r line; do
    [ -z "$line" ] && continue
    tid=$(echo "$line" | cut -d'|' -f1)
    title=$(echo "$line" | cut -d'|' -f2)
    status=$(echo "$line" | cut -d'|' -f3)
    priority=$(echo "$line" | cut -d'|' -f4)
    domain=$(echo "$line" | cut -d'|' -f5)
    due=$(echo "$line" | cut -d'|' -f6)

    if [ -z "${prev_status[$tid]}" ]; then
      new_tasks=" ${tid} ${title} | ${priority} | ${domain}\n${new_tasks}"
    else
      [ "${status}" != "${prev_status[$tid]}" ] && status_changes=" ${tid} ${prev_status[$tid]} → ${status}\n${status_changes}"
      field_diff=""
      [ "${priority}" != "${prev_priority[$tid]}" ] && field_diff="${field_diff}优先级 ${prev_priority[$tid]} → ${priority}, "
      [ "${domain}" != "${prev_domain[$tid]}" ] && field_diff="${field_diff}领域 ${prev_domain[$tid]} → ${domain}, "
      [ "${due}" != "${prev_due[$tid]}" ] && field_diff="${field_diff}截止日期 ${prev_due[$tid]} → ${due}, "
      [ -n "$field_diff" ] && field_changes=" ${tid} ${field_diff%, }\n${field_changes}"
    fi
  done <<< "$tasks_data"

  for tid in "${!prev_status[@]}"; do
    [ -n "$(echo "$tasks_data" | grep "^${tid}|")" ] && continue
    [ -n "${cancelled_tasks[$tid]}" ] && cancel_changes=" ${tid}\n${cancel_changes}"
  done

  has_diff=0
  if [ -n "$new_tasks" ]; then
    echo "新增 ($(echo -e "$new_tasks" | wc -l))"
    echo -e "$new_tasks"
    echo ""; has_diff=1
  fi
  if [ -n "$status_changes" ]; then
    echo "状态变更 ($(echo -e "$status_changes" | wc -l))"
    echo -e "$status_changes"
    echo ""; has_diff=1
  fi
  if [ -n "$field_changes" ]; then
    echo "字段变更 ($(echo -e "$field_changes" | wc -l))"
    echo -e "$field_changes"
    echo ""; has_diff=1
  fi
  if [ -n "$cancel_changes" ]; then
    echo "取消 ($(echo -e "$cancel_changes" | wc -l))"
    echo -e "$cancel_changes"
    echo ""; has_diff=1
  fi
  [ "$has_diff" -eq 0 ] && echo "无变动" && echo ""
else
  echo "（首次运行，无历史快照可供对比）"
  echo ""
fi
