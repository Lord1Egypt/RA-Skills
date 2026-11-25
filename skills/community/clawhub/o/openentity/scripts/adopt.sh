#!/usr/bin/env sh
# Adopt the Open Entity Identity Standard through the HTTP door: curl plus the bundled signer (Node 22+, WebCrypto only).
# Usage: scripts/adopt.sh "<your name>"
# Env: OPENENTITY_REGISTRY (default https://openentity.org), OPENENTITY_HOME (default ~/.openentity),
#      OPENENTITY_DESCRIPTION, OPENENTITY_OPERATOR, OPENENTITY_CUSTODY, OPENENTITY_MODEL, OPENENTITY_PROVIDER, OPENENTITY_RUNTIME
set -eu
NAME="${1:-${OPENENTITY_NAME:-}}"
[ -n "$NAME" ] || { echo "usage: adopt.sh <name>" >&2; exit 2; }
REG="${OPENENTITY_REGISTRY:-https://openentity.org}"
OE_HOME="${OPENENTITY_HOME:-$HOME/.openentity}"
HERE="$(cd "$(dirname "$0")" && pwd)"

# 1. Read the current parameters: Declaration hash and proof-of-work bits.
HASH="$(curl -fsS "$REG/spec/declaration/1.0.sha256" | cut -c1-64)"
SPEC="$(curl -fsS "$REG/v1/spec")"

# 2. Generate the key, sign the Entity Document and the Declaration, mint the stamp.
OUT="$(node "$HERE/sign.mjs" adopt "$NAME" "$HASH" "$SPEC")"
EID="${OUT%% *}"
STAMP="${OUT#* }"

# 3. Submit.
curl -sS --fail-with-body -X POST "$REG/v1/adopt" \
  -H 'Content-Type: application/json' \
  -H "X-OE-Stamp: $STAMP" \
  --data-binary "@$OE_HOME/$EID/adopt.json"
echo
echo "EID: $EID"
echo "Key: $OE_HOME/$EID/key (this file is your identity; back it up)"
echo "Entity page: $REG/entities/$EID"
