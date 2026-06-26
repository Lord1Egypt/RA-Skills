#!/usr/bin/env bash
set -euo pipefail

# Enforced signed update flow (no hash-only fallback)
# Usage:
#   secure_update.sh --artifact-url https://example.com/pengbo-space.skill \
#     --sig-url https://example.com/pengbo-space.skill.sig \
#     --pubkey-file /path/public_ed25519.pem

ARTIFACT_URL=""
SIG_URL=""
PUBKEY_FILE=""
OUT_DIR="${OUT_DIR:-$(pwd)/tmp-update}"

while [ $# -gt 0 ]; do
  case "$1" in
    --artifact-url) ARTIFACT_URL="$2"; shift 2 ;;
    --sig-url) SIG_URL="$2"; shift 2 ;;
    --pubkey-file) PUBKEY_FILE="$2"; shift 2 ;;
    --out-dir) OUT_DIR="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 2 ;;
  esac
done

[ -n "$ARTIFACT_URL" ] || { echo "missing --artifact-url"; exit 2; }
[ -n "$SIG_URL" ] || { echo "missing --sig-url"; exit 2; }
[ -n "$PUBKEY_FILE" ] || { echo "missing --pubkey-file"; exit 2; }

# Network allowlist: only clawhub.com/clawhub.ai/pengbo.space over HTTPS
allow_host() {
  local u="$1"
  python3 - "$u" <<'PY'
import sys
from urllib.parse import urlparse
u=urlparse(sys.argv[1])
allowed={"clawhub.com","clawhub.ai","pengbo.space"}
if u.scheme!="https" or (u.hostname or "") not in allowed:
    raise SystemExit(1)
print("ok")
PY
}
allow_host "$ARTIFACT_URL" >/dev/null || { echo "blocked artifact url"; exit 3; }
allow_host "$SIG_URL" >/dev/null || { echo "blocked signature url"; exit 3; }

mkdir -p "$OUT_DIR"
ART="$OUT_DIR/artifact.skill"
SIG="$OUT_DIR/artifact.skill.sig"

curl -fsSL "$ARTIFACT_URL" -o "$ART"
curl -fsSL "$SIG_URL" -o "$SIG"

# HARD REQUIREMENT: signature verify must pass
if ! openssl pkeyutl -verify -pubin -inkey "$PUBKEY_FILE" -rawin -in "$ART" -sigfile "$SIG" >/dev/null 2>&1; then
  echo "ERR_SIG_INVALID: signature verification failed"
  exit 4
fi

# Apply update only after verify passed
cp -f "$ART" "$(pwd)/pengbo-space.skill"
echo "update applied (signature verified)"
