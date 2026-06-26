#!/bin/bash
# hearth/scripts/lib/probe.sh — 5-layer probe primitives
# Read-only library — sourced by other scripts.

# Build the L2-L4 remote bundle command.
# This is what gets sent over SSH (or run locally) — produces pipe-delimited output
# parsed by the caller via awk -F'|'.
#
# Args: services_csv (comma-separated list, or empty)
# Echoes the bash command string.
hearth_build_remote_bundle() {
  local services="$1"
  local services_loop=""
  if [ -n "$services" ]; then
    # Convert comma-separated list to space-separated for `for` loop
    local svc_list
    svc_list=$(echo "$services" | tr ',' ' ')
    services_loop="SVC=\"\"; for s in $svc_list; do SVC=\"\$SVC \$s=\$(systemctl is-active \$s 2>/dev/null)\"; done"
  fi

  cat <<REMOTE_END
UP=\$(uptime -p 2>/dev/null | sed "s/^up //")
LD=\$(awk '{print \$1, \$2, \$3}' /proc/loadavg 2>/dev/null)
MEM=\$(free -h 2>/dev/null | awk '/^Mem:/ {print "used " \$3 " / " \$2 ", " \$7 " avail"}')
DSK=\$(df -h / 2>/dev/null | awk 'NR==2 {print "/ " \$5 " used, " \$4 " free"}')
$services_loop
echo "L2|\$UP|\$LD"
echo "L3|\$MEM|\$DSK"
echo "L4|\$SVC"
REMOTE_END
}

# Parse pipe-delimited L2/L3/L4/L5b output and pretty-print to stdout
# Reads from stdin
hearth_format_layers() {
  awk -F'|' '
    /^L2/ {print "  L2 uptime:  " $2 ", load: " $3}
    /^L3/ {print "  L3 mem:     " $2 " | disk: " $3}
    /^L4/ {
      svc = $2
      sub(/^ /, "", svc)
      print "  L4 svc:     " svc
    }
  '
}

# Format a "no SSH" device's L2-L4 output (for http-only and no_systemd cases)
hearth_format_no_ssh() {
  local mode="$1"  # "http-only" or "no-systemd"
  case "$mode" in
    http-only)
      echo "  L2 uptime:  unmanaged-host (no SSH)"
      echo "  L3 mem:     unmanaged-host (no SSH)"
      echo "  L4 svc:     unmanaged-host (no SSH/WMI access)"
      ;;
    no-systemd)
      # L2/L3 still work via SSH on a chroot — this is only for L4
      echo "  L4 svc:     no-systemd (chroot — N/A)"
      ;;
  esac
}

# Run an HTTP probe and emit a single-line summary
# Args: name url expect_code expect_match auth_header_env verify_tls
hearth_http_probe() {
  local name="$1"
  local url="$2"
  local expect_code="${3:-200}"
  local expect_match="$4"
  local auth_header_env="$5"
  local verify_tls="${6:-true}"
  local resolve="$7"

  local curl_opts=(-s --max-time 4 -o /tmp/.hearth_probe -w "%{http_code}")
  [ "$verify_tls" = "false" ] && curl_opts+=(-k)
  [ -n "$auth_header_env" ] && curl_opts+=(-H "Authorization: Bearer ${!auth_header_env}")
  [ -n "$resolve" ] && curl_opts+=(--resolve "$resolve")

  local code
  code=$(curl "${curl_opts[@]}" "$url" 2>/dev/null || echo "000")

  local result
  if [ "$code" = "$expect_code" ]; then
    result="$name=HTTP $code"
    if [ -n "$expect_match" ]; then
      if grep -qE "$expect_match" /tmp/.hearth_probe 2>/dev/null; then
        result="$result OK"
      else
        result="$result MISMATCH"
      fi
    fi
  else
    result="$name=HTTP $code (expected $expect_code)"
  fi

  rm -f /tmp/.hearth_probe
  echo "$result"
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