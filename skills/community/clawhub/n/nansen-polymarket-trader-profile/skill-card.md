## Description:

What is a Polymarket trader betting on? Trades by address, PnL breakdown, and market context. Use when analysing a specific Polymarket wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to inspect a specific Polymarket wallet's trade history, profit and loss, and market context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls, including calls in loops, can spend funds through the configured wallet when an eligible x402 payment challenge occurs.

Mitigation: Review the intended calls and applicable wallet spending limits before running research, especially in loops.

Risk: Profit and loss can combine resolved and unresolved markets, so the figures may not represent realized outcomes alone.

Mitigation: Check each market's resolution status and distinguish realized results from unresolved positions when interpreting performance.

## Reference(s):

- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)
- [ClawHub skill release](https://clawhub.ai/nansen-devops/skills/nansen-polymarket-trader-profile)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands]

**Output Format:** [Text analysis based on structured CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Wallet-address-specific trade and PnL context]

## Skill Version(s):

0.1.3 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
