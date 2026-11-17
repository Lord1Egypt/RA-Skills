## Description:

Detects coordinated Polymarket whale wallet exits and fades suspected panic-driven price overshoots by buying into qualifying dips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor public Polymarket and leaderboard activity, identify possible coordinated whale exits, and create fade-trade decisions. It runs in paper mode by default and can place live Polymarket trades only when explicitly launched with live trading enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real Polymarket trades when live trading is explicitly enabled.

Mitigation: Use paper mode unless real trades are intended, and enforce account-side spending and trading limits before live use.

Risk: Server security review says live-trading safeguards and dependency controls are weak.

Mitigation: Review the code and SDK provenance before installation, and do not rely on documented volume, open-position, slippage, or flip-flop controls without fixing or independently enforcing them.

Risk: The skill requires an API key for operation.

Mitigation: Use a dedicated least-privilege API key and rotate it if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-whale-exit-fade-trader)
- [predicting.top leaderboard API](https://predicting.top/api/leaderboard)
- [Polymarket data API](https://data-api.polymarket.com)

## Skill Output:

**Output Type(s):** [Text, API Calls, Configuration]

**Output Format:** [Plain text run logs and Simmer SDK trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; paper trading is the default unless live trading is explicitly enabled.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
