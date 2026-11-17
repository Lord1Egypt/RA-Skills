## Description:

Who is this wallet and what have they been doing? Identity labels, balance, PnL summary, recent transactions, perp positions, and counterparties.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to investigate a blockchain wallet's identity labels, balances, profit and loss, recent transactions, perpetual positions, and counterparties using Nansen data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses and research queries are shared with Nansen when the skill makes research requests.

Mitigation: Use only wallet addresses and queries you are comfortable sharing with Nansen under the selected account.

Risk: A supported HTTP 402 challenge during authenticated research can spend funds from the configured wallet, and repeated calls can incur repeated payments.

Mitigation: Review the applicable payment policy and spending limits before research calls or loops, and proceed only when the user has authorized the potential spend.

## Reference(s):

- [Browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)
- [ClawHub skill release](https://clawhub.ai/nansen-devops/skills/nansen-wallet-deep-dive)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Wallet research summary based on Nansen profiler results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected wallet address, chain, and time window; perpetual positions are Hyperliquid data and may be empty.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
