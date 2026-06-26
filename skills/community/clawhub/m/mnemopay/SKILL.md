---
name: mnemopay
description: Trust OS for AI agents that handle money or consequential actions. Adds governed memory, payments, reputation, identity, approvals, audit evidence, and durable browser/code/computer jobs.
---

# MnemoPay

MnemoPay is the trust and control layer for autonomous agents. Use it when an
agent needs persistent memory, payment rails, scoped authority, budgets,
approvals, reputation, or verifiable evidence of what it did.

## Install

```bash
npm install @mnemopay/sdk
claude mcp add -s user mnemopay -- npx -y @mnemopay/sdk mcp
```

Python:

```bash
pip install mnemopay
```

## MCP Tool Groups

MnemoPay has a broad platform catalog, but exposes only the 14-tool
`essentials` group by default.

```bash
npx -y @mnemopay/sdk mcp --tools=essentials
npx -y @mnemopay/sdk mcp --tools=governance,identity,skills
npx -y @mnemopay/sdk mcp --tools=agent_os
```

Never expose `organization_admin`, `operator`, or `all` to an untrusted agent.
Those groups require explicit credentials and should be enabled only for
authorized operators.

## Capabilities

- Persistent memory with decay, reinforcement, and Merkle integrity
- Stripe, Paystack, Lightning, x402, MPP, and AP2 payment rails
- Agent Reputation Scoring and portable KYA identity
- Spend policies, capability tokens, approvals, and emergency stops
- Action ledger, signed receipts, and Article 12 audit bundles
- Governed skills and GridStamp spatial evidence
- Durable hosted browser, coding, computer-use, skill, and brain jobs
- Organization roles, members, invitations, policies, agents, and limits

## Safety Rules

- Require an explicit amount, currency, recipient, and reason before payments.
- Prefer read-only tools until the user clearly requests an action.
- Use approval workflows for high-risk, destructive, or high-value actions.
- Never return API keys, invitation tokens, worker credentials, or secrets.
- Keep admin/operator tools outside the default tool set.

## Links

- Website: https://mnemopay.com
- SDK: https://www.npmjs.com/package/@mnemopay/sdk
- Python: https://pypi.org/project/mnemopay/
- Source: https://github.com/mnemopay/mnemopay-sdk
