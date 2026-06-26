#!/usr/bin/env bash
# OpenClaw Security Self-Check
# Reads openclaw.json and host state, outputs a structured report.
# No modifications — read-only audit.
# Usage: ./security-check.sh [--json]

set -euo pipefail

JSON_OUTPUT=false
[[ "${1:-}" == "--json" ]] && JSON_OUTPUT=true

# --- Locate config ---
OPENCLAW_DIR="${HOME}/.openclaw"
CONFIG_FILE="${OPENCLAW_DIR}/openclaw.json"

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "ERROR: Config not found at $CONFIG_FILE"
  exit 1
fi

CONFIG=$(cat "$CONFIG_FILE")

# --- Helpers ---
pass() { echo "PASS"; }
warn() { echo "WARN"; }
fail() { echo "FAIL"; }
skip() { echo "SKIP"; }

jq_val() { echo "$CONFIG" | python3 -c "import sys,json; d=json.load(sys.stdin); print(${1})" 2>/dev/null || echo ""; }

# --- Check 1: Gateway Bind ---
check1_name="Gateway Bind Address"
bind_val=$(jq_val "d.get('gateway',{}).get('bind','loopback')")
if [[ -z "$bind_val" || "$bind_val" == "loopback" || "$bind_val" == "localhost" || "$bind_val" == "127.0.0.1" || "$bind_val" == "::1" ]]; then
  check1_status=$(pass)
  check1_detail="bind=${bind_val:-loopback (default)}"
  check1_severity=""
elif [[ "$bind_val" == "0.0.0.0" || "$bind_val" == "::" ]]; then
  check1_status=$(fail)
  check1_detail="bind=$bind_val — exposed to all interfaces!"
  check1_severity="CRITICAL"
else
  check1_status=$(warn)
  check1_detail="bind=$bind_val — non-standard, verify intent"
  check1_severity="MEDIUM"
fi

# --- Check 2: Gateway Auth Mode ---
check2_name="Gateway Auth Mode"
auth_mode=$(jq_val "d.get('gateway',{}).get('auth',{}).get('mode','token')")
if [[ -z "$auth_mode" || "$auth_mode" == "token" || "$auth_mode" == "password" ]]; then
  check2_status=$(pass)
  check2_detail="mode=${auth_mode:-token (default)}"
  check2_severity=""
elif [[ "$auth_mode" == "off" || "$auth_mode" == "none" ]]; then
  check2_status=$(fail)
  check2_detail="mode=$auth_mode — no authentication!"
  check2_severity="CRITICAL"
else
  check2_status=$(warn)
  check2_detail="mode=$auth_mode — non-standard"
  check2_severity="HIGH"
fi

# --- Check 3: Token Strength ---
check3_name="Gateway Token Strength"
if [[ "$auth_mode" == "password" ]]; then
  check3_status=$(skip)
  check3_detail="password mode, skipping token check"
  check3_severity=""
