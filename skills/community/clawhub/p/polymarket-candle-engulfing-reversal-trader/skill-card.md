## Description:

Detects engulfing reversal patterns in crypto 5-minute interval markets on Polymarket for BTC, ETH, SOL, and XRP, using conviction-based sizing for post-engulfing continuation trades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External trading agents and developers use this skill to monitor Polymarket crypto interval markets, identify engulfing reversal setups, and submit simulated or explicit live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket trades using a Simmer/Polymarket trading key, and the security review notes that advertised limits are not complete live-trading safeguards.

Mitigation: Keep the skill in paper mode unless the strategy and limits have been reviewed, use the smallest practical API permissions and balances, and set conservative trading tunables.

Risk: Trading behavior depends on the external simmer-sdk package.

Mitigation: Pin or review the SDK version before live use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-candle-engulfing-reversal-trader)
- [simmer-sdk PyPI package](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls]

**Output Format:** [Plain text console logs and Simmer trade API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trading requires an explicit --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release evidence; artifact frontmatter metadata reports 1.0.0 and clawhub.json reports 0.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
