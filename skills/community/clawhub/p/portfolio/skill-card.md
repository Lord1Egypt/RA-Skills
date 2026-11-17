## Description:

Manage investment portfolios. Use when adding positions, analyzing allocation, calculating returns, or generating rebalance advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage local investment portfolio records, review holdings, analyze allocation, calculate returns, and generate rebalance suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and modifies persistent local portfolio data under ~/.portfolio.

Mitigation: Review commands before execution and keep backups of important portfolio data.

Risk: Remove operations can change saved holdings and transaction records.

Mitigation: Confirm ticker symbols and quantities before running remove commands.

Risk: CSV exports may be unsafe if untrusted ticker values are imported before validation and CSV escaping are improved.

Mitigation: Avoid importing untrusted ticker values into CSV exports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/portfolio)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, CSV]

**Output Format:** [Markdown guidance with bash commands and command output in table, JSON, or CSV formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes portfolio holdings and transaction data to local JSON files under ~/.portfolio.]

## Skill Version(s):

3.4.2 (source: server release metadata; artifact frontmatter lists 3.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
