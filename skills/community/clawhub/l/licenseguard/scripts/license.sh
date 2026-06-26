#!/usr/bin/env bash
# LicenseGuard -- License Validation Module
# Same JWT-based offline validation as other ClawHub skills

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"
LICENSEGUARD_LICENSE_KEY="${LICENSEGUARD_LICENSE_KEY:-}"

declare -A TIER_LEVELS=(
  [free]=0
  [pro]=1
  [team]=2
  [enterprise]=3
)

get_licenseguard_key() {
  if [[ -n "$LICENSEGUARD_LICENSE_KEY" ]]; then
    echo "$LICENSEGUARD_LICENSE_KEY"
    return 0
  fi

  if [[ -f "$OPENCLAW_CONFIG" ]]; then
    local key=""
    if command -v python3 &>/dev/null; then
      key=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    print(cfg.get('skills', {}).get('entries', {}).get('licenseguard', {}).get('apiKey', ''))
except: pass
" 2>/dev/null)
    elif command -v node &>/dev/null; then
      key=$(node -e "
try {
  const cfg = require('$OPENCLAW_CONFIG');
  console.log(cfg?.skills?.entries?.licenseguard?.apiKey || '');
} catch(e) {}
" 2>/dev/null)
    elif command -v jq &>/dev/null; then
      key=$(jq -r '.skills.entries.licenseguard.apiKey // ""' "$OPENCLAW_CONFIG" 2>/dev/null)
    fi

    if [[ -n "${key:-}" ]]; then
      echo "$key"
      return 0
    fi
  fi
  return 1
}

decode_jwt_payload() {
  local token="$1"
  local payload
  payload=$(echo "$token" | cut -d. -f2)
  local padded="$payload"
  local mod=$((${#payload} % 4))
  if [[ $mod -eq 2 ]]; then padded="${payload}=="; fi
  if [[ $mod -eq 3 ]]; then padded="${payload}="; fi
  echo "$padded" | tr '_-' '/+' | base64 -d 2>/dev/null || \
  echo "$padded" | tr '_-' '/+' | base64 -D 2>/dev/null || \
  echo "$padded" | tr '_-' '/+' | openssl base64 -d 2>/dev/null || \
  return 1
}

extract_field() {
  local json="$1" field="$2"
  if command -v python3 &>/dev/null; then
    python3 -c "import json; print(json.loads('$json').get('$field', ''))" 2>/dev/null
  elif command -v node &>/dev/null; then
    node -e "console.log(JSON.parse('$json')['$field'] || '')" 2>/dev/null
  elif command -v jq &>/dev/null; then
    echo "$json" | jq -r ".$field // \"\"" 2>/dev/null
  else
    echo "$json" | grep -oP "\"$field\"\s*:\s*\"?\K[^\",$}]+" 2>/dev/null || echo ""
  fi
}

validate_license() {
  local key="$1"

  # Decode the JWT payload
  local payload
  if ! payload=$(decode_jwt_payload "$key"); then
    return 1
  fi

  # Check product field matches licenseguard
  local product
  product=$(extract_field "$payload" "product")
  if [[ "$product" != "licenseguard" && -n "$product" ]]; then
    return 1
  fi

  # Check expiry
  local expiry
  expiry=$(extract_field "$payload" "exp")
  if [[ -n "$expiry" ]]; then
    local now
    now=$(date +%s)
    if [[ "$now" -gt "$expiry" ]]; then
      return 1
    fi
  fi

  return 0
}

check_licenseguard_license() {
  local required_tier="${1:-pro}"
  local required_level="${TIER_LEVELS[$required_tier]:-1}"

  local key
  if ! key=$(get_licenseguard_key) || [[ -z "$key" ]]; then
    echo -e "${RED}${BOLD}--- LicenseGuard License Required ---${NC}"
    echo ""
    echo -e "This feature requires a ${BOLD}${required_tier}${NC} license."
    echo ""
    echo -e "Get your license at: ${CYAN}${BOLD}https://licenseguard.pages.dev/pricing${NC}"
    echo ""
    echo "Then configure it:"
    echo -e "  ${DIM}# In ~/.openclaw/openclaw.json:${NC}"
    echo -e "  ${CYAN}\"skills\": { \"entries\": { \"licenseguard\": { \"apiKey\": \"YOUR_KEY\" } } }${NC}"
    echo ""
    echo -e "  ${DIM}# Or set the environment variable:${NC}"
    echo -e "  ${CYAN}export LICENSEGUARD_LICENSE_KEY=\"YOUR_KEY\"${NC}"
    return 1
  fi

  local payload
  if ! payload=$(decode_jwt_payload "$key"); then
    echo -e "${RED}[LicenseGuard]${NC} Invalid license key."
    echo -e "Get a valid license at: ${CYAN}https://licenseguard.pages.dev/pricing${NC}"
    return 1
  fi

  # Validate product field
  local product
  product=$(extract_field "$payload" "product")
  if [[ -n "$product" && "$product" != "licenseguard" ]]; then
    echo -e "${RED}[LicenseGuard]${NC} License key is for a different product: ${BOLD}$product${NC}"
    echo -e "Get a LicenseGuard license at: ${CYAN}https://licenseguard.pages.dev/pricing${NC}"
    return 1
  fi

  local tier expiry
  tier=$(extract_field "$payload" "tier")
  expiry=$(extract_field "$payload" "exp")

  local actual_level="${TIER_LEVELS[$tier]:-0}"
  if [[ "$actual_level" -lt "$required_level" ]]; then
    echo -e "${RED}[LicenseGuard]${NC} This feature requires ${BOLD}$required_tier${NC} tier. You have: ${BOLD}$tier${NC}"
    echo -e "Upgrade at: ${CYAN}https://licenseguard.pages.dev/upgrade${NC}"
    return 1
  fi

  if [[ -n "$expiry" ]]; then
    local now
    now=$(date +%s)
    if [[ "$now" -gt "$expiry" ]]; then
      echo -e "${RED}[LicenseGuard]${NC} License expired. Renew at: ${CYAN}https://licenseguard.pages.dev/renew${NC}"
      return 1
    fi
  fi

  return 0
}

get_licenseguard_tier() {
  local key
  if ! key=$(get_licenseguard_key) || [[ -z "$key" ]]; then
    echo "free"
    return 0
  fi

  local payload
  if ! payload=$(decode_jwt_payload "$key" 2>/dev/null); then
    echo "free"
    return 0
  fi

  local product
  product=$(extract_field "$payload" "product")
  if [[ -n "$product" && "$product" != "licenseguard" ]]; then
    echo "free"
    return 0
  fi

  local expiry
  expiry=$(extract_field "$payload" "exp")
  if [[ -n "$expiry" ]]; then
    local now
    now=$(date +%s)
    if [[ "$now" -gt "$expiry" ]]; then
      echo "free"
      return 0
    fi
  fi

  local tier
  tier=$(extract_field "$payload" "tier")
  echo "${tier:-free}"
}

show_licenseguard_status() {
  local key
  if ! key=$(get_licenseguard_key) || [[ -z "$key" ]]; then
    echo -e "License: ${YELLOW}Free tier${NC}"
    echo -e "  Available: scan (5 file limit)"
    echo -e "  Upgrade at: ${CYAN}https://licenseguard.pages.dev/pricing${NC}"
    return
  fi

  local payload tier expiry seats
  payload=$(decode_jwt_payload "$key" 2>/dev/null) || { echo -e "License: ${RED}Invalid key${NC}"; return; }

  # Validate product
  local product
  product=$(extract_field "$payload" "product")
  if [[ -n "$product" && "$product" != "licenseguard" ]]; then
    echo -e "License: ${RED}Wrong product key ($product)${NC}"
    echo -e "  Get a LicenseGuard license at: ${CYAN}https://licenseguard.pages.dev/pricing${NC}"
    return
  fi

  tier=$(extract_field "$payload" "tier")
  expiry=$(extract_field "$payload" "exp")
  seats=$(extract_field "$payload" "seats")

  local now status_color status_text
  now=$(date +%s)
  status_color="$GREEN"; status_text="Active"
  if [[ -n "$expiry" && "$now" -gt "$expiry" ]]; then
    status_color="$RED"; status_text="Expired"
  fi

  local expiry_date="Never"
  [[ -n "$expiry" ]] && expiry_date=$(date -d "@$expiry" +%Y-%m-%d 2>/dev/null || date -r "$expiry" +%Y-%m-%d 2>/dev/null || echo "unknown")

  echo -e "License: ${status_color}${BOLD}${tier^^}${NC} (${status_color}${status_text}${NC})"
  echo -e "  Product: licenseguard"
  echo -e "  Seats: ${seats:-unlimited}"
  echo -e "  Expires: $expiry_date"
  echo ""

  case "$tier" in
    pro)
      echo -e "  Available: scan (unlimited), hooks, report, matrix"
      echo -e "  Upgrade to Team for: policy, sbom"
      ;;
    team)
      echo -e "  Available: scan, hooks, report, matrix, policy, sbom"
      ;;
    enterprise)
      echo -e "  Available: All features + priority support"
      ;;
  esac
}
