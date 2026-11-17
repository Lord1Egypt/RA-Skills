#!/usr/bin/env bash
# Phase timing. Sourced, not executed.
#
# Records how long each startup phase took, on every run, without a debug flag:
# the slow runs are the ones nobody thought to instrument. The log carries phase
# names and durations only -- never a URL, a route token, or a credential.

[[ -n "${__LINE_OA_PHASE_TIMING_LOADED:-}" ]] && return 0
__LINE_OA_PHASE_TIMING_LOADED=1

# Monotonic seconds. /proc/uptime is unaffected by wall-clock adjustments, which
# matters because these intervals are the whole point of the log.
phase_now() {
  local up
  read -r up _ < /proc/uptime
  printf '%s' "$up"
}

# phase_init <component> [runtime-dir]
phase_init() {
  local component="$1"
  local runtime_dir="${2:-${LINE_OA_SEND_CHAT_RUNTIME_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/line-oa-chat-send}}"
  __phase_component="$component"
  __phase_start="$(phase_now)"
  __phase_last="$__phase_start"
  __phase_names=()
  __phase_elapsed=()
  __phase_deltas=()
  __phase_dir="$runtime_dir/timing"
  mkdir -p "$__phase_dir"
  chmod 700 "$runtime_dir" "$__phase_dir" 2>/dev/null || true
  __phase_log="$__phase_dir/${component}-$(date -u +%Y%m%dT%H%M%SZ)-$$.log"
  : > "$__phase_log"
  chmod 600 "$__phase_log"
  printf '# component=%s started=%s\n' "$component" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$__phase_log"
}

# phase_mark <phase-name>
# The name is the only free text that reaches the log, and callers pass fixed
# identifiers -- never interpolated URLs or tokens.
phase_mark() {
  local name="$1" now elapsed delta
  now="$(phase_now)"
  elapsed="$(awk -v a="$now" -v b="$__phase_start" 'BEGIN{printf "%.3f", a-b}')"
  delta="$(awk -v a="$now" -v b="$__phase_last" 'BEGIN{printf "%.3f", a-b}')"
  __phase_last="$now"
  __phase_names+=("$name")
  __phase_elapsed+=("$elapsed")
  __phase_deltas+=("$delta")
  printf '%-28s elapsed=%8ss delta=%8ss\n' "$name" "$elapsed" "$delta" >> "$__phase_log"
}

# phase_summary [stream]  -- defaults to stderr so it never pollutes stdout,
# which callers may be parsing for a URL.
phase_summary() {
  local stream="${1:-2}"
  {
    printf '\n--- phase timing (%s) ---\n' "$__phase_component"
    local i
    for i in "${!__phase_names[@]}"; do
      printf '  %-28s %8ss  (+%ss)\n' "${__phase_names[$i]}" "${__phase_elapsed[$i]}" "${__phase_deltas[$i]}"
    done
    printf '  %-28s %8ss\n' "TOTAL" "${__phase_elapsed[${#__phase_elapsed[@]}-1]:-0.000}"
    printf '  log: %s\n' "$__phase_log"
  } >&"$stream"
}

phase_log_path() { printf '%s' "$__phase_log"; }
