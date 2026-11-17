## Description:

Polymarket Whale Alert monitors the past 24 hours of large Polymarket orders from smart-money trader profiles and formats the results for whale-alert style queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnica](https://clawhub.ai/user/cnica)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to request one-time snapshots of recent large Polymarket orders, including smart-money labels, market links, wallet links, order size, price, win rate, PnL, and timestamp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback behavior may broaden results or show unverified wallets during data outages, which can mislead users relying on whale or smart-money signals.

Mitigation: Treat unclassified results as diagnostics, confirm the threshold used in the output, and review wallet classifications before relying on the report.

## Reference(s):

- [Predictradar Polymarket data-layer MCP examples](https://github.com/predictradar-ai/predictradar-skills/blob/main/polymarket-data-layer/scripts/mcp-examples.js)
- [ClawHub skill page](https://clawhub.ai/cnica/skills/polymarket-predictradar-whale-alert-skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with clickable market and wallet links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One-time live-data snapshot for the previous 24 hours, subject to data availability and configured smart-money thresholds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
