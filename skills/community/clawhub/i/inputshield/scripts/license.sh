#!/usr/bin/env bash
# InputShield -- License Validation Module
# JWT-based offline validation with 3 fallback decode methods.
# Same pattern as SecretScan/ConfigSafe/DocSync/DepGuard/EnvGuard.
#
# Tier hierarchy:
#   free=0, pro=1, team=2, enterprise=3
#
# The JWT payload must contain:
#   product: "inputshield"
#   tier: "free"|"pro"|"team"|"enterprise"
#   exp: unix timestamp (optional, checked if present)
#   seats: number (optional, informational)

set -euo pipefail

# ---------------------------------------------------------------------------
# Colors (safe to re-declare; sourcing scripts may set these)
# ---------------------------------------------------------------------------

RED="${RED:-\033[0;31m}"
GREEN="${GREEN:-\033[0;32m}"
YELLOW="${YELLOW:-\033[1;33m}"
BLUE="${BLUE:-\033[0;34m}"
CYAN="${CYAN:-\033[0;36m}"
MAGENTA="${MAGENTA:-\033[0;35m}"
BOLD="${BOLD:-\033[1m}"
DIM="${DIM:-\033[2m}"
NC="${NC:-\033[0m}"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"
INPUTSHIELD_LICENSE_KEY="${INPUTSHIELD_LICENSE_KEY:-}"

# Tier hierarchy: free=0, pro=1, team=2, enterprise=3
declare -A TIER_LEVELS=(
  [free]=0
  [pro]=1
  [team]=2
  [enterprise]=3
)

# ---------------------------------------------------------------------------
# Key Retrieval
# ---------------------------------------------------------------------------

