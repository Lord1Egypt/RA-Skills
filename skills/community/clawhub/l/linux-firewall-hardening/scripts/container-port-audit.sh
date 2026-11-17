#!/usr/bin/env bash
# container-port-audit.sh — External reachability check + Docker DNAT bypass detection
# Usage: bash container-port-audit.sh [<target-ipv4>] [<target-ipv6>]
#   With IPs: runs external TCP/UDP checks from THIS host to the target
#   Without IPs: runs local container port audit only
# Requires: nc, ss, bash (with /dev/tcp compiled in)
set -euo pipefail

TARGET4="${1:-}"
TARGET6="${2:-}"
TIMEOUT=3

# ─── Port classification via /dev/tcp ───────────────────────────────
classify_tcp() {
  local host="$1" port="$2" to="${3:-$TIMEOUT}"
  local start elapsed
  start=$(date +%s%N)
  if timeout "$to" bash -c "exec 3<>/dev/tcp/${host}/${port}" 2>/dev/null; then
    echo "OPEN"
  else
    end=$(date +%s%N)
    elapsed=$(( (end - start) / 1000000 ))
    if [ "$elapsed" -ge $(( to * 1000 - 200 )) ]; then
      echo "FILTERED(drop)"
    else
      echo "REFUSED(reject)"
    fi
  fi
}

check_udp() {
  local host="$1" port="$2" to="${3:-$TIMEOUT}"
  # Remote probe: nc -u -z -w with verbose flag for best-effort detection
  if nc -uzvw"$to" "$host" "$port" 2>&1 | grep -qE 'open|succeeded'; then
    echo "OPEN|FILTERED"
  else
    echo "REFUSED(closed)"
  fi
}

check_udp_local() {
  # Deterministic local check — bypasses UDP probe ambiguity entirely
  local port="$1"
  if sudo ss -ulnpH 2>/dev/null | grep -q ":${port} "; then
    echo "OPEN(local listener)"
  else
    echo "CLOSED(no listener)"
  fi
}

# ─── External reachability (when target IPs provided) ────────────────
if [ -n "$TARGET4" ] || [ -n "$TARGET6" ]; then
  echo "=== External Reachability Check ==="
  EXPECTED_OPEN="22 443"
  EXPECTED_CLOSED="80 3306 5432 6379 8080 9090"

  for family in "v4:$TARGET4:TCP" "v6:$TARGET6:TCP"; do
    label="${family%%:*}" target="${family#*:}" target="${target%%:*}"
    [ -z "$target" ] && continue
    echo "-- $label TCP --"
    for port in $EXPECTED_OPEN; do
      state=$(classify_tcp "$target" "$port")
      echo "  tcp/${port}: $state"
    done
    for port in $EXPECTED_CLOSED; do
      state=$(classify_tcp "$target" "$port")
      echo "  tcp/${port}: $state"
    done
  done

  for family in "v4:$TARGET4:UDP" "v6:$TARGET6:UDP"; do
    label="${family%%:*}" target="${family#*:}" target="${target%%:*}"
    [ -z "$target" ] && continue
    echo "-- $label UDP --"
    for port in 53 123 161; do
      state=$(check_udp "$target" "$port")
      echo "  udp/${port}: $state"
    done
  done
fi

# ─── Container port DNAT audit (always run) ─────────────────────────
echo ""
echo "=== Container Port DNAT Audit ==="

echo "-- Listening sockets (runtime-owned) --"
sudo ss -tulnpH 2>/dev/null | grep -Ei 'docker|containerd|conmon|podman' | awk '{print $5}' | sort -u || echo "  (none)"

echo "-- NAT DNAT rules (published ports) --"
sudo iptables -t nat -S 2>/dev/null | grep -Ei 'DNAT|DOCKER|CNI' || echo "  (none)"

echo "-- FORWARD chain (container traffic) --"
sudo iptables -t filter -S FORWARD 2>/dev/null | grep -Ei 'DOCKER|br-|cni|podman|veth' || echo "  (none)"

echo ""
echo "=== Container Port Exposure Assessment ==="
dnat_ports=$(sudo iptables -t nat -S 2>/dev/null | grep -oE 'dport [0-9]+' | awk '{print $2}' | sort -u)
if [ -z "$dnat_ports" ]; then
  echo "Result: PASS — no container DNAT ports detected"
else
  echo "Result: WARN — ports exposed via DNAT (bypass INPUT filtering): ${dnat_ports}"
  echo "These ports are NOT protected by INPUT DROP policies. Verify each is intentional."
fi
