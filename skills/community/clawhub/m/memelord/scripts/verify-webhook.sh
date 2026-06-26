#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
if [[ -f "$ROOT_DIR/_env.sh" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT_DIR/_env.sh"
fi

# Helper: verify Memelord webhook signatures (HMAC-SHA256)
# You provide:
#   --secret <webhookSecret>
#   --body-file <raw_body_path>
#   --signature <hex>
#
# This is generic since different webhook setups put the signature in different headers.

usage() {
  cat <<'USAGE'
Usage:
  verify-webhook.sh --secret "<webhookSecret>" --body-file <raw_body.txt> --signature <hex>

Example:
  ./verify-webhook.sh --secret "$WEBHOOK_SECRET" --body-file ./payload.json --signature "deadbeef..."
USAGE
}

SECRET=""
BODY_FILE=""
SIG=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage; exit 0;;
    --secret) SECRET="$2"; shift 2;;
    --body-file) BODY_FILE="$2"; shift 2;;
    --signature) SIG="$2"; shift 2;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2;;
  esac
done

if [[ -z "$SECRET" || -z "$BODY_FILE" || -z "$SIG" ]]; then
  echo "Missing required args" >&2
  usage
  exit 2
fi

# Compute hex digest of HMAC-SHA256(secret, rawBody)
COMPUTED=$(node - <<'NODE' "$SECRET" "$BODY_FILE"
const fs = require('fs');
const crypto = require('crypto');
const secret = process.argv[2];
const bodyPath = process.argv[3];
const raw = fs.readFileSync(bodyPath);
const h = crypto.createHmac('sha256', secret).update(raw).digest('hex');
process.stdout.write(h);
NODE
)

if [[ "${COMPUTED}" == "${SIG}" ]]; then
  echo "OK"
  exit 0
fi

echo "FAIL"
echo "computed=$COMPUTED"
echo "given=$SIG"
exit 1
