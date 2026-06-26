# OpenClaw Ghost Pay Install

## Requirements

- Node.js 20+ runtime
- Trusted server/runtime environment
- `GHOST_SIGNER_PRIVATE_KEY` set as a secret

## 1. Install dependencies

For local repo use:

```bash
npm install
```

For package-only local use:

```bash
cd integrations/openclaw-ghost-pay
npm install
```

For ClawHub publish/install, publish the folder root so the helper scripts ship with the skill bundle:

```bash
clawhub publish ./integrations/openclaw-ghost-pay --slug openclaw-ghost-pay --name "Ghost Protocol OpenClaw Pay" --version 1.5.0 --tags latest,agents,eip712,ghostprotocol,ghostwire,mcp,openclaw,payments,x402
```

If `clawhub` fails with `fetch failed` in this environment, use the bundled wrapper:

```powershell
powershell -ExecutionPolicy Bypass -File ./integrations/openclaw-ghost-pay/scripts/clawhub.ps1 publish ./integrations/openclaw-ghost-pay --slug openclaw-ghost-pay --name "Ghost Protocol OpenClaw Pay" --version 1.5.0 --tags latest,agents,eip712,ghostprotocol,ghostwire,mcp,openclaw,payments,x402
```

## 2. Set runtime env

Required:

```bash
GHOST_SIGNER_PRIVATE_KEY=0x...
```

Optional:

```bash
GHOST_OPENCLAW_BASE_URL=https://ghostprotocol.cc
GHOST_OPENCLAW_CHAIN_ID=8453
GHOST_OPENCLAW_SERVICE_SLUG=agent-18755
GHOST_OPENCLAW_AGENT_ID=18755
GHOST_OPENCLAW_X402_URL=https://merchant.example.com/ask
GHOST_OPENCLAW_TIMEOUT_MS=15000
GHOSTWIRE_PROVIDER_ADDRESS=0x...
GHOSTWIRE_EVALUATOR_ADDRESS=0x...
GHOSTWIRE_PRINCIPAL_AMOUNT=1000000
GHOSTWIRE_CLIENT_ADDRESS=0x...
GHOSTWIRE_REQUEST_PROMPT=Roast my wallet honestly.
GHOSTWIRE_APPROVAL_MODE=exact
```

## 3. Register plugin in local OpenClaw config

Use the package root:

```json
{
  "plugins": {
    "ghost-protocol-openclaw": {
      "path": "./integrations/openclaw-ghost-pay",
      "enabled": true,
      "skills": {
        "entries": {
          "openclaw-ghost-pay": {
            "enabled": true
          }
        }
      }
    }
  }
}
```

## 4. Validate installation

```bash
node integrations/openclaw-ghost-pay/bin/get-payment-requirements.mjs --service agent-18755
```

If that succeeds, run paid dry run:

```bash
node integrations/openclaw-ghost-pay/bin/call-x402.mjs --url https://merchant.example.com/ask --method POST --body-json "{\"prompt\":\"hello\"}" --dry-run true
```

Then report a verified settlement when a real request succeeds:

```bash
node integrations/openclaw-ghost-pay/bin/report-x402-settlement.mjs --agent-id 18755 --service agent-18755 --request-id req_123 --payment-reference 0xabc123 --payer-identity 0xpayer --amount-atomic 1000000 --success true --status-code 200
```

Optional GhostWire wrappers:

```bash
node integrations/openclaw-ghost-pay/bin/get-wire-quote.mjs --client 0x... --provider 0x... --evaluator 0x... --principal-amount 1000000
```

```bash
node integrations/openclaw-ghost-pay/bin/create-wire-job-from-quote.mjs --quote-id wq_... --client 0x... --provider 0x... --evaluator 0x... --request-prompt "Roast my wallet honestly."
```

```bash
node integrations/openclaw-ghost-pay/bin/get-wire-job-status.mjs --job-id wj_...
```
