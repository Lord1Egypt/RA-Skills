## Description:

Deep dive on a Hyperliquid perp trader. Identity, open positions, recent trades, and overall PnL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto traders and analysts can use this skill to review a Hyperliquid perpetual trader's labels, open positions, recent trades, PnL, and leaderboard standing using Nansen data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls, including repeated calls in loops, can incur x402 payments from the configured wallet under its existing authorization.

Mitigation: Run `nansen auth status` before the research task and stop if the selected session or authentication state is invalid. Review the wallet payment policy, spending limits, and call count before queries or loops; do not switch to anonymous access after authentication fails.

## Reference(s):

- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)
- [ClawHub skill release](https://clawhub.ai/nansen-devops/skills/nansen-perp-trader-profile)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trader-address specific; lookback and result limits can be selected for applicable queries. Results depend on data available through Nansen.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
