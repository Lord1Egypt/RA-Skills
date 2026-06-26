#!/usr/bin/env bash
# Usage: indeed_check_pending.sh [--help]
# Checks all pending snapshots, fetches completed ones, removes them from pending.
# Env: BRIGHTDATA_API_KEY (required)
# Output: Structured JSON: {"completed":[...],"still_pending":[...],"failed":[...]}
# Exit: 0 if any results fetched or no pending, 1 on error, 2 if all still running

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
source "${SCRIPT_DIR}/_lib.sh"

readonly STALE_THRESHOLD_HOURS=24

show_help() {
  cat >&2 <<'EOF'
Usage: indeed_check_pending.sh [OPTIONS]

Check all pending Indeed snapshots. Fetches completed results and removes
them from the pending queue.

Options:
  --help               Show this help message

Exit Codes:
  0    Success (results fetched, or no pending snapshots)
  1    Error occurred
  2    All snapshots still running (none ready)

Output:
  Structured JSON: {"completed":[...],"still_pending":[...],"failed":[...]}
EOF
  exit 0
}

check_stale() {
  local triggered_at="$1"
  local description="$2"
  local now_epoch
  now_epoch=$(date -u +%s)
  local entry_epoch
  # GNU date -d, then BSD date -jf, then fallback to 0
  entry_epoch=$(date -u -d "$triggered_at" +%s 2>/dev/null || \
                date -u -jf "%Y-%m-%dT%H:%M:%S" "${triggered_at%%Z*}" +%s 2>/dev/null || \
                echo "0")
  local age_hours
  age_hours=$(( (now_epoch - entry_epoch) / 3600 ))

  if [[ "$age_hours" -ge "$STALE_THRESHOLD_HOURS" ]]; then
    echo "Warning: stale pending entry (${age_hours}h old): ${description}" >&2
  fi
}

main() {
  if [[ "${1:-}" == "--help" ]]; then
    show_help
  fi

  cleanup_old_entries

  local pending
  pending=$(load_pending)

  local count
  count=$(echo "$pending" | jq 'length')

  if [[ "$count" -eq 0 ]]; then
    echo "No pending snapshots." >&2
    jq -n '{"completed":[],"still_pending":[],"failed":[]}'
    exit 0
  fi

  echo "Checking ${count} pending snapshot(s)..." >&2

  local completed="[]"
  local still_pending="[]"
  local failed="[]"
  local fetched_count=0
  local error_count=0

  for i in $(seq 0 $((count - 1))); do
    local entry
    entry=$(echo "$pending" | jq ".[$i]")
    local snapshot_id
    snapshot_id=$(echo "$entry" | jq -r '.snapshot_id')
    local description
    description=$(echo "$entry" | jq -r '.description')
    local triggered_at
    triggered_at=$(echo "$entry" | jq -r '.triggered_at')

    if ! _validate_snapshot_id "$snapshot_id"; then
      echo "Error: skipping invalid snapshot_id in pending entry: ${description}" >&2
      # Direct removal — remove_pending would fail the same validation
      local tmp_pending
      tmp_pending=$(mktemp "${LIB_PENDING_FILE}.XXXXXX")
      if jq --arg sid "$snapshot_id" '[.[] | select(.snapshot_id != $sid)]' \
        "$LIB_PENDING_FILE" > "$tmp_pending" 2>/dev/null; then
        mv -f "$tmp_pending" "$LIB_PENDING_FILE"
      else
        rm -f "$tmp_pending"
      fi
      error_count=$((error_count + 1))
      continue
    fi

    check_stale "$triggered_at" "$description"

    local body
    body=$(make_api_request GET "${LIB_BASE_URL}/progress/${snapshot_id}")
    _read_http_code
    if ! check_http_status "$HTTP_CODE" "$body" "progress check for ${snapshot_id}"; then
      error_count=$((error_count + 1))
      continue
    fi

    local status
    status=$(echo "$body" | jq -r '.status // "unknown"')

    case "$status" in
      ready)
        echo "Fetching results for: ${description}" >&2
        local results
        results=$(make_api_request GET "${LIB_BASE_URL}/snapshot/${snapshot_id}?format=json")
        _read_http_code
        if check_http_status "$HTTP_CODE" "$results" "snapshot fetch for ${snapshot_id}"; then
          if save_result_file "$snapshot_id" "$results"; then
            local result_count
            result_count=$(echo "$results" | jq 'if type == "array" then length else 0 end')
            local result_file="${LIB_RESULTS_DIR}/${snapshot_id}.json"
            completed=$(echo "$completed" | jq \
              --arg sid "$snapshot_id" \
              --arg desc "$description" \
              --argjson rc "$result_count" \
              --arg rf "$result_file" \
              '. + [{"snapshot_id":$sid,"query_description":$desc,"result_count":$rc,"result_file":$rf}]')
            remove_pending "$snapshot_id" || echo "Warning: failed to remove pending entry for ${snapshot_id}" >&2
            fetched_count=$((fetched_count + 1))
          else
            echo "Warning: failed to save results for ${snapshot_id}" >&2
            failed=$(echo "$failed" | jq \
              --arg sid "$snapshot_id" \
              --arg desc "$description" \
              --arg reason "failed to save result file" \
              '. + [{"snapshot_id":$sid,"query_description":$desc,"reason":$reason}]')
            error_count=$((error_count + 1))
          fi
        else
          error_count=$((error_count + 1))
        fi
        ;;
      failed)
        echo "Error: snapshot ${snapshot_id} failed (${description})" >&2
        local reason
        reason=$(echo "$body" | jq -r '.reason // "snapshot failed"')
        failed=$(echo "$failed" | jq \
          --arg sid "$snapshot_id" \
          --arg desc "$description" \
          --arg reason "$reason" \
          '. + [{"snapshot_id":$sid,"query_description":$desc,"reason":$reason}]')
        remove_pending "$snapshot_id" || echo "Warning: failed to remove pending entry for ${snapshot_id}" >&2
        error_count=$((error_count + 1))
        ;;
      *)
        echo "Still running: ${description} (snapshot ${snapshot_id})" >&2
        still_pending=$(echo "$still_pending" | jq \
          --arg sid "$snapshot_id" \
          --arg desc "$description" \
          '. + [{"snapshot_id":$sid,"query_description":$desc}]')
        ;;
    esac
  done

  echo "Summary: ${fetched_count} fetched, $(echo "$still_pending" | jq 'length') still running, ${error_count} errors" >&2

  jq -n \
    --argjson completed "$completed" \
    --argjson still_pending "$still_pending" \
    --argjson failed "$failed" \
    '{"completed":$completed,"still_pending":$still_pending,"failed":$failed}'

  if [[ "$fetched_count" -gt 0 ]]; then
    exit 0
  elif [[ "$error_count" -gt 0 ]]; then
    exit 1
  else
    exit 2
  fi
}

main "$@"
