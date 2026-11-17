## Description:

Scan Simmer markets for a configurable fair-value edge and buy YES or NO when the market price diverges enough from your thesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skybinjf](https://clawhub.ai/user/skybinjf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and prediction-market operators use this skill as a configurable Simmer trading template that scans markets, compares market prices to a user-supplied fair probability, and trades when the configured edge threshold is met.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change financial account state through automatic redemption even when users may expect dry-run behavior.

Mitigation: Review redemption behavior before installation, use a limited-scope Simmer API key, and gate redemption separately from dry-run trading where possible.

Risk: Live mode can place prediction-market trades based on configured fair-value assumptions.

Mitigation: Keep dry-run mode as the default, enable live trading only after strategy review, and configure conservative market, edge, sizing, and slippage limits.

Risk: Unpinned dependencies or publishing tooling can change behavior in automated environments.

Mitigation: Pin the Simmer SDK dependency and ClawHub CLI version before publishing or deploying this skill in automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skybinjf/skills/prediction-fair-value-template)
- [ClawHub publisher profile](https://clawhub.ai/user/skybinjf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation, Python code, JSON configuration, and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run is the documented default; live trading requires explicit enablement.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
