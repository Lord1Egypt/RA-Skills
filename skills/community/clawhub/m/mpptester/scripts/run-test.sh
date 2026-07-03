#!/usr/bin/env bash
# Run an MPP send test end-to-end against mpptester.com.
# Usage: run-test.sh [mainnet-beta|devnet] [label]
# Starts a test, prints the Solana Pay URL to pay, then polls until the result
# is known and prints the shareable receipt link.
set -euo pipefail

BASE="${MPP_BASE_URL:-https://mpptester.com}"
NETWORK="${1:-mainnet-beta}"
LABEL="${2:-skill test}"

case "$NETWORK" in
  mainnet-beta|devnet) ;;
  *) echo "network must be 'mainnet-beta' or 'devnet'"; exit 2 ;;
esac

echo "Starting $NETWORK MPP test…"
START=$(curl -s -X POST "$BASE/api/mpp/start" \
  -H 'Content-Type: application/json' \
  -d "{\"network\":\"$NETWORK\",\"label\":\"$LABEL\"}")

REF=$(printf '%s' "$START" | python3 -c "import sys,json;print(json.load(sys.stdin)['reference'])")
PAY=$(printf '%s' "$START" | python3 -c "import sys,json;print(json.load(sys.stdin)['paymentUrl'])")

echo
echo "Test reference : $REF"
echo "Receipt        : $BASE/test/$REF"
echo
echo "Pay this Solana Pay request (\$0.50 USDC, must include the reference):"
echo "  $PAY"
echo
echo "Waiting for payment (expires in 30 min)…"

for i in $(seq 1 120); do
  sleep 5
  RESP=$(curl -s "$BASE/api/mpp/tests/$REF")
  STATUS=$(printf '%s' "$RESP" | python3 -c "import sys,json;print(json.load(sys.stdin).get('status',''))")
  case "$STATUS" in
    confirmed)
      SIG=$(printf '%s' "$RESP" | python3 -c "import sys,json;print(json.load(sys.stdin).get('txSignature',''))")
      echo "PASSED ✓  tx: $SIG"
      echo "Proof: $BASE/test/$REF"
      exit 0 ;;
    expired)
      echo "EXPIRED — no payment received in time."
      exit 1 ;;
    *)
      printf '.' ;;
  esac
done

echo
echo "Still pending after timeout. Check $BASE/test/$REF"
exit 1
