## Description:

Wallet profiler — balance, PnL, labels, transactions, counterparties, related wallets, batch, trace, compare. Use when analysing a specific wallet address or comparing wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Blockchain analysts and developers use this skill to inspect a wallet's balances, performance, labels, transaction history, and relationships, or to batch and compare wallet profiles across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supported x402 challenges can incur payment from the configured wallet, and repeated or trace calls can multiply the cost.

Mitigation: Check the wallet's authorization, payment policy, and spending limits before research; keep trace width and loop size conservative and account for the expected number of calls.

## Reference(s):

- [Nansen Wallet Profiler on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-wallet-profiler)
- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration instructions, Text, Markdown]

**Output Format:** [Wallet research results as text, Markdown tables, JSON, or CSV, with shell command and authentication guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected wallet address, chain, lookback period, and requested fields; trace and batch operations can make multiple API calls.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
