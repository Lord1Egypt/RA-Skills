## Description:

Trades crypto "Up or Down" 5-minute interval markets on Polymarket by detecting Three White Soldiers and Three Black Crows continuation patterns, then sizes simulated or live trades from the lag distance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run or adapt an automated Polymarket strategy for crypto 5-minute interval markets. The skill discovers candidate markets, detects Three White Soldiers or Three Black Crows patterns, and can place simulated trades by default or live Polymarket trades when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money Polymarket trades with USDC exposure.

Mitigation: Keep the default paper-trading mode unless live trading is intentional, and externally limit the API key or account funds before enabling live mode.

Risk: Some advertised risk tunables may not reliably cap liquidity, resolution horizon, or total open positions.

Mitigation: Review configured limits and monitor account-level exposure outside the skill before relying on live execution.

Risk: SIMMER_API_KEY grants trading authority.

Mitigation: Store the key only in the runtime secret store, rotate it if exposed, and avoid granting more funding or permissions than the strategy needs.

## Reference(s):

- [Skill page](https://clawhub.ai/diagnostikon/skills/polymarket-candle-three-soldiers-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls]

**Output Format:** [Console logs and trade API calls driven by Python configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading unless live mode is explicitly enabled.]

## Skill Version(s):

0.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
