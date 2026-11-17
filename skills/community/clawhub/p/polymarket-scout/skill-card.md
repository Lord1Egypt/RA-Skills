## Description:

Scan Polymarket hourly crypto markets (BTC/ETH/SOL/XRP) for edge opportunities, counter-consensus setups, freshness windows, and expected value using the Argus strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamierossouw](https://clawhub.ai/user/jamierossouw)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to scan live Polymarket hourly crypto markets for ranked prediction-market edge signals. It supports market review and decision support, but recommendations should be treated as unverified betting or financial guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill produces betting-oriented market signals, edge estimates, win-rate claims, and Kelly sizing.

Mitigation: Require explicit user confirmation before acting on any recommendation and treat all outputs as unverified gambling or financial guidance.

Risk: The skill fetches live Polymarket data and may present time-sensitive opportunities.

Mitigation: Confirm market state, timing, odds, and user intent immediately before any external action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jamierossouw/skills/polymarket-scout)
- [Publisher profile](https://clawhub.ai/user/jamierossouw)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Markdown, Guidance]

**Output Format:** [Markdown with ranked market-signal analysis and sizing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches live Polymarket CLOB and Gamma API data without API keys; outputs should require explicit user confirmation before any betting action.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
