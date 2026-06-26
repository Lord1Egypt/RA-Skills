#!/usr/bin/env bash
# scripts/gig-task-wait.sh — wait for a gig-task to gather enough approved
# (or completed) results. `linkedclaw gig-task get` is a single-shot query
# (no --wait flag, unlike `linkedclaw recv`), so this script supplies the
# polling loop. Slicing the wait into short calls also keeps each tool
# invocation under the typical agent runtime's per-call yield ceiling.
#
# Usage:
#   gig-task-wait.sh <task_id> [--until <field>=<n>] [--total-seconds <s>]
#                              [--poll-seconds <s>]
#
# Default targets: --until completed_count=1, --total-seconds 600,
# --poll-seconds 15 (per-call wait).
#
# --until accepts any numeric field from the task record:
#   accepted_count, completed_count, approved_count
#
# Exit 0 if the target field reached the requested count within the budget
# (final task record echoed to stdout as JSON). Exit 1 if the deadline
# elapsed before reaching the target (latest record still echoed).
#
# Why this exists:
#   The skill's broadcast pattern (Pattern 3) used to say "Poll until enough
#   results come in" but left the loop to the agent. Reconstructing a
#   polling loop on each invocation invites mistakes — exit-code handling
#   on the get, parsing the right field name, choosing slice sizes that
#   don't blow through a runtime's tool-call yield. Encoded once here, all
#   runtimes get the same correct loop with a single tool call.

set -u

TASK="${1:?usage: gig-task-wait.sh <task_id> [--until field=N] [--total-seconds S] [--poll-seconds S]}"
shift

UNTIL_FIELD="completed_count"
UNTIL_N=1
TOTAL=600
POLL=15

while [ $# -gt 0 ]; do
  case "$1" in
    --until)
      pair="${2:?--until needs <field>=<n>}"
      UNTIL_FIELD="${pair%%=*}"
      UNTIL_N="${pair#*=}"
      shift 2 ;;
    --total-seconds)
      TOTAL="${2:?--total-seconds needs a value}"; shift 2 ;;
    --poll-seconds)
      POLL="${2:?--poll-seconds needs a value}"; shift 2 ;;
    *)
      echo "{\"error\": \"unknown arg: $1\"}" >&2; exit 2 ;;
  esac
done

case "$UNTIL_FIELD" in
  accepted_count|completed_count|approved_count) ;;
  *)
    echo "{\"error\": \"--until field must be accepted_count|completed_count|approved_count, got: $UNTIL_FIELD\"}" >&2
    exit 2 ;;
esac

DEADLINE=$(( $(date +%s) + TOTAL ))
record=""

while [ "$(date +%s)" -lt "$DEADLINE" ]; do
  record=$(linkedclaw gig-task get "$TASK" 2>&1) || {
    # Surface the CLI's own error frame and bail — usually invalid task id
    # or auth issue; retrying won't help.
    echo "$record"
    exit 1
  }
  current=$(echo "$record" | jq -r --arg f "$UNTIL_FIELD" '.[$f] // 0' 2>/dev/null || echo 0)
  if [ "$current" -ge "$UNTIL_N" ] 2>/dev/null; then
    echo "$record"
    exit 0
  fi
  # Don't oversleep past the deadline.
  remaining=$(( DEADLINE - $(date +%s) ))
  [ "$remaining" -le 0 ] && break
  sleep_for=$(( remaining < POLL ? remaining : POLL ))
  sleep "$sleep_for"
done

echo "$record"
exit 1