else
  token_val=$(jq_val "d.get('gateway',{}).get('auth',{}).get('token','')")
  token_len=${#token_val}
  if [[ $token_len -ge 32 ]]; then
    check3_status=$(pass)
    check3_detail="${token_len} chars"
    check3_severity=""
  elif [[ $token_len -ge 16 ]]; then
    check3_status=$(warn)
    check3_detail="${token_len} chars — recommend 32+"
    check3_severity="MEDIUM"
  else
    check3_status=$(fail)
    check3_detail="${token_len} chars — too weak!"
    check3_severity="HIGH"
  fi
fi

# --- Check 4: DM Policy (per channel) ---
check4_name="DM Policy"
dm_channels=$(jq_val "','.join([k for k,v in d.get('channels',{}).items() if isinstance(v,dict)])")
if [[ -z "$dm_channels" ]]; then
  check4_status=$(skip)
  check4_detail="no channels configured"
  check4_severity=""
else
  check4_issues=""
  IFS=',' read -ra channels <<< "$dm_channels"
  for ch in "${channels[@]}"; do
    ch=$(echo "$ch" | xargs)  # trim
    dm_policy=$(jq_val "d.get('channels',{}).get('$ch',{}).get('dmPolicy','pairing')")
    allow_from=$(jq_val "str(len(d.get('channels',{}).get('$ch',{}).get('allowFrom',[])))")
    if [[ "$dm_policy" == "open" && "$allow_from" == "0" ]]; then
      check4_issues="${check4_issues}${ch}(open+no allowFrom) "
    fi
  done
  if [[ -z "$check4_issues" ]]; then
    check4_status=$(pass)
    check4_detail="all channels have safe DM policy"
    check4_severity=""
  else
    check4_status=$(fail)
    check4_detail="$check4_issues"
    check4_severity="HIGH"
  fi
fi

# --- Check 5: Group Policy (per channel) ---
check5_name="Group Policy"
if [[ -z "$dm_channels" ]]; then
  check5_status=$(skip)
  check5_detail="no channels configured"
  check5_severity=""
else
  check5_issues=""
  for ch in "${channels[@]}"; do
    ch=$(echo "$ch" | xargs)
    grp_policy=$(jq_val "d.get('channels',{}).get('$ch',{}).get('groupPolicy','allowlist')")
    if [[ "$grp_policy" == "open" || "$grp_policy" == "any" ]]; then
      check5_issues="${check5_issues}${ch}($grp_policy) "
    fi
  done
  if [[ -z "$check5_issues" ]]; then
    check5_status=$(pass)
    check5_detail="all channels use allowlist"
    check5_severity=""
  else
    check5_status=$(fail)
    check5_detail="$check5_issues"
    check5_severity="HIGH"
  fi
fi

# --- Check 6: Config File Permissions ---
check6_name="Config File Permissions"
if [[ "$(uname)" == "Darwin" ]]; then
  file_perm=$(stat -f '%Lp' "$CONFIG_FILE" 2>/dev/null || echo "unknown")
else
  file_perm=$(stat -c '%a' "$CONFIG_FILE" 2>/dev/null || echo "unknown")
fi
if [[ "$file_perm" == "600" || "$file_perm" == "400" ]]; then
  check6_status=$(pass)
  check6_detail="permissions $file_perm"
  check6_severity=""
elif [[ "$file_perm" == "644" || "$file_perm" == "640" ]]; then
  check6_status=$(warn)
  check6_detail="permissions $file_perm — group/others can read"
  check6_severity="MEDIUM"
elif [[ "$file_perm" == "unknown" ]]; then
  check6_status=$(skip)
  check6_detail="could not determine permissions"
  check6_severity=""
else
  check6_status=$(fail)
  check6_detail="permissions $file_perm — too permissive!"
  check6_severity="HIGH"
fi

# --- Check 7: Plaintext Secrets in Config ---
check7_name="Plaintext Secrets Scan"
secret_keys=$(jq_val """
secrets = []
def scan(obj, path=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and v and any(s in k.lower() for s in ['password','secret','apikey','api_key','privatekey','private_key']) and 'token' not in k.lower():
                secrets.append(path + '.' + k if path else k)
            scan(v, path + '.' + k if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            scan(v, path)
scan(d)
print(','.join(secrets) if secrets else '')
""")
if [[ -z "$secret_keys" ]]; then
  check7_status=$(pass)
  check7_detail="no plaintext secrets found"
  check7_severity=""
else
  check7_status=$(warn)
  check7_detail="found: $secret_keys"
  check7_severity="MEDIUM"
fi

# --- Check 8: Host Firewall ---
check8_name="Host Firewall"
if command -v ufw &>/dev/null; then
  fw_status=$(sudo ufw status 2>/dev/null | head -1 || echo "unknown")
  if echo "$fw_status" | grep -qi "active"; then
    check8_status=$(pass)
    check8_detail="UFW active"
    check8_severity=""
  else
    check8_status=$(fail)
    check8_detail="UFW installed but inactive"
    check8_severity="HIGH"
  fi
elif command -v firewall-cmd &>/dev/null; then
  fw_state=$(firewall-cmd --state 2>/dev/null || echo "unknown")
  if [[ "$fw_state" == "running" ]]; then
    check8_status=$(pass)
    check8_detail="firewalld running"
    check8_severity=""
  else
    check8_status=$(fail)
    check8_detail="firewalld installed but not running"
    check8_severity="HIGH"
  fi
else
  check8_status=$(fail)
  check8_detail="no firewall found (ufw/firewalld)"
  check8_severity="HIGH"
fi

# --- Check 9: SSH Configuration ---
check9_name="SSH Hardening"
sshd_config="/etc/ssh/sshd_config"
if [[ -r "$sshd_config" ]]; then
  pw_auth=$(grep -E "^PasswordAuthentication" "$sshd_config" 2>/dev/null | awk '{print $2}' || echo "unknown")
  root_login=$(grep -E "^PermitRootLogin" "$sshd_config" 2>/dev/null | awk '{print $2}' || echo "unknown")
  issues=""
  [[ "$pw_auth" == "yes" ]] && issues="${issues}PasswordAuth=yes "
  [[ "$root_login" == "yes" ]] && issues="${issues}RootLogin=yes "
  if [[ -z "$issues" ]]; then
    check9_status=$(pass)
    check9_detail="PasswordAuth=${pw_auth:-default} RootLogin=${root_login:-default}"
    check9_severity=""
  else
    check9_status=$(warn)
    check9_detail="$issues— recommend disabling"
    check9_severity="MEDIUM"
  fi
elif ! command -v sshd &>/dev/null; then
  check9_status=$(skip)
  check9_detail="sshd not installed"
  check9_severity=""
else
  check9_status=$(skip)
  check9_detail="cannot read $sshd_config"
  check9_severity=""
fi

# --- Check 10: Exposed Ports ---
check10_name="Exposed Listening Ports"
if command -v ss &>/dev/null; then
  exposed=$(ss -ltnp 2>/dev/null | grep -v "127.0.0" | grep -v "::1" | grep "LISTEN" | wc -l)
  if [[ "$exposed" -le 3 ]]; then
    check10_status=$(pass)
    check10_detail="${exposed} non-loopback listening ports"
    check10_severity=""
  elif [[ "$exposed" -le 8 ]]; then
    check10_status=$(warn)
    check10_detail="${exposed} non-loopback listening ports — review if all needed"
    check10_severity="MEDIUM"
  else
    check10_status=$(fail)
    check10_detail="${exposed} non-loopback listening ports — too many!"
    check10_severity="HIGH"
  fi
else
  check10_status=$(skip)
  check10_detail="ss not available"
  check10_severity=""
fi

# --- Output ---
icon() {
  case "$1" in
    PASS) echo "✅" ;;
    WARN) echo "⚠️" ;;
    FAIL) echo "❌" ;;
    SKIP) echo "⏭️" ;;
  esac
}

