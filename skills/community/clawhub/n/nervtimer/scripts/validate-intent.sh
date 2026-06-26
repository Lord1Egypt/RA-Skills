#!/usr/bin/env bash
set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq is required" >&2
  exit 1
fi

INPUT="$(cat)"

if [[ -z "${INPUT// }" ]]; then
  echo "error: empty input" >&2
  exit 1
fi

echo "$INPUT" | jq -e '
  def is_non_empty_string: (type == "string" and (gsub("^\\s+|\\s+$";"") | length) > 0);

  . as $root
  | ($root.action | is_non_empty_string)
  and (
    if $root.action == "create_timer" then
      ($root.timer.title | is_non_empty_string)
      and (($root.timer.schedule_type == "one_shot") or ($root.timer.schedule_type == "recurrent"))
      and (
        if $root.timer.schedule_type == "one_shot" then
          ($root.timer.scheduled_for | is_non_empty_string)
        else
          ($root.timer.recurrence.mode == "cron" or $root.timer.recurrence.mode == "every_ms")
          and (
            if $root.timer.recurrence.mode == "cron" then
              ($root.timer.recurrence.cron_expr | is_non_empty_string)
            else
              (($root.timer.recurrence.every_ms | type) == "number")
              and ($root.timer.recurrence.every_ms >= 60000)
            end
          )
        end
      )
    elif ($root.action == "complete_timer" or $root.action == "cancel_timer" or $root.action == "list_active") then
      true
    else
      false
    end
  )
' >/dev/null

echo "$INPUT" | jq -c .
