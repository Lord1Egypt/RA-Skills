## Description:

Detects harami candlestick patterns on Polymarket crypto 5-minute interval markets for BTC, ETH, SOL, and XRP and sizes reversal trades by conviction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to scan Polymarket crypto interval markets for harami reversal setups, then run paper trades by default or live trades only when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-trading safety limits are incomplete and can fail open.

Mitigation: Use paper trading first, enable live mode only after review, and do not use real funds until fail-open checks, volume enforcement, open-position accounting, and dependency pinning are fixed.

Risk: The skill requires a trading API key with financial authority.

Mitigation: Use a least-privilege trading key, keep it secret, and set external account-level limits where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-candle-harami-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Markdown guidance, Python execution logs, and trade API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paper trading is the default; live trading requires an explicit --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
