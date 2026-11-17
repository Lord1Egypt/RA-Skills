#!/bin/bash
# hearth/scripts/sweep.sh — run check-device.sh across all devices (read-only)
#
# Usage:
#   ./sweep.sh                       # full sweep (parallel), human-readable
#   ./sweep.sh --device <name>       # check just one device
#   ./sweep.sh --group <name>        # check just devices in a named group
#   ./sweep.sh --json                # machine-readable JSON (for agents/scripts)
#   ./sweep.sh --problems-only       # show only devices that are down/degraded
#   ./sweep.sh --watch <seconds>     # re-run every <seconds> until interrupted
#   ./sweep.sh --sequential          # disable parallelism (one device at a time)
#   ./sweep.sh --parallel <n>        # cap concurrent probes (default 8)
#   ./sweep.sh --no-color            # disable ANSI colour
#   ./sweep.sh --dry-run             # validate config, don't probe
#   ./sweep.sh --version             # print version
#   ./sweep.sh --help                # this message
#
# Exit code: 0 = all healthy   1 = one or more degraded   2 = one or more down

set -u

VERSION="0.3.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/config.sh
. "$SCRIPT_DIR/lib/config.sh"
# shellcheck source=lib/probe.sh
. "$SCRIPT_DIR/lib/probe.sh"

usage() {
  sed -n '4,20p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

# ---- Parse args ------------------------------------------------------------
single_device=""
group=""
dry_run=false
json_out=false
problems_only=false
watch_secs=""
max_parallel=8
color_flag=""
while [ $# -gt 0 ]; do
  case "$1" in
    --version) echo "hearth $VERSION"; exit 0;;
    --help|-h) usage;;
    --device)  single_device="$2"; shift 2;;
    --group)   group="$2"; shift 2;;
    --json)    json_out=true; shift;;
    --problems-only) problems_only=true; shift;;
    --watch)   watch_secs="$2"; shift 2;;
    --sequential) max_parallel=1; shift;;
    --parallel) max_parallel="$2"; shift 2;;
    --no-color) color_flag="--no-color"; HEARTH_COLOR=never; export HEARTH_COLOR; shift;;
    --dry-run) dry_run=true; shift;;
    *) echo "Unknown argument: $1" >&2; usage;;
  esac
done

hearth_color_init

# ---- Find config + parser --------------------------------------------------
config_path=$(hearth_find_config) || {
  echo "ERROR: no devices.yaml found." >&2
  echo "Set HEARTH_CONFIG, or create ~/.hearth/devices.yaml from examples/devices.example.yaml" >&2
  exit 2
}
parser=$(hearth_detect_yaml_parser) || {
  echo "ERROR: no YAML parser available. Install yq (https://github.com/mikefarah/yq) or python3 with PyYAML." >&2
  exit 2
}

# ---- Build device list -----------------------------------------------------
devices=()
if [ -n "$single_device" ]; then
  devices=("$single_device")
elif [ -n "$group" ]; then
  while IFS= read -r d; do [ -n "$d" ] && devices+=("$d"); done < <(hearth_get_group "$config_path" "$group")
  if [ "${#devices[@]}" -eq 0 ]; then
    echo "ERROR: group '$group' is empty or undefined in $config_path" >&2
    exit 2
  fi
else
  while IFS= read -r d; do [ -n "$d" ] && devices+=("$d"); done < <(hearth_list_devices "$config_path")
fi

if [ "${#devices[@]}" -eq 0 ]; then
  echo "ERROR: no devices found in $config_path" >&2
  exit 2
fi

# ---- Dry run ---------------------------------------------------------------
if [ "$dry_run" = "true" ]; then
  echo "# config: $config_path"
  echo "# yaml parser: $parser"
  echo "# DRY RUN — devices that would be probed:"
  for d in "${devices[@]}"; do echo "  - $d"; done
  exit 0
fi

device_timeout=$(hearth_get_default "$config_path" "device_timeout" "18")

# hearth_timeout: GNU timeout, gtimeout (macOS coreutils), or a perl fallback,
# or last-resort no-timeout. Keeps a single hung host from blocking the run.
if command -v timeout >/dev/null 2>&1; then
  HEARTH_TIMEOUT_BIN="timeout"
elif command -v gtimeout >/dev/null 2>&1; then
  HEARTH_TIMEOUT_BIN="gtimeout"
else
  HEARTH_TIMEOUT_BIN=""
fi
hearth_timeout() {
  local secs="$1"; shift
  if [ -n "$HEARTH_TIMEOUT_BIN" ]; then
    "$HEARTH_TIMEOUT_BIN" "$secs" "$@"
  elif command -v perl >/dev/null 2>&1; then
    perl -e 'my $s=shift; eval { local $SIG{ALRM}=sub{die}; alarm $s; exec @ARGV; }; exit 124;' "$secs" "$@"
  else
    "$@"
  fi
}

