## Description:

Trades marubozu continuation signals on Polymarket 5-minute BTC, ETH, SOL, and XRP interval markets using conviction-based position sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run or adapt a Polymarket crypto interval trading agent that searches for marubozu continuation opportunities and submits paper or live orders through Simmer. It is intended for users who understand prediction-market trading, credential handling, and the financial risk of live execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live and paper mode handling may mislead users and expose them to unintended real trades.

Mitigation: Run only in paper mode in a fresh process and do not enable --live until the client-mode cache issue is fixed and reviewed.

Risk: The required SIMMER_API_KEY is a high-value trading credential.

Mitigation: Use a limited, separate credential and keep autostart disabled until the skill has been tested.

Risk: Risk controls may be incomplete because the security summary calls out minimum-volume enforcement and interval-adjacency validation concerns.

Mitigation: Review and fix those controls before using the skill for live trading.

Risk: Unpinned dependency installation can change trading behavior over time.

Mitigation: Pin and review simmer-sdk before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-candle-marubozu-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, API calls]

**Output Format:** [Python script execution with text logs, tunable configuration, and Simmer trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live trading requires an explicit --live flag and a SIMMER_API_KEY credential.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
