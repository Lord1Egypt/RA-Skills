## Description:

Tracks rolling win rate per whale wallet and only follows wallets on a verified hot streak, dynamically promoting and demoting wallets based on recent performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate Polymarket whale wallets by recent realized win rate and follow only currently hot wallets. It can propose or place Simmer/Polymarket trades, with paper mode as the default and live trading requiring an explicit flag.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place real-money Polymarket orders in unintended markets or exceed the documented position limit.

Mitigation: Keep the skill in paper mode, avoid --live until market matching and portfolio-limit enforcement are reviewed, and use a dedicated low-limit Simmer/Polymarket API key.

Risk: The skill depends on simmer-sdk while handling trading credentials.

Mitigation: Pin or otherwise verify simmer-sdk before supplying credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-whale-streak-trader)
- [predicting.top leaderboard API](https://predicting.top/api/leaderboard)
- [Polymarket data API](https://data-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text with trade reasoning and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless --live is supplied.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
