## Description:

Weights copytrading by portfolio concentration -- a whale committing 30% of capital to one market signals far more conviction than 2% spread across many. Copies high-concentration positions with proportionally boosted sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze Polymarket whale portfolios, identify high-concentration positions, and paper-trade or explicitly live-trade conviction-weighted copy signals with configurable safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place real Polymarket orders, and server evidence reports that live-trading safeguards can fail open.

Mitigation: Keep paper mode unless live trading is intentional and understood; use a tightly scoped SIMMER_API_KEY with server-side spending and position limits.

Risk: The sensitive trading dependency is not pinned.

Mitigation: Prefer or require a release that pins simmer-sdk before using live mode.

Risk: Portfolio state may not be verified before trading.

Mitigation: Prefer behavior that fails closed when portfolio state cannot be verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-copy-size-conviction-trader)
- [predicting.top leaderboard API](https://predicting.top/api/leaderboard)
- [Polymarket data API](https://data-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Console text with optional trade API requests and configuration through environment variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper mode unless run with --live.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
