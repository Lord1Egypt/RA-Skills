#!/usr/bin/env bash
# ip-consistency.sh — Compare IPv4 and IPv6 firewall rules for divergence
# Usage: bash ip-consistency.sh [CHAIN]
#   Default chain: INPUT
#   Checks: OUTPUT, FORWARD
#   With --all: checks INPUT + OUTPUT + FORWARD
# Requires: iptables, ip6tables, nft (optional, auto-detected)
set -euo pipefail

# Detect which backend is active and snapshot rules
snapshot_rules() {
  if command -v nft >/dev/null 2>&1 && nft list ruleset >/dev/null 2>&1 && [ -n "$(nft list ruleset 2>/dev/null)" ]; then
    # nftables native mode — use -s to strip counters for stable diffs
    nft -s list ruleset
    return 0
  else
    # Legacy iptables mode
    echo "# v4"
    sudo iptables-save 2>/dev/null | grep -v '^#'
    echo "# v6"
    sudo ip6tables-save 2>/dev/null | grep -v '^#'
    return 0
  fi
}

BACKEND="iptables"
if command -v nft >/dev/null 2>&1 && nft list ruleset >/dev/null 2>&1 && [ -n "$(nft list ruleset 2>/dev/null)" ]; then
  BACKEND="nftables"
fi
echo "Detected backend: $BACKEND"

CHAIN="${1:-INPUT}"
if [ "$CHAIN" = "--all" ]; then
  CHAINS="INPUT OUTPUT FORWARD"
else
  CHAINS="$CHAIN"
fi

# Normalize rules: strip counters, addresses, version-specific tokens
normalize() {
  local binary="$1" chain="$2"
  "$binary" -S "$chain" 2>/dev/null \
    | grep -E -- '--dport|--sport' \
    | sed -E \
        -e 's/-A [A-Z]+ //' \
        -e 's/ -m (tcp|udp|state|conntrack) / /g' \
        -e 's/ --state [A-Z,]+//' \
        -e 's/ --ctstate [A-Z,]+//' \
    | awk '{$1=$1; print}' \
    | sort -u
}

HAS_DIFF=0

for CH in $CHAINS; do
  echo "=== Chain: $CH ==="

  v4_rules=$(normalize iptables  "$CH" || echo "")
  v6_rules=$(normalize ip6tables "$CH" || echo "")

  if [ -z "$v4_rules" ] && [ -z "$v6_rules" ]; then
    echo "Result: OK — no dport/sport rules on either stack (empty chain for $CH)"
    continue
  fi

  if [ -z "$v4_rules" ] && [ -n "$v6_rules" ]; then
    echo "Result: DIFF — IPv6 has rules but IPv4 has none → v4 is open while v6 is restricted"
    HAS_DIFF=1
    continue
  fi
  if [ -n "$v4_rules" ] && [ -z "$v6_rules" ]; then
    echo "Result: DIFF — IPv4 has rules but IPv6 has none → v6 is open while v4 is restricted"
    HAS_DIFF=1
    continue
  fi

  diff_output=$(diff <(echo "$v4_rules") <(echo "$v6_rules") || true)
  if [ -z "$diff_output" ]; then
    echo "Result: OK — port/protocol rules match between IPv4 and IPv6"
  else
    echo "Result: DIFF — divergence detected:"
    echo "$diff_output"
    HAS_DIFF=1
  fi

  # Also check default policies
  p4=$(sudo iptables  -S "$CH" 2>/dev/null | head -1 || echo "-P ${CH} UNKNOWN")
  p6=$(sudo ip6tables -S "$CH" 2>/dev/null | head -1 || echo "-P ${CH} UNKNOWN")
  if [ "$p4" != "$p6" ]; then
    echo "Default policy mismatch: v4='$p4' v6='$p6'"
    HAS_DIFF=1
  else
    echo "Default policy: $p4 (both stacks)"
  fi
done

if [ "$HAS_DIFF" -eq 0 ]; then
  echo ""
  echo "=== OVERALL: PASS — IPv4/IPv6 rules consistent ==="
  exit 0
else
  echo ""
  echo "=== OVERALL: WARN — IPv4/IPv6 divergence found ==="
  exit 1
fi
