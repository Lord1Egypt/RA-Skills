---
name: openclaw-ghost-pay
description: Discover Ghost payment requirements, execute real x402 calls, report x402 settlements, and run GhostWire quote/prepare/status flows for direct escrow.
version: 1.5.0
metadata: {"clawdis":{"homepage":"https://github.com/Ghost-Protocol-Infrastructure/GHOST_PROTOCOL/tree/main/integrations/openclaw-ghost-pay","os":["darwin","linux","win32"],"requires":{"env":["GHOST_SIGNER_PRIVATE_KEY"],"bins":["node"]},"primaryEnv":"GHOST_SIGNER_PRIVATE_KEY","install":[{"id":"viem","kind":"node","package":"viem","label":"Install viem (required for settlement reporting)"}]}}
---

# OpenClaw Ghost Pay

Use this skill when an OpenClaw agent must:

1. Discover Ghost payment requirements for a service.
2. Execute a real `x402` request against a merchant endpoint.
3. Report a verified `x402` settlement back to Ghost for GhostRank.
4. Optionally run GhostWire quote/prepare/status flows.

This published skill bundle includes the helper scripts it references. Use `{baseDir}` when invoking them so the commands work after `clawhub install openclaw-ghost-pay`.

## Required environment

- `GHOST_SIGNER_PRIVATE_KEY` (required): trusted signing key for `x402` calls and settlement reporting.

Optional:

- `GHOST_OPENCLAW_BASE_URL` (default: `https://ghostprotocol.cc`)
- `GHOST_OPENCLAW_CHAIN_ID` (default: `8453`)
- `GHOST_OPENCLAW_SERVICE_SLUG` (optional default service slug)
- `GHOST_OPENCLAW_AGENT_ID` (optional default agent id for settlement reporting)
- `GHOST_OPENCLAW_X402_URL` (optional default merchant endpoint URL for `call-x402.mjs`)
- `GHOST_OPENCLAW_TIMEOUT_MS` (default: `15000`)
- `GHOSTWIRE_PROVIDER_ADDRESS`
- `GHOSTWIRE_EVALUATOR_ADDRESS`
- `GHOSTWIRE_PRINCIPAL_AMOUNT`
- `GHOSTWIRE_CLIENT_ADDRESS`
- `GHOSTWIRE_SPEC_HASH` (optional explicit override; otherwise derive from request)
- `GHOSTWIRE_REQUEST_PROMPT`
- `GHOSTWIRE_REQUEST_JSON`
- `GHOSTWIRE_REQUEST_WALLET`
- `GHOSTWIRE_REQUEST_METADATA_JSON`
- `GHOSTWIRE_METADATA_URI`
- `GHOSTWIRE_APPROVAL_MODE`

Never put private keys in prompts, plaintext config screenshots, or frontend output.

## Flow

### 1. Get payment requirements

```bash
node {baseDir}/bin/get-payment-requirements.mjs --service agent-18755
```

This calls Ghost read-only MCP and resolves:

- Express gate endpoint
- chain id
- request cost credits
- Ghost's canonical `x402` metadata block

### 2. Dry run a real x402 request

```bash
node {baseDir}/bin/call-x402.mjs --url https://merchant.example.com/ask --method POST --body-json "{\"prompt\":\"hello\"}" --dry-run true
```

### 3. Execute a live x402 request

```bash
node {baseDir}/bin/call-x402.mjs --url https://merchant.example.com/ask --method POST --body-json "{\"prompt\":\"hello\"}"
```

This helper runs the real `402 -> payment -> retry` flow against the merchant endpoint.

### 4. Report the verified settlement back to Ghost

```bash
node {baseDir}/bin/report-x402-settlement.mjs --agent-id 18755 --service agent-18755 --request-id req_123 --payment-reference 0xabc123 --payer-identity 0xpayer --amount-atomic 1000000 --success true --status-code 200
```

This is the step that makes successful `x402` usage visible to GhostRank.

## GhostWire flow

### 5. Get a GhostWire quote

```bash
node {baseDir}/bin/get-wire-quote.mjs --client 0x... --provider 0x... --evaluator 0x... --principal-amount 1000000
```

### 6. Create a GhostWire job from a quote

```bash
node {baseDir}/bin/create-wire-job-from-quote.mjs --quote-id wq_... --client 0x... --provider 0x... --evaluator 0x... --request-prompt "Roast my wallet honestly."
```

### 7. Poll GhostWire job status

```bash
node {baseDir}/bin/get-wire-job-status.mjs --job-id wj_... --wait-terminal true
```

## Safe usage rules

- Use only against approved Ghost service slugs and merchant-approved GhostWire roles.
- Do not log signer private keys.
- Prefer `--dry-run true` before the first live paid request in a new runtime.
- Treat `402` as a payment challenge or policy failure, not a transport failure.
- Treat GhostWire prepare output as sensitive transaction-prep data for the client wallet.
- For GhostWire, put the consumer task in `--request-prompt` / `--request-json`; keep `--metadata-uri` for the merchant deliverable locator.
