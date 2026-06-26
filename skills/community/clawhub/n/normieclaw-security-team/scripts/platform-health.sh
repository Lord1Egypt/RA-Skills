#!/usr/bin/env bash
set -euo pipefail

# ============================================================================
# Security Team — Platform Council Health Checker
# Checks service uptime, disk usage, SSL certs, uncommitted git changes, memory.
# Output: JSON to stdout
# ============================================================================

# --- Workspace Root Detection ---
find_skill_root() {
    # Stay within the skill directory — do not traverse outside
    cd "$(dirname "$0")/.." && pwd
}")" && pwd)"
  echo "$(dirname "$(dirname "$script_dir")")"
}

SKILL_DIR="$(cd "$(find_skill_root)" && pwd -P)"
CONFIG_FILE="$SKILL_DIR/config/security-config.json"

# --- OS Detection ---
OS="$(uname -s)"

# --- Dependency Detection ---
HAS_JQ=false
HAS_OPENSSL=false

command -v jq >/dev/null 2>&1 && HAS_JQ=true
command -v openssl >/dev/null 2>&1 && HAS_OPENSSL=true

# --- Config Loading ---
DOMAINS=()
SERVICES=()
SCAN_DIRS=()
DISK_WARN=85
DISK_CRIT=95
SSL_WARN_DAYS=30
SSL_CRIT_DAYS=7

