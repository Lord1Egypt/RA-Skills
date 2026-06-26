#!/usr/bin/env bash
# PipelineLint -- License Validation Module
# Offline JWT-based license validation with 3 base64 decode fallbacks.
# Validates product claim, tier level, and expiry date.

set -euo pipefail

# --- Colors -------------------------------------------------------------------

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# --- Configuration ------------------------------------------------------------

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"
PIPELINELINT_LICENSE_KEY="${PIPELINELINT_LICENSE_KEY:-}"

# --- Tier Hierarchy -----------------------------------------------------------
# free=0, pro=1, team=2, enterprise=3
# Higher tier level grants access to more patterns and features.

declare -A TIER_LEVELS=(
  [free]=0
  [pro]=1
  [team]=2
  [enterprise]=3
)

# --- Key Retrieval ------------------------------------------------------------

# Retrieve the PipelineLint license key from environment variable or config file.
# Priority: ENV var > openclaw.json (python3 > node > jq fallbacks)
get_pipelinelint_key() {
  # 1. Check environment variable
  if [[ -n "$PIPELINELINT_LICENSE_KEY" ]]; then
    echo "$PIPELINELINT_LICENSE_KEY"
    return 0
  fi

  # 2. Check openclaw.json config file
  if [[ -f "$OPENCLAW_CONFIG" ]]; then
    local key=""

    # Try python3 first
    if command -v python3 &>/dev/null; then
      key=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    print(cfg.get('skills', {}).get('entries', {}).get('pipelinelint', {}).get('apiKey', ''))
except: pass
" 2>/dev/null)

    # Try node second
    elif command -v node &>/dev/null; then
      key=$(node -e "
try {
  const cfg = require('$OPENCLAW_CONFIG');
  console.log(cfg?.skills?.entries?.pipelinelint?.apiKey || '');
} catch(e) {}
" 2>/dev/null)

    # Try jq third
    elif command -v jq &>/dev/null; then
      key=$(jq -r '.skills.entries.pipelinelint.apiKey // ""' "$OPENCLAW_CONFIG" 2>/dev/null)
    fi

    if [[ -n "${key:-}" ]]; then
      echo "$key"
      return 0
    fi
  fi

  return 1
}

# --- JWT Decode ---------------------------------------------------------------

# Decode the payload (second segment) of a JWT token.
# Uses 3 fallback methods for base64 decoding:
#   1. base64 -d   (GNU/Linux coreutils)
#   2. base64 -D   (BSD/macOS)
#   3. openssl base64 -d  (universal fallback)
#
# Handles URL-safe base64 (tr '_-' '/+') and padding normalization.
decode_jwt_payload() {
  local token="$1"

  # Extract the second segment (payload) from the JWT
  local payload
  payload=$(echo "$token" | cut -d. -f2)

  # Normalize base64url padding
  local padded="$payload"
  local mod=$((${#payload} % 4))
  if [[ $mod -eq 2 ]]; then padded="${payload}=="; fi
  if [[ $mod -eq 3 ]]; then padded="${payload}="; fi

  # Convert URL-safe base64 to standard base64 and decode
  # Fallback 1: GNU base64 -d
  # Fallback 2: BSD base64 -D
  # Fallback 3: openssl base64 -d
  echo "$padded" | tr '_-' '/+' | base64 -d 2>/dev/null || \
  echo "$padded" | tr '_-' '/+' | base64 -D 2>/dev/null || \
  echo "$padded" | tr '_-' '/+' | openssl base64 -d 2>/dev/null || \
  return 1
}

# --- Field Extraction ---------------------------------------------------------

# Extract a single field from a JSON string.
# Uses python3 > node > jq > grep fallbacks.
extract_field() {
  local json="$1" field="$2"

  if command -v python3 &>/dev/null; then
    python3 -c "import json; print(json.loads('$json').get('$field', ''))" 2>/dev/null
  elif command -v node &>/dev/null; then
    node -e "console.log(JSON.parse('$json')['$field'] || '')" 2>/dev/null
  elif command -v jq &>/dev/null; then
    echo "$json" | jq -r ".$field // \"\"" 2>/dev/null
  else
    # Last resort: simple grep extraction
    echo "$json" | grep -oP "\"$field\"\s*:\s*\"?\K[^\",$}]+" 2>/dev/null || echo ""
  fi
}

# --- License Validation -------------------------------------------------------

# Validate a license key by decoding its JWT payload and checking the product
# field. Returns the decoded payload JSON on success.
validate_license() {
  local key="$1"
  local payload

  if ! payload=$(decode_jwt_payload "$key"); then
    return 1
  fi

  local product
  product=$(extract_field "$payload" "product")

  # Validate product matches pipelinelint
  if [[ "$product" != "pipelinelint" && -n "$product" ]]; then
    return 1
  fi

  echo "$payload"
  return 0
}

# --- Full License Check -------------------------------------------------------

# Perform a complete license check for a required tier.
# Validates: key presence, JWT decode, product match, tier level, expiry.
# Prints user-friendly error messages on failure.
check_pipelinelint_license() {
  local required_tier="${1:-pro}"
  local required_level="${TIER_LEVELS[$required_tier]:-1}"

  # Step 1: Retrieve the license key
  local key
  if ! key=$(get_pipelinelint_key) || [[ -z "$key" ]]; then
    echo -e "${RED}${BOLD}--- PipelineLint License Required ---${NC}"
    echo ""
    echo -e "This feature requires a ${BOLD}${required_tier}${NC} license."
    echo ""
    echo -e "Get your license at: ${CYAN}${BOLD}https://pipelinelint.pages.dev/pricing${NC}"
    echo ""
    echo "Then configure it:"
    echo -e "  ${DIM}# In ~/.openclaw/openclaw.json:${NC}"
    echo -e "  ${CYAN}\"skills\": { \"entries\": { \"pipelinelint\": { \"apiKey\": \"YOUR_KEY\" } } }${NC}"
    echo ""
    echo -e "  ${DIM}# Or set the environment variable:${NC}"
    echo -e "  ${CYAN}export PIPELINELINT_LICENSE_KEY=\"YOUR_KEY\"${NC}"
    return 1
  fi

  # Step 2: Decode JWT payload
  local payload
  if ! payload=$(decode_jwt_payload "$key"); then
    echo -e "${RED}[PipelineLint]${NC} Invalid license key format."
    echo -e "Get a valid license at: ${CYAN}https://pipelinelint.pages.dev/pricing${NC}"
    return 1
  fi

  # Step 3: Extract and validate fields
  local product tier expiry
  product=$(extract_field "$payload" "product")
  tier=$(extract_field "$payload" "tier")
  expiry=$(extract_field "$payload" "exp")

  # Step 4: Validate product
  if [[ -n "$product" && "$product" != "pipelinelint" ]]; then
    echo -e "${RED}[PipelineLint]${NC} License is for product '${BOLD}$product${NC}', not pipelinelint."
    echo -e "Get a PipelineLint license at: ${CYAN}https://pipelinelint.pages.dev/pricing${NC}"
    return 1
  fi

  # Step 5: Validate tier level
  local actual_level="${TIER_LEVELS[$tier]:-0}"
  if [[ "$actual_level" -lt "$required_level" ]]; then
    echo -e "${RED}[PipelineLint]${NC} This feature requires ${BOLD}$required_tier${NC} tier. You have: ${BOLD}$tier${NC}"
    echo -e "Upgrade at: ${CYAN}https://pipelinelint.pages.dev/upgrade${NC}"
    return 1
  fi

  # Step 6: Check expiry
  if [[ -n "$expiry" ]]; then
    local now
    now=$(date +%s)
    if [[ "$now" -gt "$expiry" ]]; then
      echo -e "${RED}[PipelineLint]${NC} License expired. Renew at: ${CYAN}https://pipelinelint.pages.dev/renew${NC}"
      return 1
    fi
  fi

  return 0
}

# --- Tier Detection -----------------------------------------------------------

# Get the current tier from the license key.
# Returns "free" if no valid key is found.
get_pipelinelint_tier() {
  local key
  if ! key=$(get_pipelinelint_key) || [[ -z "$key" ]]; then
    echo "free"
    return 0
  fi

  local payload
  if ! payload=$(decode_jwt_payload "$key" 2>/dev/null); then
    echo "free"
    return 0
  fi

  local tier
  tier=$(extract_field "$payload" "tier")
  echo "${tier:-free}"
}

# --- Tier Level Lookup --------------------------------------------------------

# Convert a tier name to its numeric level for comparison.
get_tier_level() {
  local tier="${1:-free}"
  echo "${TIER_LEVELS[$tier]:-0}"
}

# --- Status Display -----------------------------------------------------------

# Display license status information to the user.
show_pipelinelint_status() {
  local key
  if ! key=$(get_pipelinelint_key) || [[ -z "$key" ]]; then
    echo -e "License: ${YELLOW}Free tier${NC}"
    echo -e "  Patterns: 30 (SE, CF categories)"
    echo -e "  Upgrade at: ${CYAN}https://pipelinelint.pages.dev/pricing${NC}"
    return
  fi

  local payload tier expiry seats product
  payload=$(decode_jwt_payload "$key" 2>/dev/null) || {
    echo -e "License: ${RED}Invalid key${NC}"
    return
  }
  product=$(extract_field "$payload" "product")
  tier=$(extract_field "$payload" "tier")
  expiry=$(extract_field "$payload" "exp")
  seats=$(extract_field "$payload" "seats")

  # Validate product
  if [[ -n "$product" && "$product" != "pipelinelint" ]]; then
    echo -e "License: ${RED}Wrong product ($product)${NC}"
    echo -e "  This key is for $product, not PipelineLint."
    echo -e "  Get a PipelineLint license at: ${CYAN}https://pipelinelint.pages.dev/pricing${NC}"
    return
  fi

  # Determine status
  local now status_color status_text
  now=$(date +%s)
  status_color="$GREEN"; status_text="Active"
  if [[ -n "$expiry" && "$now" -gt "$expiry" ]]; then
    status_color="$RED"; status_text="Expired"
  fi

  # Format expiry date
  local expiry_date="Never"
  if [[ -n "$expiry" ]]; then
    expiry_date=$(date -d "@$expiry" +%Y-%m-%d 2>/dev/null || \
                  date -r "$expiry" +%Y-%m-%d 2>/dev/null || \
                  echo "unknown")
  fi

  echo -e "License: ${status_color}${BOLD}${tier^^}${NC} (${status_color}${status_text}${NC})"
  echo -e "  Product: pipelinelint"
  echo -e "  Seats: ${seats:-unlimited}"
  echo -e "  Expires: $expiry_date"
  echo ""

  case "$tier" in
    pro)
      echo -e "  Patterns: 60 (SE, CF, TS, AR categories)"
      echo -e "  Formats: text, json, html"
      echo -e "  Upgrade to Team for: DP, EN categories + full 90 patterns"
      ;;
    team)
      echo -e "  Patterns: 90 (all 6 categories)"
      echo -e "  Formats: text, json, html"
      echo -e "  All features available"
      ;;
    enterprise)
      echo -e "  Patterns: 90 (all 6 categories)"
      echo -e "  Formats: text, json, html"
      echo -e "  All features + priority support"
      ;;
  esac
}
