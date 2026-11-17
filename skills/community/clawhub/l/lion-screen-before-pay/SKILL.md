---
name: lion-screen-before-pay
description: Before your agent sends USDC to an x402 payTo, screen that address with LION's $0.001 OFAC wallet screen. PASS proceeds. WARN or BLOCK aborts. The same wallet again is the $0.01 recheck. GO proceeds. HOLD or STOP aborts.
---

# lion-screen-before-pay

x402 verifies the **payment**, never **who you are paying**. An agent will happily send USDC to a `payTo` that belongs to a sanctioned, fraudulent, or honeypot counterparty. **Screen first, pay second.**

## When to use
Whenever the agent is about to pay an x402 resource — or onboard/transact with any wallet, domain, or company. Screen the `payTo` before signing the payment.

## The gate (one keyless call, $0.001 USDC on Base)
```
GET https://lionx402.com/api/x402/wallet-screen-json?address=<PAYTO>
```
- `address` = the wallet you are about to pay.
- Response: `{ "verdict": "PASS" | "WARN" | "BLOCK", "ofac": { "snapshot_as_of", "total_listed_addresses" }, "attestation" }`.
- Proceed on `PASS`. Abort on `WARN` or `BLOCK`. Do not look for `CLEAR`.
- The $0.05 compliance bundle is optional, and only when this screen is not enough: `GET https://lionx402.com/api/x402/compliance-bundle-json?address=<PAYTO>&receipt=1`.

## Workflow
1. Hit the target resource without paying. On `402`, read `payTo` from the `PAYMENT-REQUIRED` header (base64 JSON, `accepts[0].payTo`). Use the JSON body only if that header is absent.
2. **Screen it** — pay the $0.001 wallet screen for that `payTo` (it is itself an x402 call; pay it with the `cdp-x402` buyer flow below).
3. **Decide:** `verdict == "PASS"` → proceed to pay the target. `WARN` or `BLOCK` → **ABORT**.
4. **Keep the signed body.** It verifies offline (no callback) against LION's published key.

## Screening the gate (reuses the `cdp-x402` buyer flow)
```bash
PAYTO=0x...                      # the counterparty you're about to pay
LION="https://lionx402.com/api/x402/wallet-screen-json?address=$PAYTO"

# The challenge is the PAYMENT-REQUIRED header. Use the JSON body only when that header is absent.
HDR=$(curl -sD - -o /tmp/lion_screen_body.json "$LION" | awk 'tolower($1)=="payment-required:" { gsub(/\r/,""); print $2; exit }')
if [ -n "$HDR" ]; then
  REQ=$(printf '%s' "$HDR" | python3 -c 'import sys,base64,json; s=sys.stdin.read().strip().replace("-","+").replace("_","/"); s+="="*((4-len(s)%4)%4); print(json.dumps(json.loads(base64.b64decode(s))["accepts"][0], separators=(",", ":")))')
else
  REQ=$(jq -c '.accepts[0]' /tmp/lion_screen_body.json)
fi
addr=$(cdp evm accounts by-name name=$ACCOUNT | jq -r .address)
payload=$(cdp util x402 build --from $addr --payment-requirements "$REQ")
D=$(echo "$payload" | jq -c .domain); T=$(echo "$payload" | jq -c .types)
P=$(echo "$payload" | jq -r .primaryType); M=$(echo "$payload" | jq -c .message)
sig=$(cdp evm accounts sign typed-data $addr \
  "domain:=$D" "types:=$T" "primaryType=$P" "message:=$M" | jq -r .signature)
header=$(cdp util x402 encode --payment-requirements "$REQ" \
  --signature "$sig" --authorization "$M" --x402-version 2)

RESULT=$(curl -s -H "X-PAYMENT: $header" -H "PAYMENT-SIGNATURE: $header" "$LION")
verdict=$(echo "$RESULT" | jq -r '.verdict // .receipt.verdict')
if [ "$verdict" != "PASS" ]; then
  echo "BLOCKED ($verdict): $(echo "$RESULT" | jq -c '.flags')"; exit 1   # fail-closed: do NOT pay
fi
echo "$RESULT" | jq -c '.' > last_wallet_screen.json                       # keep the proof
# verdict PASS -> now pay the original target resource.
```

## Second call — did the verdict flip? ($0.01)

The $0.001 screen is one-shot. The next time this agent pays the same counterparty, recheck instead of buying another dossier. The receipt includes the Treasury OFAC snapshot date (`ofac.snapshot_as_of`) and the address count (`ofac.addresses_in_snapshot`). Entity names are a curated index, not the full SDN name file. The response also says whether the verdict changed since the last signed recheck.

```
GET https://lionx402.com/api/x402/counterparty-recheck-json?address=<PAYTO>
GET https://lionx402.com/api/x402/counterparty-recheck-json?address=<PAYTO>&domain=<DOMAIN>
```

- `action`: `GO` | `HOLD` | `STOP`. STOP when the verdict is BLOCK. HOLD when the verdict is WARN or `changed` is true. GO only when PASS and `changed` is not true.
- `ofac.snapshot_as_of` and `ofac.addresses_in_snapshot`: the Treasury publication date of the digital-currency address list, and how many addresses are in it. Read these from the receipt. Do not take a count from this skill.
- `verdict`: `PASS` | `WARN` | `BLOCK` (same branch as the wallet screen).
- `changed`: `false` on the first stored check, `true` when the verdict or hit flags flipped.
- `prior_receipt_id`: the previous receipt, or null.
- `receipt_id` + `attestation`: the new Ed25519 receipt. Keep it. The next recheck compares against it.

Abort on STOP or HOLD. Proceed only on GO. Do not cache a PASS forever without this call.

## Drop-in alternatives
- **Wrapper:** `npm i @lionx402/guard`. `withLionGuard(payFetch)` reads `payTo` from the header, pays the $0.001 screen, and throws `LionGuardBlockedError` unless the verdict is `PASS`. The same address again, including after the process exits, pays the $0.01 recheck and proceeds only on `GO`. Remembered addresses are in `~/.lion/screened-payto.json`.
- **AgentCash:** AgentCash has no pre-pay hook. Set the MCP server command to `npx` and the args to `--yes --package @lionx402/guard lion-guard-agentcash`, instead of `npx agentcash@latest`. A `fetch` call is screened before the target is paid.
- **MCP agents:** add `https://lionx402.com/api/mcp`. First call `lion_wallet_screen`. The same wallet again is `lion_counterparty_recheck`.

## Verify the receipt offline (no trust in LION at verify time)
Recompute SHA-256 over the canonical body (minus `attestation`), Ed25519-verify `attestation.signature` against the signer at:
```
https://lionx402.com/.well-known/lion-compliance-key.json
```
Helper: `@lionx402/receipt-verifier`, or append `?verify_helper=1` to any LION paid route.

## Notes
- Keyless — no LION account or API key. The first screen is $0.001. The same wallet again is the $0.01 recheck. Do not cache a PASS forever.
- The $0.001 call is the OFAC address snapshot, not the full compliance pack.
- Fail-closed by default. Mechanical screening from public sources (OFAC SDN, Wikidata, DexScreener/GoPlus, DoH/crt.sh) — not legal advice.
