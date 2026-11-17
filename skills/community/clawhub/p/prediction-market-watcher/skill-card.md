## Description:

Monitor, analyze, and trade on Kalshi and Polymarket prediction markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m-lwatcher](https://clawhub.ai/user/m-lwatcher)

### License/Terms of Use:

MIT-0

## Use Case:

Prediction market users and agents use this skill to review Kalshi portfolios, scan markets, check settlement status, and prepare or place trades. It also provides read-only Polymarket reference material for comparing related markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Kalshi credentials to place real-money trades.

Mitigation: Keep the workflow in demo or read-only mode unless explicit human trade confirmation and credential scoping are added.

Risk: Settlement reminders and external messaging can disclose position or market status to unintended recipients.

Mitigation: Review any cron or messaging setup, verify recipients, and remove reminder behavior that is not required.

Risk: Local risk_state.json limits are not a complete spending control.

Mitigation: Use platform or account-level limits and review orders before submission; treat local limits as supplemental.

## Reference(s):

- [Kalshi API Reference](references/kalshi-api.md)
- [Polymarket API Reference](references/polymarket-api.md)
- [Prediction Market Watcher on ClawHub](https://clawhub.ai/m-lwatcher/skills/prediction-market-watcher)
- [m-lwatcher Publisher Profile](https://clawhub.ai/user/m-lwatcher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets, plus text or JSON responses from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Kalshi credentials and local configuration for authenticated portfolio or order workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
