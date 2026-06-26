#!/usr/bin/env bash
set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq is required" >&2
  exit 1
fi

TIMER_JSON="$(cat)"
if [[ -z "${TIMER_JSON// }" ]]; then
  echo "error: empty timer json" >&2
  exit 1
fi

BASE_DIR_DEFAULT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE_DIR="${NERVTIMER_BASE_DIR:-$BASE_DIR_DEFAULT}"

echo "$TIMER_JSON" | jq -c --arg base_dir "$BASE_DIR" '
  def schedule_from_timer:
    if .schedule_type == "one_shot" then
      {kind:"at", at:.scheduled_for}
    elif .schedule_type == "recurrent" then
      if .recurrence.mode == "cron" then
        {kind:"cron", expr:.recurrence.cron_expr, tz:(.timezone // empty)}
      else
        {kind:"every", everyMs:.recurrence.every_ms}
      end
    else
      error("invalid schedule_type")
    end;

  . as $t
  | {
      arm_job: {
        name: ("nervtimer-arm-" + $t.timer_id),
        enabled: true,
        schedule: ($t | schedule_from_timer),
        sessionTarget: "isolated",
        wakeMode: "next-heartbeat",
        payload: {
          kind: "agentTurn",
          message:
            (
              "NERVTIMER ARM for timer_id=" + $t.timer_id + ". " +
              "Run deterministic state transition with: " +
              "bash " + $base_dir + "/scripts/state.sh start-nagging " + $t.timer_id + ". " +
              "Then generate one short reminder in the assistant personality. " +
              "Task: " + $t.title +
              (if ($t.reason // "") != "" then ". Reason: " + $t.reason else "" end) +
              "."
            )
        },
        delivery: {
          mode: "announce"
        }
      },
      nag_job: {
        name: ("nervtimer-nag-" + $t.timer_id),
        enabled: true,
        schedule: {kind:"every", everyMs:300000},
        sessionTarget: "isolated",
        wakeMode: "next-heartbeat",
        payload: {
          kind: "agentTurn",
          message:
            (
              "NERVTIMER NAG TICK for timer_id=" + $t.timer_id + ". " +
              "Call bash " + $base_dir + "/scripts/state.sh next-nag " + $t.timer_id + " and parse JSON result. " +
              "If should_nag=false, do not send a reminder. " +
              "If should_nag=true, send exactly one short reminder in German " +
              "with tone based on tone_stage and increasing urgency by nag_count. " +
              "Never insult or threaten."
            )
        },
        delivery: {
          mode: "announce"
        }
      }
    }
'