# ===========================================================================
# One pass of the sweep. Prints the full report. Sets WORST_RC.
# ===========================================================================
run_sweep() {
  local start end
  start=$(date +%s)
  local tmpdir
  tmpdir=$(mktemp -d "${TMPDIR:-/tmp}/.hearth_sweep.XXXXXX") || { echo "ERROR: mktemp failed" >&2; return 2; }

  local cd_flags=()
  [ "$json_out" = "true" ] && cd_flags+=(--json)
  [ -n "$color_flag" ] && cd_flags+=("$color_flag")

  # Launch probes (bounded concurrency), one output file per device (ordered by index).
  local i=0
  for d in "${devices[@]}"; do
    (
      hearth_timeout "$device_timeout" "$SCRIPT_DIR/check-device.sh" "${cd_flags[@]}" "$d" >"$tmpdir/$i.out" 2>&1
      echo $? >"$tmpdir/$i.rc"
    ) &
    i=$((i+1))
    # throttle to max_parallel running jobs
    while [ "$(jobs -rp | wc -l)" -ge "$max_parallel" ]; do
      wait -n 2>/dev/null || sleep 0.05
    done
  done
  wait

  # Aggregate + render in device order
  local total=${#devices[@]} healthy=0 degraded=0 down=0
  WORST_RC=0

  if [ "$json_out" = "true" ]; then
    printf '{\n'
    printf '  "timestamp": "%s",\n' "$(date -Iseconds 2>/dev/null || date)"
    printf '  "devices": [\n'
  else
    hearth_sweep_header ""
  fi

  local j=0 first_json=true
  for d in "${devices[@]}"; do
    local rc=0
    [ -f "$tmpdir/$j.rc" ] && rc=$(cat "$tmpdir/$j.rc" 2>/dev/null || echo 2)
    [ -z "$rc" ] && rc=2
    case "$rc" in
      0) healthy=$((healthy+1)) ;;
      1) degraded=$((degraded+1)); [ "$WORST_RC" -lt 1 ] && WORST_RC=1 ;;
      *) down=$((down+1)); WORST_RC=2 ;;
    esac

    # problems-only: skip healthy devices (text mode only)
    if [ "$problems_only" = "true" ] && [ "$rc" = "0" ] && [ "$json_out" != "true" ]; then
      j=$((j+1)); continue
    fi

    if [ "$json_out" = "true" ]; then
      local content
      content=$(cat "$tmpdir/$j.out" 2>/dev/null)
      if [ -n "$content" ]; then
        [ "$first_json" = "true" ] && first_json=false || printf ',\n'
        printf '    %s' "$content"
      fi
    else
      cat "$tmpdir/$j.out" 2>/dev/null
      echo ""
    fi
    j=$((j+1))
  done

  end=$(date +%s)
  local elapsed=$((end - start))

  if [ "$json_out" = "true" ]; then
    printf '\n  ],\n'
    printf '  "summary": {"total": %d, "healthy": %d, "degraded": %d, "down": %d, "elapsed_seconds": %d},\n' \
      "$total" "$healthy" "$degraded" "$down" "$elapsed"
    printf '  "exit_code": %d\n' "$WORST_RC"
    printf '}\n'
  else
    local scol="$C_GREEN"
    [ "$degraded" -gt 0 ] && scol="$C_AMBER"
    [ "$down" -gt 0 ] && scol="$C_RED"
    printf '=== %s%d/%d healthy%s' "$scol" "$healthy" "$total" "$C_RESET"
    [ "$degraded" -gt 0 ] && printf ', %s%d degraded%s' "$C_AMBER" "$degraded" "$C_RESET"
    [ "$down" -gt 0 ] && printf ', %s%d down%s' "$C_RED" "$down" "$C_RESET"
    printf ' — %ds ===\n' "$elapsed"
  fi

  rm -rf "$tmpdir"
  return 0
}

# ---- Run (optionally in a watch loop) --------------------------------------
WORST_RC=0
if [ -n "$watch_secs" ]; then
  trap 'echo; echo "hearth watch stopped."; exit $WORST_RC' INT
  while true; do
    clear 2>/dev/null || printf '\033[2J\033[H'
    printf '%shearth — watch every %ss — %s%s\n\n' "$C_DIM" "$watch_secs" "$(date 2>/dev/null)" "$C_RESET"
    run_sweep
    sleep "$watch_secs"
  done
else
  run_sweep
fi

exit $WORST_RC
