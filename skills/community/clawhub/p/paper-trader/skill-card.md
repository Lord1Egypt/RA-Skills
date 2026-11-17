## Description:

Run a structured paper-trading loop with SQLite-backed event logging, position tracking, and PnL review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brs999](https://clawhub.ai/user/brs999)

### License/Terms of Use:


## Use Case:

External users and developers use Paper Trader to track simulated trades, journal trade theses, review open positions, and summarize realized and unrealized PnL before committing live capital.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores simulated trading records and notes locally in SQLite under ~/.openclaw unless a different database path is provided.

Mitigation: Use --db to choose an appropriate local database path and apply normal local file access controls for trading notes.

Risk: The skill does not place real trades or fetch market data automatically, so stale or user-entered prices can make PnL output misleading.

Mitigation: Provide current prices explicitly, keep snapshots updated for open positions, and treat output as a paper-trading journal rather than financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brs999/skills/paper-trader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite database under ~/.openclaw by default unless --db is provided.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