resolve_scan_dir() {
  local rel_dir="$1"
  [ -n "$rel_dir" ] || return 1
  case "$rel_dir" in
    /*) return 1 ;;
  esac

  local candidate="$SKILL_DIR/$rel_dir"
  [ -d "$candidate" ] || return 1

  local resolved
  resolved="$(cd "$candidate" 2>/dev/null && pwd -P)" || return 1
  case "$resolved" in
    "$SKILL_DIR"|"$SKILL_DIR"/*) echo "$resolved" ;;
    *) return 1 ;;
  esac
}

is_http_url() {
  local url="$1"
  [[ "$url" =~ ^https?://[^[:space:]]+$ ]]
}

if [ -f "$CONFIG_FILE" ] && $HAS_JQ; then
  while IFS= read -r url; do
    [ -n "$url" ] && [[ "$url" != _comment* ]] || continue
    if is_http_url "$url"; then
      DOMAINS+=("$url")
    fi
  done < <(jq -r '.domains[]? // empty' "$CONFIG_FILE" 2>/dev/null)

  # Load enabled services
  while IFS= read -r svc; do
    [ -n "$svc" ] && SERVICES+=("$svc")
  done < <(jq -r '.services[]? | select(.enabled == true) | "\(.name)|\(.port)|\(.health_endpoint)"' "$CONFIG_FILE" 2>/dev/null)

  while IFS= read -r dir; do
    [ -n "$dir" ] && [[ "$dir" != _comment* ]] || continue
    local_safe_dir="$(resolve_scan_dir "$dir" || true)"
    [ -n "$local_safe_dir" ] && SCAN_DIRS+=("$local_safe_dir")
  done < <(jq -r '.scan_directories[]? // empty' "$CONFIG_FILE" 2>/dev/null)

  DISK_WARN=$(jq -r '.thresholds.disk_warning_percent // 85' "$CONFIG_FILE" 2>/dev/null)
  DISK_CRIT=$(jq -r '.thresholds.disk_critical_percent // 95' "$CONFIG_FILE" 2>/dev/null)
  SSL_WARN_DAYS=$(jq -r '.thresholds.ssl_warn_days // 30' "$CONFIG_FILE" 2>/dev/null)
  SSL_CRIT_DAYS=$(jq -r '.thresholds.ssl_critical_days // 7' "$CONFIG_FILE" 2>/dev/null)
fi

# --- Output Collection ---
FINDINGS="[]"

add_finding() {
  local severity="$1"
  local description="$2"
  local location="$3"
  local remediation="$4"
  local hash
  hash="$(echo -n "${severity}-${description}-${location}" | shasum -a 256 | cut -c1-16)"

  if $HAS_JQ; then
    FINDINGS=$(echo "$FINDINGS" | jq \
      --arg sev "$severity" \
      --arg desc "$description" \
      --arg loc "$location" \
      --arg rem "$remediation" \
      --arg hash "$hash" \
      '. + [{"hash": $hash, "council": "platform", "severity": $sev, "description": $desc, "location": $loc, "remediation": $rem}]')
  else
    local entry="{\"hash\":\"$hash\",\"council\":\"platform\",\"severity\":\"$severity\",\"description\":\"$description\",\"location\":\"$location\",\"remediation\":\"$remediation\"}"
    if [ "$FINDINGS" = "[]" ]; then
      FINDINGS="[$entry]"
    else
      FINDINGS="${FINDINGS%]}, $entry]"
    fi
  fi
}

# --- Check 1: Web Endpoint Health ---
check_endpoints() {
  for url in "${DOMAINS[@]}"; do
    is_http_url "$url" || continue
    local http_code
    http_code=$(curl -sL -o /dev/null -w '%{http_code}' --connect-timeout 10 --max-time 15 "$url" 2>/dev/null || echo "000")

    if [ "$http_code" = "000" ]; then
      add_finding "CRITICAL" "Endpoint unreachable (connection failed)" "$url" "Check if the server is running and DNS is resolving correctly."
    elif [[ "$http_code" =~ ^5 ]]; then
      add_finding "CRITICAL" "Endpoint returning HTTP $http_code (server error)" "$url" "Check server logs for errors."
    elif [[ "$http_code" =~ ^4 ]] && [ "$http_code" != "401" ] && [ "$http_code" != "403" ]; then
      add_finding "MEDIUM" "Endpoint returning HTTP $http_code" "$url" "Verify the URL is correct and the resource exists."
    fi
    # 2xx, 3xx, 401, 403 are considered OK (auth-protected is fine)
  done
}

# --- Check 2: Local Service Status ---
check_services() {
  for svc_str in "${SERVICES[@]}"; do
    IFS='|' read -r name port endpoint <<< "$svc_str"

    local status="down"
    if [ -n "$endpoint" ] && is_http_url "$endpoint"; then
      local http_code
      http_code=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 --max-time 10 "$endpoint" 2>/dev/null || echo "000")
      if [[ "$http_code" =~ ^[23] ]]; then
        status="up"
      fi
    fi

    if [ "$status" = "down" ]; then
      # Fallback: check if anything is listening on the port
      if command -v lsof >/dev/null 2>&1; then
        if lsof -i :"$port" -sTCP:LISTEN >/dev/null 2>&1; then
          status="up"
        fi
      elif command -v ss >/dev/null 2>&1; then
        if ss -tlnp | grep -q ":$port " 2>/dev/null; then
          status="up"
        fi
      fi
    fi

    if [ "$status" = "down" ]; then
      add_finding "CRITICAL" "$name is DOWN (port $port not responding)" "localhost:$port" "Start $name or check its configuration."
    fi
  done
}

# --- Check 3: Disk Usage ---
check_disk() {
  local usage
  if [ "$OS" = "Darwin" ]; then
    usage=$(df -h / | tail -1 | awk '{print $5}' | tr -d '%')
  else
    usage=$(df -h / | tail -1 | awk '{print $5}' | tr -d '%')
  fi

  if [ -n "$usage" ] 2>/dev/null; then
    if [ "$usage" -ge "$DISK_CRIT" ] 2>/dev/null; then
      add_finding "CRITICAL" "Disk usage at ${usage}% (critical threshold: ${DISK_CRIT}%)" "/" "Free up disk space immediately. Check large files with 'du -sh /* | sort -hr | head -20'."
    elif [ "$usage" -ge "$DISK_WARN" ] 2>/dev/null; then
      add_finding "MEDIUM" "Disk usage at ${usage}% (warning threshold: ${DISK_WARN}%)" "/" "Consider cleaning up old files, logs, or caches."
    fi
  fi
}

# --- Check 4: SSL Certificate Expiry ---
check_ssl() {
  $HAS_OPENSSL || return 0

  for url in "${DOMAINS[@]}"; do
    # Extract hostname from URL
    local host
    host=$(echo "$url" | sed -E 's|https?://||' | cut -d/ -f1 | cut -d: -f1)

    # Skip non-HTTPS and localhost
    [[ "$url" != https://* ]] && continue
    [[ "$host" == "localhost" || "$host" == "127.0.0.1" ]] && continue

    local expiry_date
    expiry_date=$(echo | openssl s_client -servername "$host" -connect "$host:443" 2>/dev/null | openssl x509 -noout -enddate 2>/dev/null | cut -d= -f2)

    if [ -n "$expiry_date" ]; then
      local expiry_epoch now_epoch days_left
      if [ "$OS" = "Darwin" ]; then
        expiry_epoch=$(date -j -f "%b %d %T %Y %Z" "$expiry_date" "+%s" 2>/dev/null || echo 0)
      else
        expiry_epoch=$(date -d "$expiry_date" "+%s" 2>/dev/null || echo 0)
      fi
      now_epoch=$(date "+%s")

      if [ "$expiry_epoch" -gt 0 ] 2>/dev/null; then
        days_left=$(( (expiry_epoch - now_epoch) / 86400 ))
        if [ "$days_left" -lt 0 ]; then
          add_finding "CRITICAL" "SSL certificate EXPIRED for $host" "$host" "Renew the SSL certificate immediately."
        elif [ "$days_left" -le "$SSL_CRIT_DAYS" ]; then
          add_finding "CRITICAL" "SSL certificate expires in $days_left days for $host" "$host" "Renew the SSL certificate urgently."
        elif [ "$days_left" -le "$SSL_WARN_DAYS" ]; then
          add_finding "MEDIUM" "SSL certificate expires in $days_left days for $host" "$host" "Plan SSL certificate renewal."
        fi
      fi
    fi
  done
}

# --- Check 5: Uncommitted Git Changes ---
check_git_status() {
  for dir in "${SCAN_DIRS[@]}"; do
    [ -d "$dir/.git" ] || continue

    local changes
    changes=$(git -C "$dir" status --porcelain 2>/dev/null | wc -l | tr -d ' ')

    if [ "$changes" -gt 0 ] 2>/dev/null; then
      local rel_dir="${dir#"$SKILL_DIR/"}"
      add_finding "MEDIUM" "Uncommitted changes detected ($changes files)" "$rel_dir" "Review and commit or stash your changes."
    fi
  done
}

# --- Check 6: System Memory ---
check_memory() {
  if [ "$OS" = "Darwin" ]; then
    # macOS: use vm_stat to check memory pressure
    local pages_free pages_speculative page_size
    page_size=$(sysctl -n hw.pagesize 2>/dev/null || echo 16384)
    pages_free=$(vm_stat 2>/dev/null | grep "Pages free" | awk '{print $3}' | tr -d '.')
    pages_speculative=$(vm_stat 2>/dev/null | grep "Pages speculative" | awk '{print $3}' | tr -d '.')

    if [ -n "$pages_free" ] 2>/dev/null; then
      local free_mb=$(( (pages_free + ${pages_speculative:-0}) * page_size / 1048576 ))
      if [ "$free_mb" -lt 512 ] 2>/dev/null; then
        add_finding "MEDIUM" "Low available memory (${free_mb}MB free)" "system" "Close unused applications or restart memory-heavy services."
      fi
    fi
  else
    # Linux: use free
    local avail_mb
    avail_mb=$(free -m 2>/dev/null | awk '/^Mem:/ {print $7}')
    if [ -n "$avail_mb" ] && [ "$avail_mb" -lt 512 ] 2>/dev/null; then
      add_finding "MEDIUM" "Low available memory (${avail_mb}MB available)" "system" "Check for memory leaks or reduce running services."
    fi
  fi
}

# --- Run All Checks ---
check_endpoints
check_services
check_disk
check_ssl
check_git_status
check_memory

# --- Calculate Score ---
SCORE=10
CRITICAL_COUNT=0
MEDIUM_COUNT=0

if $HAS_JQ; then
  CRITICAL_COUNT=$(echo "$FINDINGS" | jq '[.[] | select(.severity == "CRITICAL")] | length')
  MEDIUM_COUNT=$(echo "$FINDINGS" | jq '[.[] | select(.severity == "MEDIUM")] | length')
else
  CRITICAL_COUNT=$(echo "$FINDINGS" | grep -o '"CRITICAL"' | wc -l | tr -d ' ')
  MEDIUM_COUNT=$(echo "$FINDINGS" | grep -o '"MEDIUM"' | wc -l | tr -d ' ')
fi

SCORE=$(( SCORE - (CRITICAL_COUNT * 3) - MEDIUM_COUNT ))
[ "$SCORE" -lt 0 ] && SCORE=0

# --- Output JSON ---
if $HAS_JQ; then
  jq -n \
    --argjson score "$SCORE" \
    --argjson findings "$FINDINGS" \
    --argjson critical "$CRITICAL_COUNT" \
    --argjson medium "$MEDIUM_COUNT" \
    '{
      "council": "platform",
      "score": $score,
      "findings": $findings,
      "summary": {
        "critical": $critical,
        "medium": $medium,
        "total": ($critical + $medium)
      }
    }'
else
  echo "{\"council\":\"platform\",\"score\":$SCORE,\"findings\":$FINDINGS,\"summary\":{\"critical\":$CRITICAL_COUNT,\"medium\":$MEDIUM_COUNT,\"total\":$(( CRITICAL_COUNT + MEDIUM_COUNT ))}}"
fi
