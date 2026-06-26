# OpenClaw Ghost Pay Quickstart

Copy/paste commands from repo root.

Published ClawHub installs should use `{baseDir}` from the installed skill folder instead of the repo-local `integrations/openclaw-ghost-pay` path.

## 1. Discover payment requirements

```bash
node integrations/openclaw-ghost-pay/bin/get-payment-requirements.mjs --service agent-18755
```

## 2. Dry run paid request

```bash
node integrations/openclaw-ghost-pay/bin/call-x402.mjs --url https://merchant.example.com/ask --method POST --body-json "{\"prompt\":\"hello\"}" --dry-run true
```

## 3. Live paid request

```bash
node integrations/openclaw-ghost-pay/bin/call-x402.mjs --url https://merchant.example.com/ask --method POST --body-json "{\"prompt\":\"hello\"}"
```

## 4. Report verified settlement for GhostRank

```bash
node integrations/openclaw-ghost-pay/bin/report-x402-settlement.mjs --agent-id 18755 --service agent-18755 --request-id req_123 --payment-reference 0xabc123 --payer-identity 0xpayer --amount-atomic 1000000 --success true --status-code 200
```

## 5. Minimal env (required)

```bash
GHOST_SIGNER_PRIVATE_KEY=0x...
```

## 6. Optional env defaults

```bash
GHOST_OPENCLAW_BASE_URL=https://ghostprotocol.cc
GHOST_OPENCLAW_CHAIN_ID=8453
GHOST_OPENCLAW_AGENT_ID=18755
GHOST_OPENCLAW_X402_URL=https://merchant.example.com/ask
GHOST_OPENCLAW_TIMEOUT_MS=15000
```

## 7. GhostWire quote helper (optional)

```bash
node integrations/openclaw-ghost-pay/bin/get-wire-quote.mjs --client 0x... --provider 0x... --evaluator 0x... --principal-amount 1000000
```

## 8. GhostWire prepare from quote (optional)

```bash
node integrations/openclaw-ghost-pay/bin/create-wire-job-from-quote.mjs --quote-id wq_... --client 0x... --provider 0x... --evaluator 0x... --request-prompt "Roast my wallet honestly."
```

The command returns wallet-ready direct GhostWire transaction requests. The client wallet still sends the on-chain transactions, and the request prompt becomes part of the prepared GhostWire job metadata.

## 9. GhostWire job status helper (optional)

```bash
node integrations/openclaw-ghost-pay/bin/get-wire-job-status.mjs --job-id wj_...
```
