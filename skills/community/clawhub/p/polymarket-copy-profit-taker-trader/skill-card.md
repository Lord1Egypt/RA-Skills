## Description:

Detects when top whale wallets start taking profits by reducing winning positions, then identifies what markets they rotate INTO.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to monitor Polymarket whale wallets for take-profit behavior, identify rotation targets, and generate paper-by-default or explicitly live trade actions through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-trading controls and rotation logic may not match the safety claims users would rely on.

Mitigation: Review the trading behavior before use and keep the skill in paper mode until the SDK is pinned and audited and the rotation-window issue is fixed.

Risk: Live orders may proceed when portfolio position checks cannot be verified.

Mitigation: Require live trading to fail closed when position checks fail, and use low account limits while testing.

Risk: The skill requires a SIMMER_API_KEY for trading access.

Mitigation: Use a tightly scoped, revocable SIMMER_API_KEY and rotate or revoke it if unexpected behavior is observed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-copy-profit-taker-trader)
- [Publisher profile](https://clawhub.ai/user/diagnostikon)
- [Predicting.top leaderboard API](https://predicting.top/api/leaderboard)
- [Polymarket data API](https://data-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Console text and agent guidance with trade signals, dashboard summaries, configuration requirements, and executable Python behavior.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires simmer-sdk and SIMMER_API_KEY; defaults to paper trading unless run with an explicit live flag.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
