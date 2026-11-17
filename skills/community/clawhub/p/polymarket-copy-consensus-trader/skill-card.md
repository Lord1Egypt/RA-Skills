## Description:

Only trades Polymarket markets where 3+ top whale wallets independently agree on direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to run a Polymarket copy-trading strategy that aggregates recent activity from top public wallets, filters for multi-wallet consensus, and places paper or explicitly enabled live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can trade the wrong market because market matching uses progressive keyword search.

Mitigation: Keep the default paper mode for evaluation and require exact market identity checks before enabling live orders.

Risk: Live trading can exceed expected exposure because position limiting is per run rather than account-wide.

Mitigation: Use a revocable low-limit API key and verify account-wide exposure controls before live use.

Risk: The Simmer SDK dependency is not pinned in the artifact.

Mitigation: Pin and audit simmer-sdk before providing live trading credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-copy-consensus-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk source repository](https://github.com/SpartanLabsXyz/simmer-sdk)
- [predicting.top leaderboard API](https://predicting.top/api/leaderboard)
- [Polymarket data API](https://data-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text and trading actions driven by Python configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading unless --live is passed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
