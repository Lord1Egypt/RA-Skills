---
name: hederatoolbox
description: Query live Hedera blockchain data — token prices, whale movements, HCS topics, governance proposals, identity/KYC screening, and smart contract analysis. Pay-per-call via HBAR micropayments. No signup required.
version: 1.0.3
homepage: https://hederatoolbox.com
metadata:
  clawdbot:
    emoji: "⬡"
    primaryEnv: HEDERA_ACCOUNT_ID
    requires:
      env:
        - HEDERA_ACCOUNT_ID
---

# HederaToolbox

Query live Hedera blockchain data using AI-native, pay-per-call tools. No registration, no API keys to manage — send HBAR to the platform wallet once, and your Hedera account ID becomes your permanent key.

## What This Skill Does

When active, your agent can call 20 Hedera blockchain tools across 6 modules:

- **Token** — HBAR/token price, whale movement alerts, deep token analysis
- **HCS** — Query and monitor Hedera Consensus Service topics, anomaly detection
- **Compliance** — Write and verify tamper-proof audit records on HCS
- **Identity** — Resolve accounts, verify KYC status, sanctions screening
- **Governance** — Monitor and analyze active proposals and vote splits
- **Contract** — Read state, call functions, analyze smart contract activity

## Setup (One Time)

1. **Get your Hedera account ID** — format `0.0.XXXXXX`. Any mainnet account works.
2. **Fund your balance** — Send HBAR to the platform wallet `0.0.10309126` from your account. Your account ID becomes your API key within 10 seconds.
3. **Set the env var** — Add `HEDERA_ACCOUNT_ID=0.0.XXXXXX` to your OpenClaw config.

**Recommended starting balance: 10 HBAR (~$0.96 at current prices)**

At 10 HBAR you get approximately:
- 50 token price checks (0.10 ħ each), or
- 13 deep token analyses (0.60 ħ each), or
- A full compliance onboarding workflow (identity_resolve + identity_verify_kyc + identity_check_sanctions + hcs_write_record ≈ 6.70 ħ), or
- Roughly 8 complete scheduled agent runs at the X agent profile (≈1.15 ħ/run)

Send more at any time — balance tops up within 10 seconds.

## Security & Trust

**Your private key is never requested, stored, or transmitted.** This skill only uses your public Hedera account ID (`0.0.XXXXXX`). No wallet signing is required at any point.

**How payment verification works:** The platform runs a deposit watcher that polls the Hedera Mirror Node every 10 seconds for incoming transfers to the platform wallet (`0.0.10309126`). Hedera transactions cryptographically record the sender account ID on-chain — no memo or transaction hash is required from you. When a transfer is detected from your account, your balance is credited automatically. You can verify any deposit on Hashscan: https://hashscan.io/mainnet/account/0.0.10309126. The watcher source code is at https://github.com/mountainmystic/hederatoolbox/blob/master/src/watcher.js.

**"Permanent key" clarification:** Your Hedera account ID is a persistent billing identifier — not a cryptographic credential. The platform tracks which account sent HBAR using on-chain transaction records from the Mirror Node. Only the account that deposited HBAR can spend that balance.

