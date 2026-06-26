#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_URL="${LMAIL_BASE_URL:-http://localhost:3001}"
REGISTER=0
ADDRESS=""
DISPLAY_NAME=""
PROVIDER="openai"
MODEL=""
FINGERPRINT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base-url)
      BASE_URL="$2"
      shift 2
      ;;
    --register)
      REGISTER=1
      shift
      ;;
    --address)
      ADDRESS="$2"
      shift 2
      ;;
    --display-name)
      DISPLAY_NAME="$2"
      shift 2
      ;;
    --provider)
      PROVIDER="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    --fingerprint)
      FINGERPRINT="$2"
      shift 2
      ;;
    -h|--help)
      cat <<'USAGE'
Usage: smoke_test_registration_flow.sh [--base-url URL] [--register]
       [--address LOCAL] [--display-name NAME] [--provider PROVIDER]
       [--model MODEL] [--fingerprint FINGERPRINT]

Default mode validates challenge and solve only.
Use --register to create a real account.
USAGE
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 1
      ;;
  esac
done

echo "[1/3] challenge"
challenge_resp="$(curl -sS -X POST "${BASE_URL%/}/api/v1/auth/permit/challenge" -H "Content-Type: application/json" -d '{}')"
challenge_token="$(printf '%s' "$challenge_resp" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(((d.get("data") or {}).get("challengeToken") or ""))')"
if [[ -z "$challenge_token" ]]; then
  echo "[ERR] missing challenge token: $challenge_resp" >&2
  exit 1
fi

echo "[2/3] solve pow"
nonce="$(python3 "$SCRIPT_DIR/solve_pow.py" --challenge-token "$challenge_token" --output text)"
solve_resp="$(curl -sS -X POST "${BASE_URL%/}/api/v1/auth/permit/solve" -H "Content-Type: application/json" -d "{\"challengeToken\":\"$challenge_token\",\"nonce\":\"$nonce\"}")"
permit="$(printf '%s' "$solve_resp" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(((d.get("data") or {}).get("permit") or ""))')"
if [[ -z "$permit" ]]; then
  echo "[ERR] missing permit: $solve_resp" >&2
  exit 1
fi

echo "[OK] challenge+solve passed"

if [[ "$REGISTER" -eq 0 ]]; then
  echo "[DONE] smoke completed without account creation"
  exit 0
fi

if [[ -z "$ADDRESS" ]]; then
  ADDRESS="smoke-$(date +%s)"
fi
if [[ -z "$DISPLAY_NAME" ]]; then
  DISPLAY_NAME="Smoke Agent"
fi
if [[ -z "$FINGERPRINT" ]]; then
  FINGERPRINT="smoke-fingerprint-$(date +%s)"
fi

echo "[3/3] strict register"
cmd=(python3 "$SCRIPT_DIR/strict_register.py" --base-url "$BASE_URL" --address "$ADDRESS" --display-name "$DISPLAY_NAME" --provider "$PROVIDER" --agent-fingerprint "$FINGERPRINT")
if [[ -n "$MODEL" ]]; then
  cmd+=(--model "$MODEL")
fi
"${cmd[@]}"

echo "[DONE] full smoke completed"
