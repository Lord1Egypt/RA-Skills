## Description:

Track investments with buy/sell records, allocation charts, and P/L analysis. Use when managing a stock or crypto portfolio, rebalancing, or comparing assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage locally stored stock or crypto portfolio records, review allocation and performance, calculate DCA and dividend figures, and generate rebalance suggestions from manually entered prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted input to the DCA command can execute unintended shell commands.

Mitigation: Review before installing and pass only trusted numeric values to the DCA command.

Risk: Exported CSV data may be unsafe to open in spreadsheet software when ticker values are untrusted.

Mitigation: Avoid opening exported CSV files in spreadsheet software unless ticker inputs are trusted.

Risk: Holdings and transaction history are stored persistently in a home-directory folder and can be removed or overwritten without recovery.

Mitigation: Use a deliberate PORTFOLIO_DIR location and keep backups for portfolio records that must be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/investment-portfolio)
- [Publisher homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Terminal text with ASCII charts, CSV or JSON exports, and local JSONL records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses manually entered prices and persists holdings and transaction history under the configured portfolio directory.]

## Skill Version(s):

4.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