**On-chain writes:** Tools like `hcs_write_record` write HCS messages signed by the platform operator key (server-side, using the platform's own Hedera account). Your account ID is included in the message payload as the originator field — it is metadata, not a transaction signer. The transaction itself is signed by and appears on-chain as originating from the platform account (`0.0.10309126`), not yours. This is standard for metered API services on Hedera.

**Payment model:** You send HBAR using your own wallet (HashPack, Blade, CLI, etc.) before using the skill. The skill itself never initiates transfers or requests funds. All charges are deducted from your pre-funded balance only — the platform cannot pull additional funds from your wallet.

**Data sent off-platform:** Tool calls (account IDs, contract addresses, token IDs, query parameters) are sent to `api.hederatoolbox.com`. See the Privacy Policy at https://hederatoolbox.com/privacy.html for retention and sharing details.

**Start small:** Test with 2–5 HBAR before committing more. Full source: https://github.com/mountainmystic/hederatoolbox

## Tool Pricing (HBAR)

| Module | Tool | Cost |
|--------|------|------|
| Free | get_terms, confirm_terms, account_info | 0 ħ |
| HCS | hcs_monitor, hcs_query | 0.10 ħ |
| HCS | hcs_understand | 1.00 ħ |
| Compliance | hcs_write_record | 5.00 ħ |
| Compliance | hcs_verify_record | 1.00 ħ |
| Compliance | hcs_audit_trail | 2.00 ħ |
| Governance | governance_monitor | 0.20 ħ |
| Governance | governance_analyze | 1.00 ħ |
| Token | token_price | 0.10 ħ |
| Token | token_monitor | 0.20 ħ |
| Token | token_analyze | 0.60 ħ |
| Identity | identity_resolve | 0.20 ħ |
| Identity | identity_verify_kyc | 0.50 ħ |
| Identity | identity_check_sanctions | 1.00 ħ |
| Contract | contract_read | 0.20 ħ |
| Contract | contract_call | 1.00 ħ |
| Contract | contract_analyze | 1.50 ħ |

## MCP Endpoint

```
https://api.hederatoolbox.com/mcp
```

Standard MCP-over-HTTP. Compatible with any MCP client.

## When To Use This Skill

Use HederaToolbox tools when the user asks about:

- **HBAR price or market data** → `token_price`
- **Whale activity or unusual transfers** → `token_monitor`
- **Deep token risk analysis** → `token_analyze`
- **Reading or monitoring an HCS topic** → `hcs_monitor` or `hcs_query`
- **Detecting anomalies in HCS traffic** → `hcs_understand`
- **Writing a compliance record on-chain** → `hcs_write_record`
- **Verifying an existing compliance record** → `hcs_verify_record`
- **Full audit trail for an account or topic** → `hcs_audit_trail`
- **Resolving a Hedera account identity** → `identity_resolve`
- **KYC status for a token** → `identity_verify_kyc`
- **Sanctions screening** → `identity_check_sanctions`
- **Active governance proposals** → `governance_monitor`
- **Voter sentiment and participation** → `governance_analyze`
- **Smart contract state** → `contract_read`
- **Calling a contract function** → `contract_call`
- **Contract activity patterns and risk** → `contract_analyze`
- **Checking balance or platform info** → `account_info`

## Example Agent Prompts

```
Check the current HBAR price and look for any whale activity in the last hour.
```

```
Monitor HCS topic 0.0.10353855 and tell me if there's anything unusual.
```

```
Run a KYC check on account 0.0.7925398 for token 0.0.731861.
```

```
Analyze the SaucerSwap contract 0.0.1460200 and give me a risk summary.
```

```
What are the active governance proposals for SAUCE token right now?
```

## Tool Call Format

All tools follow the same MCP pattern. Pass your account ID as `api_key`:

```json
{
  "tool": "token_price",
  "arguments": {
    "tokenId": "0.0.1456986",
    "api_key": "0.0.YOUR_ACCOUNT_ID"
  }
}
```

The agent reads `HEDERA_ACCOUNT_ID` from the environment and passes it automatically.

## Checking Your Balance

Ask the agent: *"What's my HederaToolbox balance?"*

This calls `account_info` (free) and returns your remaining balance in HBAR.

## Topping Up

Send additional HBAR to `0.0.10309126` from your account at any time. Balance updates within 10 seconds.

## What You Could Build

- **Compliance onboarding agent** — resolve + KYC + sanctions + write HCS record for any Hedera account. Board-ready audit trail in one workflow (~6.70 ħ total).
- **Whale alert bot** — run `token_monitor` on a schedule, surface unusual transfers to Telegram or Slack.
- **DAO governance digest** — daily `governance_monitor` + `governance_analyze` summary for any token with active proposals.
- **Smart contract due diligence** — `contract_analyze` + `identity_resolve` on all callers, output a risk report.
- **On-chain market pulse** — `token_price` + `token_monitor` twice daily, draft a tweet or Slack summary from the data.

## Links

- Website: https://hederatoolbox.com
- GitHub: https://github.com/mountainmystic/hederatoolbox
- npm: `@hederatoolbox/platform`
- MCP Registry: `io.github.mountainmystic/hederatoolbox`
- Terms: https://hederatoolbox.com/terms.html
- Privacy: https://hederatoolbox.com/privacy.html
