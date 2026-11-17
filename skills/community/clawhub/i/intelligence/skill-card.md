## Description:

Intelligence helps agents retrieve and explain live ranked alpha scans and single-pair trading setups across Hyperliquid alts and HIP-3 markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and developers use this skill to ask an agent for live market scans, single-pair setup analysis, and guarded backtest or deployment handoffs for Superior Trade workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live trading deployment through a third-party service.

Mitigation: Require explicit user confirmation before any deployment step, run setup and backtesting first, and present the relevant AI Critic concerns before recommending action.

Risk: Wallet credential handling is ambiguous and could expose withdrawal-capable credentials.

Mitigation: Do not request or transmit seed phrases, master private keys, or withdrawal-capable wallet credentials; use only limited credentials after a separate final confirmation.

Risk: Market rankings and prices are live and can become stale or misleading if substituted with model knowledge.

Mitigation: Use the live Intelligence API responses, show computed timestamps and snapshot fields, and avoid fabricating or reweighting rankings.

## Reference(s):

- [Intelligence](https://account.superior.trade/intelligence)
- [Superior Trade API](https://api.superior.trade)
- [Intelligence API](references/api.md)
- [The Four Buckets](references/buckets.md)
- [Intelligence workflows](references/workflow.md)
- [Glossary](references/glossary.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request details, ranked setup summaries, tables, and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live server responses when available and should preserve engine-selected bucket, timeframe, score, and snapshot fields.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
