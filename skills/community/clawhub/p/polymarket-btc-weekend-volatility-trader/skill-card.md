## Description:

Trades BTC weekend price threshold markets on Polymarket by exploiting the systematic gap between first-passage probability and terminal probability, with conviction scaled by entry timing and BTC halving-cycle volatility regime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading developers use this skill to run a paper-by-default Polymarket strategy for BTC weekend threshold markets. It helps an agent discover matching markets, compute signal conviction, apply position limits, and optionally place live trades when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket trades with financial exposure.

Mitigation: Keep the skill in paper mode unless live trading is intentional, and use conservative position and open-position limits before enabling --live.

Risk: SIMMER_API_KEY grants trading authority and is a high-value credential.

Mitigation: Scope and rotate the key where possible, store it only in the runtime secret manager, and remove it from environments that do not need trading access.

Risk: Documented market-window and volume checks may be missing or ineffective.

Mitigation: Review and fix those safeguards before trusting live execution.

Risk: The skill depends on simmer-sdk for market discovery and trade execution.

Mitigation: Pin simmer-sdk to a reviewed version and re-run security review before dependency upgrades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-btc-weekend-volatility-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls]

**Output Format:** [Console text, Python execution commands, environment configuration, and trade API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trading requires the explicit --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
