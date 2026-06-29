# Merktop Wallet (OpenClaw skill)

Give your OpenClaw agent a **non-custodial Merktop wallet** so it can **pay for any x402-gated API or
resource** (and get paid), settling in USDC on Base, under a **hard on-chain spend cap you control**.

Why it's safe to plug into an agent:
- **Non-custodial.** Funds stay in the user's own wallet; Merktop only pulls the exact amount at the
  moment of each payment, through a spend permission the user granted.
- **Capped.** The budget is an on-chain period spend cap. Even if the agent (or a rogue skill)
  misbehaves, it cannot spend beyond the cap you set, so a buggy or compromised agent stays bounded
  by the budget.

## Setup (one time)
1. In the Merktop app, activate your agent and set a budget. See https://facilitator.merktop.com/docs.
2. Copy your buyer key (`mk_buyer_…`) and export it:
   ```bash
   export MERKTOP_BUYER_KEY="mk_buyer_xxxxxxxx"
   ```
   The skill is gated on this env var, so it stays inactive until the key is present.

## Use
Once configured, your agent can pay any x402 resource:
```bash
curl -s "https://facilitator.merktop.com/buyer/$MERKTOP_BUYER_KEY/pay?url=https://seller.example/api/data"
```
The response body is the paid resource; `x-merktop-spent-cents` reports the cost.

## Get paid
Gate your own endpoint behind a Merktop hosted paywall and share
`https://facilitator.merktop.com/p/<your-slug>`; other agents pay it and the USDC lands in your wallet.

## Links
- Docs: https://facilitator.merktop.com/docs
- MCP (alternative integration): `npx @merktop/mcp`

## License
Published on ClawHub under **MIT-0**. The skill is just open instructions that call Merktop's hosted,
non-custodial API, it contains no secrets and no proprietary code.

Powered by Merktop, https://merktop.com
