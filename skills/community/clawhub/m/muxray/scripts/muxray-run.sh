#!/usr/bin/env bash
# muxray-run.sh — a safe, validating front door to muxray.
#
# Why this exists: the agent should never build a muxray command by
# interpolating untrusted text into a shell string. This wrapper accepts only a
# fixed set of read-only subcommands and a fixed set of flags, validates every
# argument against a strict charset, and execs muxray through an argv array
# (never `sh -c`). Unknown subcommands, unknown flags, or malformed targets are
# rejected before muxray is invoked.
#
# It deliberately does NOT expose `update`, `telemetry`, `bundle`, or `shim`:
# those touch the network or write diagnostic bundles and are operator actions,
# not steps in an observation loop.
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: muxray-run.sh <subcommand> [options]

Read-only subcommands:
  list | scan | status | snapshot | diff | inspect | watch | doctor

Validated options (forwarded verbatim as argv to muxray):
  --pane <target>     session | session:window.pane | %paneid | $sessionid
  --session <name>    session name
  --since <file|id>   previous snapshot for diff/inspect
  --until <states>    comma list of: idle,running,blocked,waiting_for_input,
                      needs_approval,error,completed,unknown
  --timeout <dur>     e.g. 5m, 30s, 200ms
  --interval <dur>    poll cadence
  --out <file>        write target for snapshot
  --context <n>       integer
  --lines <n>         integer
  --max-items <n>     integer
  --text              terse human output instead of JSON
  --explain           attach rule trace
  --no-raw            drop raw capture
  --full              do not cap diff lines
  -h, --help          show this help
USAGE
}

die() { echo "muxray-run: $*" >&2; exit 2; }

# --- validators ---------------------------------------------------------------
# Patterns live in variables and are referenced UNQUOTED in [[ =~ ]] so the
# shell uses them literally as regexes (a quoted/inline pattern containing $@,
# $/, etc. would be mangled by parameter expansion). A target may start with %
# (pane id) or $ (session id) but never '-', so it can't be read as a flag.
TARGET_RE='^[A-Za-z0-9%$][A-Za-z0-9_.:%$@/-]*$'
PATHISH_RE='^[A-Za-z0-9][A-Za-z0-9_./:@-]*$'
INT_RE='^[0-9]+$'
DUR_RE='^[0-9]+(ms|s|m|h)?$'
valid_target()  { [[ "$1" =~ $TARGET_RE ]]; }
valid_pathish() { [[ "$1" =~ $PATHISH_RE ]]; }
valid_int()     { [[ "$1" =~ $INT_RE ]]; }
valid_dur()     { [[ "$1" =~ $DUR_RE ]]; }
valid_states()  {
  local IFS=','; local s
  for s in $1; do
    case "$s" in
      idle|running|blocked|waiting_for_input|needs_approval|error|completed|unknown) ;;
      *) return 1 ;;
    esac
  done
  return 0
}

[[ $# -ge 1 ]] || { usage >&2; exit 2; }
case "${1:-}" in -h|--help) usage; exit 0 ;; esac

sub="$1"; shift
case "$sub" in
  list|scan|status|snapshot|diff|inspect|watch|doctor) ;;
  *) die "subcommand not allowed: '$sub' (use one of: list scan status snapshot diff inspect watch doctor)" ;;
esac

# --- build argv ---------------------------------------------------------------
args=("$sub")
while [[ $# -gt 0 ]]; do
  case "$1" in
    --pane)
      v="${2-}"; [[ -n "$v" ]] || die "--pane needs a value"
      valid_target "$v" || die "invalid --pane target: '$v'"
      args+=("--pane" "$v"); shift 2 ;;
    --session)
      v="${2-}"; [[ -n "$v" ]] || die "--session needs a value"
      valid_target "$v" || die "invalid --session name: '$v'"
      args+=("--session" "$v"); shift 2 ;;
    --since)
      v="${2-}"; [[ -n "$v" ]] || die "--since needs a value"
      valid_pathish "$v" || die "invalid --since value: '$v'"
      args+=("--since" "$v"); shift 2 ;;
    --until)
      v="${2-}"; [[ -n "$v" ]] || die "--until needs a value"
      valid_states "$v" || die "invalid --until states: '$v'"
      args+=("--until" "$v"); shift 2 ;;
    --timeout)
      v="${2-}"; valid_dur "$v" || die "invalid --timeout: '$v'"
      args+=("--timeout" "$v"); shift 2 ;;
    --interval)
      v="${2-}"; valid_dur "$v" || die "invalid --interval: '$v'"
      args+=("--interval" "$v"); shift 2 ;;
    --out)
      v="${2-}"; [[ -n "$v" ]] || die "--out needs a value"
      valid_pathish "$v" || die "invalid --out path: '$v'"
      args+=("--out" "$v"); shift 2 ;;
    --context|--lines|--max-items)
      v="${2-}"; valid_int "$v" || die "invalid integer for $1: '$v'"
      args+=("$1" "$v"); shift 2 ;;
    --text|--explain|--no-raw|--full)
      args+=("$1"); shift ;;
    -h|--help) usage; exit 0 ;;
    --) shift; break ;;
    *) die "flag not allowed: '$1'" ;;
  esac
done
[[ $# -eq 0 ]] || die "unexpected trailing arguments"

command -v muxray >/dev/null 2>&1 || die "muxray not found in PATH (install: go install github.com/dandriscoll/muxray/cmd/muxray@latest)"

exec muxray "${args[@]}"
