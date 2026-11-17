## Description:

Automatically discovers and ranks top Polymarket wallets from public leaderboards, evaluates rolling performance, and builds a dynamic copy roster for Simmer SDK copytrading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading automation operators use this skill to discover high-performing Polymarket wallets, rank them by recent performance, and feed a bounded dynamic roster into Simmer SDK copytrading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place real-money Polymarket orders while safeguards are not fully enforced as documented.

Mitigation: Keep the skill in paper mode unless the live-trading risks have been fixed or explicitly accepted.

Risk: A broad Simmer API key could expose more trading authority than this skill needs.

Mitigation: Use a narrowly scoped Simmer API key with account-level spending and trade limits.

Risk: Dependency drift in the Simmer SDK could change trading behavior or error handling.

Mitigation: Pin the SDK version before deployment and retest the configured trading path.

Risk: Market, portfolio, or external data checks can fail or return incomplete information.

Mitigation: Require live execution to fail closed when market data, portfolio context, or safety checks cannot be verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-copy-dynamic-roster-trader)
- [Publisher profile](https://clawhub.ai/user/diagnostikon)
- [Predicting.top leaderboard API](https://predicting.top/api/leaderboard)
- [Polymarket data API](https://data-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Console text, Python execution, environment-variable configuration, and Simmer SDK API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper mode unless live execution is explicitly enabled; requires SIMMER_API_KEY and simmer-sdk.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
