## Description:

Detects when multiple top-performing Polymarket wallets independently enter the same market in the same direction within a configurable time window and can place conviction-boosted trades when two or more wallets agree.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor Polymarket whale-wallet consensus signals and automate paper or explicitly enabled live trading through Simmer. It is intended for configurable prediction-market trading workflows that require human review before live use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading safeguards can fail or exceed the user's intended limits.

Mitigation: Keep the skill in paper mode unless live trading risk is accepted, use a dedicated low-limit API key, and review behavior before enabling live mode.

Risk: Documented controls for max position, minimum volume, market matching, slippage, or flip-flop checks may not be reliable.

Mitigation: Do not rely on those controls as sole risk limits; independently validate configuration and monitor live executions.

Risk: The external trading SDK affects execution behavior.

Mitigation: Pin and review simmer-sdk before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-whale-momentum-trader)
- [predicting.top leaderboard API](https://predicting.top/api/leaderboard)
- [Polymarket Data API](https://data-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text and trading actions through the configured Simmer venue]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless live mode is explicitly enabled.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
