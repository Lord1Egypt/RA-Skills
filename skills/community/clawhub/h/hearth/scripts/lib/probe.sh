#!/bin/bash
# hearth/scripts/lib/probe.sh — 5-layer probe primitives
# Read-only library — sourced by other scripts.

# ---------------------------------------------------------------------------
# Colour support (TTY-aware, honours NO_COLOR and HEARTH_COLOR=never/always)
# ---------------------------------------------------------------------------
hearth_color_init() {
  # HEARTH_COLOR: auto (default) | always | never
  local mode="${HEARTH_COLOR:-auto}"
  local on=false
  case "$mode" in
    always) on=true ;;
    never)  on=false ;;
    *)
      # auto: colour only when stdout is a terminal and NO_COLOR is unset
      if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then on=true; fi
      ;;
  esac
  # C_BOLD/C_DIM are consumed by check-device.sh, which sources this file;
  # the SC2034 "unused" finding is a false positive from isolated analysis.
  # shellcheck disable=SC2034
  if [ "$on" = "true" ]; then
    C_RESET=$'\033[0m'; C_GREEN=$'\033[32m'; C_AMBER=$'\033[33m'
    C_RED=$'\033[31m'; C_BOLD=$'\033[1m'; C_DIM=$'\033[2m'
  else
    C_RESET=""; C_GREEN=""; C_AMBER=""; C_RED=""; C_BOLD=""; C_DIM=""
  fi
}

# Colour a status token (healthy|degraded|down) -> coloured [OK]/[DEGRADED]/[DOWN]
hearth_status_tag() {
  case "$1" in
    healthy)  printf '%s[OK]%s' "$C_GREEN" "$C_RESET" ;;
    degraded) printf '%s[DEGRADED]%s' "$C_AMBER" "$C_RESET" ;;
    down)     printf '%s[DOWN]%s' "$C_RED" "$C_RESET" ;;
    *)        printf '[%s]' "$1" ;;
  esac
}

# ---------------------------------------------------------------------------
# JSON helper — escape a string for embedding in a JSON double-quoted value
# ---------------------------------------------------------------------------
hearth_json_escape() {
  # Reads $1, prints an escaped string (without surrounding quotes)
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\t'/\\t}"
  s="${s//$'\r'/\\r}"
  s="${s//$'\n'/\\n}"
  printf '%s' "$s"
}

# ---------------------------------------------------------------------------
# Numeric threshold comparator for floats (load averages), no bc dependency.
# Returns 0 (true) if $1 > $2.
# ---------------------------------------------------------------------------
hearth_gt() {
  awk -v a="$1" -v b="$2" 'BEGIN { exit !(a+0 > b+0) }'
}

