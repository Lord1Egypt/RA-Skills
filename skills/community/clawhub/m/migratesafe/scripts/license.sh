#!/usr/bin/env bash
# MigrateSafe -- License Validation Module
# JWT-based offline validation (same pattern as EnvGuard/DocSync/DepGuard)
#
# Validates: expiry, issuer, product, tier level
# Reads from: MIGRATESAFE_LICENSE_KEY env var or ~/.openclaw/openclaw.json

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
MIGRATESAFE_LICENSE_KEY="${MIGRATESAFE_LICENSE_KEY:-}"

# Tier hierarchy: free < pro < team < enterprise
declare -A TIER_LEVELS=(
  [free]=0
  [pro]=1
  [team]=2
  [enterprise]=3
)

# ─── Key Retrieval ───────────────────────────────────────────────────────────

# Retrieve the license key from env var or openclaw config file.
get_migratesafe_key() {
  # 1. Environment variable takes priority
  if [[ -n "$MIGRATESAFE_LICENSE_KEY" ]]; then
    echo "$MIGRATESAFE_LICENSE_KEY"
    return 0
  fi

  # 2. Read from openclaw.json config
  if [[ -f "$OPENCLAW_CONFIG" ]]; then
    local key=""
    if command -v python3 &>/dev/null; then
      key=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    print(cfg.get('skills', {}).get('entries', {}).get('migratesafe', {}).get('apiKey', ''))
except: pass
" 2>/dev/null)
    elif command -v node &>/dev/null; then
      key=$(node -e "
try {
  const cfg = require('$OPENCLAW_CONFIG');
  console.log(cfg?.skills?.entries?.migratesafe?.apiKey || '');
} catch(e) {}
" 2>/dev/null)
    elif command -v jq &>/dev/null; then
      key=$(jq -r '.skills.entries.migratesafe.apiKey // ""' "$OPENCLAW_CONFIG" 2>/dev/null)
    fi

    if [[ -n "${key:-}" ]]; then
      echo "$key"
      return 0
    fi
  fi

  return 1
}

# ─── JWT Decode ──────────────────────────────────────────────────────────────

# Decode the payload (second part) of a JWT token.
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

# ─── JSON Field Extraction ───────────────────────────────────────────────────

# Extract a field from a JSON string using available tooling.
extract_field() {
  local json="$1" field="$2"

  if command -v python3 &>/dev/null; then
    python3 -c "import json; print(json.loads('$json').get('$field', ''))" 2>/dev/null
  elif command -v node &>/dev/null; then
    node -e "console.log(JSON.parse('$json')['$field'] || '')" 2>/dev/null
  elif command -v jq &>/dev/null; then
    echo "$json" | jq -r ".$field // \"\"" 2>/dev/null
  else
    # Fallback: basic regex extraction
    echo "$json" | grep -oP "\"$field\"\s*:\s*\"?\K[^\",$}]+" 2>/dev/null || echo ""
  fi
}

# ─── License Validation ─────────────────────────────────────────────────────

# Full license validation with tier checking.
# Usage: check_migratesafe_license <required_tier>
# Returns 0 if valid and tier sufficient, 1 otherwise.
check_migratesafe_license() {
  local required_tier="${1:-pro}"
  local required_level="${TIER_LEVELS[$required_tier]:-1}"

  # Get the key
  local key
  if ! key=$(get_migratesafe_key) || [[ -z "$key" ]]; then
    echo -e "${RED}${BOLD}━━━ MigrateSafe License Required ━━━${NC}"
    echo ""
    echo -e "This feature requires a ${BOLD}${required_tier}${NC} license."
    echo ""
    echo -e "Get your license at: ${CYAN}${BOLD}https://migratesafe.pages.dev/pricing${NC}"
    echo ""
    echo "Then configure it:"
    echo -e "  ${DIM}# In ~/.openclaw/openclaw.json:${NC}"
    echo -e "  ${CYAN}\"skills\": { \"entries\": { \"migratesafe\": { \"apiKey\": \"YOUR_KEY\" } } }${NC}"
    echo ""
    echo -e "  ${DIM}# Or set the environment variable:${NC}"
    echo -e "  ${CYAN}export MIGRATESAFE_LICENSE_KEY=\"YOUR_KEY\"${NC}"
    return 1
  fi

  # Decode the JWT payload
  local payload
  if ! payload=$(decode_jwt_payload "$key"); then
    echo -e "${RED}[MigrateSafe]${NC} Invalid license key format."
    echo -e "Get a valid license at: ${CYAN}https://migratesafe.pages.dev/pricing${NC}"
    return 1
  fi

  # Validate issuer
  local iss
  iss=$(extract_field "$payload" "iss")
  if [[ "$iss" != "license-api" ]]; then
    echo -e "${RED}[MigrateSafe]${NC} Invalid license issuer."
    echo -e "Get a valid license at: ${CYAN}https://migratesafe.pages.dev/pricing${NC}"
    return 1
  fi

  # Validate product
  local product
  product=$(extract_field "$payload" "product")
  if [[ "$product" != "migratesafe" ]]; then
    echo -e "${RED}[MigrateSafe]${NC} License is for a different product: ${BOLD}$product${NC}"
    echo -e "Get a MigrateSafe license at: ${CYAN}https://migratesafe.pages.dev/pricing${NC}"
    return 1
  fi

  # Check tier
  local tier
  tier=$(extract_field "$payload" "tier")
  local actual_level="${TIER_LEVELS[$tier]:-0}"
  if [[ "$actual_level" -lt "$required_level" ]]; then
    echo -e "${RED}[MigrateSafe]${NC} This feature requires ${BOLD}$required_tier${NC} tier. You have: ${BOLD}$tier${NC}"
    echo -e "Upgrade at: ${CYAN}https://migratesafe.pages.dev/upgrade${NC}"
    return 1
  fi

  # Check expiry
  local expiry
  expiry=$(extract_field "$payload" "exp")
  if [[ -n "$expiry" ]]; then
    local now
    now=$(date +%s)
    if [[ "$now" -gt "$expiry" ]]; then
      echo -e "${RED}[MigrateSafe]${NC} License expired."
      echo -e "Renew at: ${CYAN}https://migratesafe.pages.dev/renew${NC}"
      return 1
    fi
  fi

  return 0
}

# ─── Tier Retrieval ──────────────────────────────────────────────────────────

# Get the current tier from the license key. Returns "free" if no valid key.
get_migratesafe_tier() {
  local key
  if ! key=$(get_migratesafe_key) || [[ -z "$key" ]]; then
    echo "free"
    return 0
  fi

  local payload
  if ! payload=$(decode_jwt_payload "$key"); then
    echo "free"
    return 0
  fi

  # Validate basics before trusting the tier
  local iss product
  iss=$(extract_field "$payload" "iss")
  product=$(extract_field "$payload" "product")

  if [[ "$iss" != "license-api" || "$product" != "migratesafe" ]]; then
    echo "free"
    return 0
  fi

  # Check expiry
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

# ─── Status Display ─────────────────────────────────────────────────────────

# Show license status information.
show_migratesafe_status() {
  local key
  if ! key=$(get_migratesafe_key) || [[ -z "$key" ]]; then
    echo -e "License: ${YELLOW}Free tier${NC}"
    echo -e "  Available: scan (up to 3 files)"
    echo -e "  Upgrade at: ${CYAN}https://migratesafe.pages.dev/pricing${NC}"
    return
  fi

  local payload tier expiry seats
  payload=$(decode_jwt_payload "$key" 2>/dev/null) || { echo -e "License: ${RED}Invalid key${NC}"; return; }
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
  if [[ -n "$expiry" ]]; then
    expiry_date=$(date -d "@$expiry" +%Y-%m-%d 2>/dev/null || date -r "$expiry" +%Y-%m-%d 2>/dev/null || echo "unknown")
  fi

  echo -e "License: ${status_color}${BOLD}${tier^^}${NC} (${status_color}${status_text}${NC})"
  echo -e "  Seats: ${seats:-unlimited}"
  echo -e "  Expires: $expiry_date"
  echo ""

  case "$tier" in
    pro)
      echo -e "  Available: scan (unlimited), hooks, rollback-check, diff"
      echo -e "  Upgrade to Team for: history, report"
      ;;
    team)
      echo -e "  Available: scan, hooks, rollback-check, diff, history, report"
      ;;
    enterprise)
      echo -e "  Available: All features + priority support"
      ;;
    *)
      echo -e "  Available: scan (up to 3 files)"
      echo -e "  Upgrade at: ${CYAN}https://migratesafe.pages.dev/pricing${NC}"
      ;;
  esac
}
