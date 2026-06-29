#!/usr/bin/env bash
# muxray-watch-diff.sh — summarize one pane's working turn.
#
# Captures a baseline snapshot of a pane, blocks until the pane settles (stops
# being `running`), then prints what changed and the final classification. This
# is the canonical "what did this agent just do?" sequence.
#
# Safety: the pane target is validated against a strict charset and muxray is
# invoked via an argv array — no untrusted text ever reaches a shell.
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: muxray-watch-diff.sh -t <pane-target> [options]

Options:
  -t, --target    tmux pane target, required
                  (session | session:window.pane | %paneid | $sessionid)
  -u, --until     comma-separated settle states (default: muxray's default set)
  -T, --timeout   max time to wait, e.g. 5m, 30s (default: 5m)
  -i, --interval  poll cadence, e.g. 1s (default: muxray default)
  -h, --help      show this help

Output: three JSON documents on stdout in order — baseline snapshot meta,
the final watch classification, and the diff against the baseline.
USAGE
}

die() { echo "muxray-watch-diff: $*" >&2; exit 2; }
# Patterns in variables, referenced unquoted, so $@/$ in the charset are not
# expanded by the shell. Targets may start with % or $ but never '-'.
TARGET_RE='^[A-Za-z0-9%$][A-Za-z0-9_.:%$@/-]*$'
DUR_RE='^[0-9]+(ms|s|m|h)?$'
valid_target() { [[ "$1" =~ $TARGET_RE ]]; }
valid_dur()    { [[ "$1" =~ $DUR_RE ]]; }
valid_states() {
  local IFS=','; local s
  for s in $1; do
    case "$s" in
      idle|running|blocked|waiting_for_input|needs_approval|error|completed|unknown) ;;
      *) return 1 ;;
    esac
  done
}

target=""; until_states=""; timeout="5m"; interval=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--target)   target="${2-}"; shift 2 ;;
    -u|--until)    until_states="${2-}"; shift 2 ;;
    -T|--timeout)  timeout="${2-}"; shift 2 ;;
    -i|--interval) interval="${2-}"; shift 2 ;;
    -h|--help)     usage; exit 0 ;;
    *) die "unknown option: '$1'" ;;
  esac
done

[[ -n "$target" ]] || { usage >&2; exit 2; }
valid_target "$target" || die "invalid pane target: '$target'"
valid_dur "$timeout"   || die "invalid --timeout: '$timeout'"
[[ -z "$until_states" ]] || valid_states "$until_states" || die "invalid --until states: '$until_states'"
[[ -z "$interval" ]]     || valid_dur "$interval"        || die "invalid --interval: '$interval'"
command -v muxray >/dev/null 2>&1 || die "muxray not found in PATH"

baseline="$(mktemp "${TMPDIR:-/tmp}/muxray-baseline.XXXXXX.json")"
trap 'rm -f "$baseline"' EXIT

echo "# baseline snapshot"
muxray snapshot --pane "$target" --no-raw --out "$baseline"

echo "# waiting until settled"
watch_args=(watch --pane "$target" --timeout "$timeout")
[[ -n "$until_states" ]] && watch_args+=(--until "$until_states")
[[ -n "$interval" ]]     && watch_args+=(--interval "$interval")
# watch exits 5 on timeout; surface the final classification either way.
muxray "${watch_args[@]}" || true

echo "# what changed since baseline"
muxray diff --pane "$target" --since "$baseline"
