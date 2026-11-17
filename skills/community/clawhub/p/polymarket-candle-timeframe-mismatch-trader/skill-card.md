## Description:

Multi-timeframe analysis for crypto Up or Down markets on Polymarket that detects when 5-minute candle consensus diverges from the hourly market and trades convergence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading automation users use this skill to run or adapt a Polymarket crypto Up or Down strategy that compares short-interval candle consensus with hourly market pricing. The skill defaults to paper trading and requires deliberate live-mode use before placing real trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place real Polymarket orders and the documented controls may not fully match the implemented safeguards.

Mitigation: Review the skill before installation, keep it in paper mode by default, and enable live mode only after confirming the risk controls against the current implementation.

Risk: Credential exposure or over-permissioning could expand financial impact because the skill requires SIMMER_API_KEY.

Mitigation: Use a restricted API key and keep live balances and venue-side limits low.

Risk: Unpinned runtime dependencies can change trading behavior after release.

Mitigation: Pin and review the simmer-sdk dependency before live use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/polymarket-candle-timeframe-mismatch-trader)
- [Publisher Profile](https://clawhub.ai/user/diagnostikon)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and the simmer-sdk dependency; live trading is controlled by an explicit live flag.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
