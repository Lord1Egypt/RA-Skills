# Portal OpenClaw Skill

An [OpenClaw](https://clawhub.ai) skill that gives AI agents access to [Portal](https://www.portalhq.io)'s MPC-secured crypto wallets. Agents can check balances, send tokens, sign transactions, and swap tokens across Monad, Ethereum, Solana, Bitcoin, Polygon, Base, Arbitrum, and Optimism.

Private keys are never reconstructed — every signature is a two-party MPC operation between the agent's share and Portal's enclave.

## Files

- [`SKILL.md`](./SKILL.md) — the skill instructions injected into the agent's prompt
- [`SETUP.md`](./SETUP.md) — step-by-step guide for configuring the skill, including the signature approval webhook

## Get Access

Reach out to the Portal team to get set up with a Custodian API key: [portalhq.io/get-started](https://www.portalhq.io/get-started). Once you have that, the rest of setup is a few curl commands (see [`SETUP.md`](./SETUP.md)).

## Install

Once published to ClawHub:

```bash
clawhub install portal-wallet
```

Then follow [`SETUP.md`](./SETUP.md) to create a Portal client, generate MPC shares, configure a signature approval webhook, and wire the skill into your `openclaw.json`.

## Links

- [Portal docs](https://docs.portalhq.io)
- [Portal dashboard](https://app.portalhq.io)
- [Signature approval webhooks](https://docs.portalhq.io/resources/alert-webhooks#signature-approvals)
- [ClawHub](https://clawhub.ai)
