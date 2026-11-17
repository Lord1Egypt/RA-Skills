## Description:

MNS (Money Never Sleeps) is a CLI operations manual that guides agents through local portfolio ledger review, already-executed trade recording, market sentiment checks, target-weight rebalancing reports, strategy parameter inspection, and backtesting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sopaco](https://clawhub.ai/user/sopaco)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate the MNS CLI for local portfolio bookkeeping, daily or weekly strategy reporting, manual price and configuration workflows, and backtest review. The skill is for recording user-confirmed transactions and explaining rule-based outputs, not for executing broker trades or making investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run an unpinned third-party npm package.

Mitigation: Review the npm package and publisher before installation, prefer a pinned audited version, and run it in an isolated environment when possible.

Risk: The CLI can mutate local financial ledger records, including recording trades and resetting data.

Mitigation: Only record trades or reset data after explicit user confirmation of the real-world transaction or destructive action.

Risk: Rule-based rebalancing reports may be mistaken for investment advice.

Mitigation: Present reports as mechanical calculations, avoid making buy or sell decisions for the user, and preserve the skill's stated limitations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sopaco/skills/money-never-sleep)
- [Project homepage](https://github.com/sopaco/money-never-sleep)
- [OpenClaw source link](https://github.com/sopaco/money-never-sleep)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command-output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should distinguish bookkeeping from investment advice and use command output as the source for portfolio figures.]

## Skill Version(s):

0.6.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
