## Description:

Trade Agent helps an assistant analyze gold and forex markets, provide trading signals, risk assessment, and position suggestions, and handle AIUSD account actions such as balances, trades, staking, withdrawals, gas top-ups, and transaction history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeman88-tch](https://clawhub.ai/user/freeman88-tch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect a personal assistant to AIUSD account workflows for balances, trading, staking, withdrawals, gas top-ups, and transaction history, with market-analysis guidance for gold and forex trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can request high-impact financial actions including trades, withdrawals, staking changes, gas top-ups, and credential resets.

Mitigation: Require explicit user review and confirmation before executing financial actions or resetting credentials.

Risk: Local authentication uses bearer tokens and cached credentials.

Mitigation: Protect and scope tokens, avoid production wallet credentials during review, and use a sandbox or low-risk account for first use.

Risk: Installer files execute local code and may replace an existing aiusd-skill directory.

Mitigation: Review the decoded package before installation and back up any existing aiusd-skill directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/freeman88-tch/skills/lobster-trade-agent)
- [Publisher Profile](https://clawhub.ai/user/freeman88-tch)
- [AIUSD Website](https://aiusd.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with tool-call results and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live tool schema lookup before account actions and may trigger OAuth re-authentication.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, frontmatter, and build-info; artifact _meta.json lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