# Retrieve the InputShield license key from env var or openclaw.json config.
# Returns the key on stdout; returns 1 if not found.
get_inputshield_key() {
  # Priority 1: environment variable
  if [[ -n "$INPUTSHIELD_LICENSE_KEY" ]]; then
    echo "$INPUTSHIELD_LICENSE_KEY"
    return 0
  fi

  # Priority 2: openclaw.json config file
  if [[ -f "$OPENCLAW_CONFIG" ]]; then
    local key=""

    # Try python3 first
    if command -v python3 &>/dev/null; then
      key=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    print(cfg.get('skills', {}).get('entries', {}).get('inputshield', {}).get('apiKey', ''))
except: pass
" 2>/dev/null)

    # Fallback to node
    elif command -v node &>/dev/null; then
      key=$(node -e "
try {
  const fs = require('fs');
  const cfg = JSON.parse(fs.readFileSync('$OPENCLAW_CONFIG', 'utf8'));
  console.log(cfg?.skills?.entries?.inputshield?.apiKey || '');
} catch(e) {}
" 2>/dev/null)

    # Fallback to jq
    elif command -v jq &>/dev/null; then
      key=$(jq -r '.skills.entries.inputshield.apiKey // ""' "$OPENCLAW_CONFIG" 2>/dev/null)
    fi

    if [[ -n "${key:-}" ]]; then
      echo "$key"
      return 0
    fi
  fi

  return 1
}

# ---------------------------------------------------------------------------
# JWT Decode -- 3 Fallback Methods
# ---------------------------------------------------------------------------

# Decode the payload portion of a JWT token (the middle segment between dots).
# Uses 3 fallback methods:
#   1. base64 -d (Linux / GNU coreutils)
#   2. base64 -D (macOS / BSD)
#   3. openssl base64 -d (universal fallback)
#
# Handles URL-safe base64 (replaces -_ with +/) and adds padding as needed.
decode_jwt_payload() {
  local token="$1"

  # --- JWT Structure Validation ---
  # A valid JWT must have exactly 3 dot-separated parts: header.payload.signature
  local dot_count
  dot_count=$(echo "$token" | tr -cd '.' | wc -c)
  if [[ "$dot_count" -ne 2 ]]; then
    echo "[JWT] Malformed token: expected 3 parts (header.payload.signature), got $((dot_count + 1))" >&2
    return 1
  fi

  local header payload signature
  header=$(echo "$token" | cut -d. -f1)
  payload=$(echo "$token" | cut -d. -f2)
  signature=$(echo "$token" | cut -d. -f3)

  # Signature must be non-empty
  if [[ -z "$signature" ]]; then
    echo "[JWT] Rejected: signature segment is empty (unsigned token)" >&2
    return 1
  fi

  # --- Signature Verification (HMAC-SHA256 via openssl, if available) ---
  # NOTE: Full cryptographic verification requires the shared secret. When
  # CLAWHUB_JWT_SECRET is set, we verify the HMAC-SHA256 signature. Without
  # the secret, we still enforce structural integrity (3-part, non-empty sig)
  # which blocks trivially forged tokens (e.g., alg:none attacks).
  if [[ -n "${CLAWHUB_JWT_SECRET:-}" ]] && command -v openssl &>/dev/null; then
    local signing_input="${header}.${payload}"
    local expected_sig
    expected_sig=$(printf '%s' "$signing_input" \
      | openssl dgst -sha256 -hmac "$CLAWHUB_JWT_SECRET" -binary 2>/dev/null \
      | openssl base64 -e 2>/dev/null \
      | tr '/+' '_-' | tr -d '=')
    if [[ "$expected_sig" != "$signature" ]]; then
      echo "[JWT] Signature verification failed" >&2
      return 1
    fi
  fi

  # --- Decode Payload ---
  local padded="$payload"
  local mod=$((${#payload} % 4))
  if [[ $mod -eq 2 ]]; then padded="${payload}=="; fi
  if [[ $mod -eq 3 ]]; then padded="${payload}="; fi

  local decoded
  decoded=$(echo "$padded" | tr '_-' '/+' | base64 -d 2>/dev/null || \
            echo "$padded" | tr '_-' '/+' | base64 -D 2>/dev/null || \
            echo "$padded" | tr '_-' '/+' | openssl base64 -d 2>/dev/null) || {
    echo "[JWT] Failed to decode payload" >&2
    return 1
  }

  # --- Expiry Check ---
  # Check exp claim inline to catch expired tokens at decode time
  local exp_val=""
  if command -v python3 &>/dev/null; then
    exp_val=$(python3 -c "import json; print(json.loads('$decoded').get('exp', ''))" 2>/dev/null || true)
  elif command -v node &>/dev/null; then
    exp_val=$(node -e "console.log(JSON.parse('$decoded').exp || '')" 2>/dev/null || true)
  elif command -v jq &>/dev/null; then
    exp_val=$(echo "$decoded" | jq -r '.exp // ""' 2>/dev/null || true)
  fi

  if [[ -n "$exp_val" && "$exp_val" != "null" ]]; then
    local now
    now=$(date +%s)
    if [[ "$now" -gt "$exp_val" ]]; then
      echo "[JWT] Token expired (exp=$exp_val, now=$now)" >&2
      return 1
    fi
  fi

  echo "$decoded"
}

# ---------------------------------------------------------------------------
# JSON Field Extraction
# ---------------------------------------------------------------------------

# Extract a field value from a JSON string.
# Uses python3 -> node -> jq -> grep as fallbacks.
extract_field() {
  local json="$1" field="$2"

  if command -v python3 &>/dev/null; then
    python3 -c "
import json, sys
try:
    data = json.loads(sys.argv[1])
    val = data.get(sys.argv[2], '')
    print(val if val is not None else '')
except: pass
" "$json" "$field" 2>/dev/null
  elif command -v node &>/dev/null; then
    node -e "
try {
  const data = JSON.parse(process.argv[1]);
  console.log(data[process.argv[2]] || '');
} catch(e) {}
" "$json" "$field" 2>/dev/null
  elif command -v jq &>/dev/null; then
    echo "$json" | jq -r ".$field // \"\"" 2>/dev/null
  else
    # Regex fallback -- works for simple string/number values
    echo "$json" | grep -oP "\"$field\"\s*:\s*\"?\K[^\",$}]+" 2>/dev/null || echo ""
  fi
}

# ---------------------------------------------------------------------------
# License Validation
# ---------------------------------------------------------------------------

# Validate the license key by decoding its JWT payload and checking
# that the product field matches "inputshield".
# Returns the payload JSON on stdout, or returns 1 on failure.
validate_license() {
  local key="$1"
  local payload

  if ! payload=$(decode_jwt_payload "$key"); then
    return 1
  fi

  local product
  product=$(extract_field "$payload" "product")

  # Validate product matches "inputshield"
  if [[ -n "$product" && "$product" != "inputshield" ]]; then
    return 1
  fi

  echo "$payload"
  return 0
}

# ---------------------------------------------------------------------------
# License Check (main entry point for requiring a license)
# ---------------------------------------------------------------------------

# check_inputshield_license <required_tier>
#
# Verifies the user holds a valid InputShield license at or above
# the required tier. Prints user-friendly error messages on failure.
# Returns 0 on success, 1 on failure.
check_inputshield_license() {
  local required_tier="${1:-pro}"
  local required_level="${TIER_LEVELS[$required_tier]:-1}"

  # Retrieve the license key
  local key
  if ! key=$(get_inputshield_key) || [[ -z "$key" ]]; then
    echo -e "${RED}${BOLD}--- InputShield License Required ---${NC}"
    echo ""
    echo -e "This feature requires a ${BOLD}${required_tier}${NC} license."
    echo ""
    echo -e "Get your license at: ${CYAN}${BOLD}https://inputshield.pages.dev/pricing${NC}"
    echo ""
    echo "Then configure it:"
    echo -e "  ${DIM}# In ~/.openclaw/openclaw.json:${NC}"
    echo -e "  ${CYAN}\"skills\": { \"entries\": { \"inputshield\": { \"apiKey\": \"YOUR_KEY\" } } }${NC}"
    echo ""
    echo -e "  ${DIM}# Or set the environment variable:${NC}"
    echo -e "  ${CYAN}export INPUTSHIELD_LICENSE_KEY=\"YOUR_KEY\"${NC}"
    return 1
  fi

  # Decode the JWT payload
  local payload
  if ! payload=$(decode_jwt_payload "$key"); then
    echo -e "${RED}[InputShield]${NC} Invalid license key -- could not decode JWT payload."
    echo -e "Get a valid license at: ${CYAN}https://inputshield.pages.dev/pricing${NC}"
    return 1
  fi

  # Extract and validate fields
  local product tier expiry
  product=$(extract_field "$payload" "product")
  tier=$(extract_field "$payload" "tier")
  expiry=$(extract_field "$payload" "exp")

  # Validate product
  if [[ -n "$product" && "$product" != "inputshield" ]]; then
    echo -e "${RED}[InputShield]${NC} License is for product '${BOLD}$product${NC}', not inputshield."
    echo -e "Get an InputShield license at: ${CYAN}https://inputshield.pages.dev/pricing${NC}"
    return 1
  fi

  # Validate tier hierarchy
  local actual_level="${TIER_LEVELS[$tier]:-0}"
  if [[ "$actual_level" -lt "$required_level" ]]; then
    echo -e "${RED}[InputShield]${NC} This feature requires ${BOLD}$required_tier${NC} tier. You have: ${BOLD}$tier${NC}"
    echo -e "Upgrade at: ${CYAN}https://inputshield.pages.dev/upgrade${NC}"
    return 1
  fi

  # Check expiry
  if [[ -n "$expiry" ]]; then
    local now
    now=$(date +%s)
    if [[ "$now" -gt "$expiry" ]]; then
      echo -e "${RED}[InputShield]${NC} License expired."
      echo -e "Renew at: ${CYAN}https://inputshield.pages.dev/renew${NC}"
      return 1
    fi
  fi

  return 0
}

# ---------------------------------------------------------------------------
# Tier Detection
# ---------------------------------------------------------------------------

# Get the current license tier. Returns "free" if no valid license found.
get_inputshield_tier() {
  local key
  if ! key=$(get_inputshield_key) || [[ -z "$key" ]]; then
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
  if [[ -n "$product" && "$product" != "inputshield" ]]; then
    echo "free"
    return 0
  fi

  local tier
  tier=$(extract_field "$payload" "tier")
  echo "${tier:-free}"
}

# ---------------------------------------------------------------------------
# Pattern Limit by Tier
# ---------------------------------------------------------------------------

# Get the number of patterns available per category for the given tier.
# free=5, pro=10, team/enterprise=15
get_patterns_per_category() {
  local tier="${1:-free}"
  case "$tier" in
    free)       echo 5 ;;
    pro)        echo 10 ;;
    team)       echo 15 ;;
    enterprise) echo 15 ;;
    *)          echo 5 ;;
  esac
}

