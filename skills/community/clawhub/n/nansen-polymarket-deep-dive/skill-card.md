## Description:

Deep dive on a Polymarket market — OHLCV, orderbook, top holders, positions, trades, and PnL leaderboard. Use when analysing a specific prediction market.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts use this skill to examine a specific Polymarket market through its price and volume history, order book, holders, positions, trades, and profit-and-loss leaderboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls can trigger x402 payments from the configured wallet, and each call in a loop may incur a payment.

Mitigation: Use only an explicitly authorized wallet with an appropriate payment policy and spending limits; account for costs before running calls or loops.

Risk: A selected API key or browser session may be invalid or unable to renew, blocking authenticated research.

Mitigation: Check `nansen auth status` before research and stop after an authentication or renewal failure; do not switch to anonymous access to retry.

## Reference(s):

- [Nansen Polymarket Deep Dive on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-polymarket-deep-dive)
- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Guidance]

**Output Format:** [Markdown with shell command examples and market data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market research uses a numeric market ID and requires a selected API key or saved browser session.]

## Skill Version(s):

0.1.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
