## Description:

Trades gap-fill reversions on Polymarket 5-minute crypto interval markets by detecting contradictory strong signals across consecutive intervals and sizing positions by gap magnitude.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to identify gap-fill reversion opportunities in Polymarket 5-minute crypto interval markets and place paper or explicitly live trades through Simmer. It is intended for configurable automated trading workflows that require clear thresholds, position sizing, and execution-mode controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live execution can place real Polymarket trades, and the server security review warns that liquidity and total exposure limits may be weaker than documented.

Mitigation: Run in paper mode by default, avoid --live until reviewed, and add or verify server-side or account-wide position and exposure limits before funding live use.

Risk: SIMMER_API_KEY grants trading authority and can expose funded accounts if over-permissioned.

Mitigation: Use the smallest practical balance and permissions for the credential, rotate it if exposed, and keep it out of logs and shared artifacts.

Risk: The skill depends on simmer-sdk for market access and trade execution behavior.

Mitigation: Pin and review the simmer-sdk dependency before live deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-candle-gap-fill-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls]

**Output Format:** [Console status text with configurable environment variables and trade API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trading requires an explicit --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