# Get the total number of patterns available for the given tier.
# free=30, pro=60, team/enterprise=90
get_total_patterns() {
  local tier="${1:-free}"
  case "$tier" in
    free)       echo 30 ;;
    pro)        echo 60 ;;
    team)       echo 90 ;;
    enterprise) echo 90 ;;
    *)          echo 30 ;;
  esac
}

# ---------------------------------------------------------------------------
# Status Display
# ---------------------------------------------------------------------------

# Display the current license status, tier info, and available features.
show_inputshield_status() {
  local key
  if ! key=$(get_inputshield_key) || [[ -z "$key" ]]; then
    echo -e "License: ${YELLOW}Free tier${NC}"
    echo -e "  Patterns: 30 of 90 (5 per category)"
    echo -e "  Available: scan (basic)"
    echo -e "  Upgrade at: ${CYAN}https://inputshield.pages.dev/pricing${NC}"
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
  if [[ -n "$product" && "$product" != "inputshield" ]]; then
    echo -e "License: ${RED}Wrong product ($product)${NC}"
    echo -e "  This key is for $product, not InputShield."
    echo -e "  Get an InputShield license at: ${CYAN}https://inputshield.pages.dev/pricing${NC}"
    return
  fi

  local now status_color status_text
  now=$(date +%s)
  status_color="$GREEN"; status_text="Active"
  if [[ -n "$expiry" && "$now" -gt "$expiry" ]]; then
    status_color="$RED"; status_text="Expired"
  fi

  local expiry_date="Never"
  if [[ -n "$expiry" ]]; then
    expiry_date=$(date -d "@$expiry" +%Y-%m-%d 2>/dev/null || \
                  date -r "$expiry" +%Y-%m-%d 2>/dev/null || \
                  echo "unknown")
  fi

  local total_patterns
  total_patterns=$(get_total_patterns "$tier")
  local per_category
  per_category=$(get_patterns_per_category "$tier")

  echo -e "License: ${status_color}${BOLD}${tier^^}${NC} (${status_color}${status_text}${NC})"
  echo -e "  Product: inputshield"
  echo -e "  Seats: ${seats:-unlimited}"
  echo -e "  Expires: $expiry_date"
  echo -e "  Patterns: $total_patterns of 90 ($per_category per category)"
  echo ""

  case "$tier" in
    pro)
      echo -e "  Available: scan (60 patterns), hooks, report"
      echo -e "  Upgrade to Team for: audit, category filtering, JSON/HTML output"
      ;;
    team)
      echo -e "  Available: scan (90 patterns), hooks, report, audit, category filtering, all output formats"
      ;;
    enterprise)
      echo -e "  Available: All features + priority support"
      ;;
    *)
      echo -e "  Available: scan (30 patterns)"
      echo -e "  Upgrade at: ${CYAN}https://inputshield.pages.dev/pricing${NC}"
      ;;
  esac
}
