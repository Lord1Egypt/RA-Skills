## Description:

High-frequency paper trading framework for crypto that uses multi-indicator technical analysis, Kelly-based position sizing, stop-loss management, and a trade ledger for paper trading, backtesting, HFT simulation, or autonomous-agent development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamierossouw](https://clawhub.ai/user/jamierossouw)

### License/Terms of Use:


## Use Case:

External developers and trading-system builders use this skill to guide crypto paper trading, backtesting, watchlist scanning, and autonomous trading-agent workflows without placing real trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paper-trading simulations may be mistaken for real trading guidance or run autonomously across a large watchlist.

Mitigation: Use explicit paper-trading-only prompts, confirm where local portfolio and ledger files will be written, and require confirmation before large watchlist or autonomous runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jamierossouw/skills/hft-paper-trader)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Files]

**Output Format:** [Markdown guidance with optional JSON, CSV, and Markdown state-file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paper-trading state may include PORTFOLIO.json, LEDGER.csv, and lessons.md.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
