#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scan.sh <directory>

Scan a directory for local traces that prevent clean publishing:
  - Hardcoded absolute paths (/root/, /home/, /tmp/)
  - Hardcoded IP addresses
  - API keys / tokens (sk-, ghp_, xoxb-, etc.)
  - Local username references
  - openclaw.json config references
  - Sensitive values in .env files

Output: file:line:match:risk_level
EOF
  exit 1
}

[[ $# -lt 1 ]] && usage
TARGET_DIR="$1"
[[ ! -d "$TARGET_DIR" ]] && echo "ERROR: '$TARGET_DIR' is not a directory" && exit 1

FOUND=0

SELF_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"

scan_pattern() {
  local label="$1" pattern="$2" risk="$3"
  while IFS= read -r line; do
    local file="${line%%:*}"
    [[ "$(realpath "$file")" == "$SELF_PATH" ]] && continue
    echo "${line}:${risk}  # ${label}"
    FOUND=1
  done < <(grep -rnI --include='*' -E "$pattern" "$TARGET_DIR" \
    --exclude-dir='.git' --exclude-dir='node_modules' \
    --exclude-dir='__pycache__' --exclude-dir='.venv' \
    --exclude='*.png' --exclude='*.jpg' --exclude='*.ico' \
    2>/dev/null || true)
}

# 1. Hardcoded absolute paths
scan_pattern "hardcoded-path" \
  '(/root/|/home/[a-zA-Z]|/Users/[a-zA-Z]|/tmp/[a-zA-Z])' \
  "HIGH"

# 2. Hardcoded IP addresses (skip 0.0.0.0, 127.0.0.1, common docs)
scan_pattern "hardcoded-ip" \
  '\b(10\.[0-9]+\.[0-9]+\.[0-9]+|172\.(1[6-9]|2[0-9]|3[01])\.[0-9]+\.[0-9]+|192\.168\.[0-9]+\.[0-9]+)\b' \
  "MEDIUM"

# 3. API keys / tokens
scan_pattern "api-key" \
  '(sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|xoxb-[0-9]|xoxp-[0-9]|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35})' \
  "CRITICAL"

# 4. Generic secret patterns (password=, token=, secret= with values)
scan_pattern "secret-assignment" \
  '(password|token|secret|api_key|apikey|access_key)\s*[=:]\s*["\x27]?[a-zA-Z0-9/+]{8,}' \
  "HIGH"

# 5. Local username references
if [[ -n "${USER:-}" ]]; then
  scan_pattern "local-username" \
    "\\b${USER}\\b" \
    "MEDIUM"
fi

# 6. openclaw.json references
scan_pattern "openclaw-config" \
  'openclaw\.json' \
  "LOW"

# 7. .env file sensitive values (scan .env* files specifically)
while IFS= read -r envfile; do
  while IFS= read -r line; do
    echo "${line}:HIGH  # env-secret"
    FOUND=1
  done < <(grep -nE '^[A-Z_]+\s*=\s*.+' "$envfile" \
    | grep -ivE '=(true|false|[0-9]+|""|'\'''\''|\$\{)' 2>/dev/null || true)
done < <(find "$TARGET_DIR" -maxdepth 3 -name '.env*' -not -name '.env.example' \
  -not -path '*/.git/*' 2>/dev/null || true)

# Summary
if [[ "$FOUND" -eq 0 ]]; then
  echo "CLEAN: No local traces found in $TARGET_DIR"
  exit 0
else
  echo ""
  echo "--- scan complete: issues found above ---"
  exit 1
fi