pass_count=0; warn_count=0; fail_count=0; skip_count=0

for i in $(seq 1 10); do
  eval "s=\$check${i}_status"
  case "$s" in
    PASS) pass_count=$((pass_count + 1)) ;;
    WARN) warn_count=$((warn_count + 1)) ;;
    FAIL) fail_count=$((fail_count + 1)) ;;
    SKIP) skip_count=$((skip_count + 1)) ;;
  esac
done

if $JSON_OUTPUT; then
  echo "{"
  echo "  \"summary\": {\"pass\": $pass_count, \"warn\": $warn_count, \"fail\": $fail_count, \"skip\": $skip_count},"
  echo "  \"checks\": ["
  for i in $(seq 1 10); do
    eval "name=\$check${i}_name"
    eval "status=\$check${i}_status"
    eval "detail=\$check${i}_detail"
    eval "severity=\$check${i}_severity"
    comma=","
    [[ $i -eq 10 ]] && comma=""
    echo "    {\"id\": $i, \"name\": \"$name\", \"status\": \"$status\", \"detail\": \"$detail\", \"severity\": \"$severity\"}${comma}"
  done
  echo "  ]"
  echo "}"
else
  echo ""
  echo "🔒 OpenClaw Security Check Report"
  echo "=================================="
  echo ""
  for i in $(seq 1 10); do
    eval "name=\$check${i}_name"
    eval "status=\$check${i}_status"
    eval "detail=\$check${i}_detail"
    eval "severity=\$check${i}_severity"
    sev_tag=""
    [[ -n "$severity" ]] && sev_tag=" [$severity]"
    printf "%2d. %-28s %s %s — %s%s\n" "$i" "$name" "$(icon $status)" "$status" "$detail" "$sev_tag"
  done
  echo ""
  echo "Score: ${pass_count}/10 PASS, ${warn_count} WARN, ${fail_count} FAIL, ${skip_count} SKIP"
  echo ""
fi