# ---------------------------------------------------------------------------
# Build the L2-L4 remote bundle command.
# Emits pipe-delimited lines parsed by the caller:
#   L2|<uptime>|<load1 load5 load15>
#   L3|<mem summary>|<disk summary>
#   L3R|<disk_pct>|<load1>|<ncpu>|<mem_total_kb>|<mem_avail_kb>|<temp_c>
#   L4|<svc1=state svc2=state ...>
#
# Args: services_csv (comma-separated list, or empty)
# ---------------------------------------------------------------------------
hearth_build_remote_bundle() {
  local services="$1"
  local services_loop=""
  if [ -n "$services" ]; then
    local svc_list
    svc_list=$(echo "$services" | tr ',' ' ')
    services_loop="SVC=\"\"; for s in $svc_list; do SVC=\"\$SVC \$s=\$(systemctl is-active \$s 2>/dev/null || echo unknown)\"; done"
  fi

  cat <<REMOTE_END
UP=\$(uptime -p 2>/dev/null | sed "s/^up //")
[ -z "\$UP" ] && UP=\$(uptime 2>/dev/null | sed "s/.*up //; s/,  *load.*//" )
LD=\$(awk '{print \$1, \$2, \$3}' /proc/loadavg 2>/dev/null)
LD1=\$(awk '{print \$1}' /proc/loadavg 2>/dev/null)
NCPU=\$(nproc 2>/dev/null || getconf _NPROCESSORS_ONLN 2>/dev/null || echo 1)
MEM=\$(free -h 2>/dev/null | awk '/^Mem:/ {print "used " \$3 " / " \$2 ", " \$7 " avail"}')
MT=\$(awk '/^MemTotal:/{print \$2}' /proc/meminfo 2>/dev/null)
MA=\$(awk '/^MemAvailable:/{print \$2}' /proc/meminfo 2>/dev/null)
DSK=\$(df -h / 2>/dev/null | awk 'NR==2 {print "/ " \$5 " used, " \$4 " free"}')
DPCT=\$(df -P / 2>/dev/null | awk 'NR==2 {gsub("%","",\$5); print \$5}')
TEMP=""
if [ -r /sys/class/thermal/thermal_zone0/temp ]; then
  TEMP=\$(awk '{printf "%.1f", \$1/1000}' /sys/class/thermal/thermal_zone0/temp 2>/dev/null)
elif command -v vcgencmd >/dev/null 2>&1; then
  TEMP=\$(vcgencmd measure_temp 2>/dev/null | grep -oE '[0-9]+\.[0-9]+')
fi
$services_loop
echo "L2|\$UP|\$LD"
echo "L3|\$MEM|\$DSK"
echo "L3R|\$DPCT|\${LD1:-0}|\${NCPU:-1}|\${MT:-0}|\${MA:-0}|\$TEMP"
echo "L4|\$SVC"
REMOTE_END
}

# Run an HTTP probe and emit a single-line summary.
# Uses a per-call mktemp file (no fixed /tmp path — safe under concurrency and
# against symlink pre-creation on shared hosts).
# Args: name url expect_code expect_match auth_header_env verify_tls resolve
hearth_http_probe() {
  local name="$1"
  local url="$2"
  local expect_code="${3:-200}"
  local expect_match="$4"
  local auth_header_env="$5"
  local verify_tls="${6:-true}"
  local resolve="$7"

  local body
  body=$(mktemp "${TMPDIR:-/tmp}/.hearth_probe.XXXXXX") || body=""

  local curl_opts=(-s --max-time 4 -w "%{http_code}")
  [ -n "$body" ] && curl_opts+=(-o "$body") || curl_opts+=(-o /dev/null)
  [ "$verify_tls" = "false" ] && curl_opts+=(-k)
  if [ -n "$auth_header_env" ]; then
    curl_opts+=(-H "Authorization: Bearer ${!auth_header_env:-}")
  fi
  [ -n "$resolve" ] && curl_opts+=(--resolve "$resolve")

  # curl always writes %{http_code} (000 on connect failure) to stdout, even
  # when it exits non-zero — so capture that and only default if truly empty.
  local code
  code=$(curl "${curl_opts[@]}" "$url" 2>/dev/null)
  [ -z "$code" ] && code="000"

  local result
  if [ "$code" = "$expect_code" ]; then
    result="$name=HTTP $code"
    if [ -n "$expect_match" ]; then
      if [ -n "$body" ] && grep -qE "$expect_match" "$body" 2>/dev/null; then
        result="$result OK"
      else
        result="$result MISMATCH"
      fi
    fi
  else
    result="$name=HTTP $code (expected $expect_code)"
  fi

  [ -n "$body" ] && rm -f "$body"
  echo "$result"
}

# Decide whether an HTTP probe result string represents a healthy app.
# Returns 0 if healthy, 1 if degraded.
hearth_http_ok() {
  case "$1" in
    *MISMATCH*)          return 1 ;;
    *"(expected "*)      return 1 ;;
    *=HTTP\ 000*)        return 1 ;;
    *)                   return 0 ;;
  esac
}

# Format and emit the timestamped sweep header
hearth_sweep_header() {
  local title="${1:-HOMELAB — ESTATE HEALTH SWEEP}"
  echo "=== $title ==="
  echo "Timestamp: $(date -Iseconds 2>/dev/null || date)"
  echo ""
}

# Format and emit the sweep footer
hearth_sweep_footer() {
  local seconds="$1"
  echo "=== sweep complete in ${seconds} seconds ==="
}
