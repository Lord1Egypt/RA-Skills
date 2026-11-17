## Description:

Tracks top Polymarket whale wallets, reports leaderboard and open-position data, and highlights high-conviction market signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[themsquared](https://clawhub.ai/user/themsquared)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a Python-based Polymarket monitoring report for top monthly earners, open positions, recent trades, and consensus signals. The output should be treated as advisory market information, not automated trading execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents trading signals and position recommendations from external market APIs that may be incomplete, stale, or unsuitable for a user's risk profile.

Mitigation: Treat the output as advisory information and require human review before making trading decisions.

Risk: The artifact depends on an unpinned third-party Python package.

Mitigation: Install in a virtual environment and review or pin the dependency before operational use.

Risk: Remote market text is printed to the terminal, including in watch mode.

Mitigation: Avoid terminals that permit risky control-sequence behavior unless remote text is sanitized before display.

Risk: The documentation advertises JSON output for automation, while the reviewed script does not define a JSON CLI option.

Mitigation: Verify the CLI behavior in a test environment before relying on JSON automation workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/themsquared/skills/polymarket-whale-tracker-pro)
- [Polymarket Data API endpoint](https://data-api.polymarket.com)
- [Polymarket Gamma API endpoint](https://gamma-api.polymarket.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Terminal text report with documented JSON mode for automation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes leaderboard, wallet address, watch, and minimum position size modes; watch mode refreshes every five minutes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
