## Description:

Trades structural mispricings in crypto price-threshold markets by reconstructing the implied probability distribution curve across multiple strike levels and detecting mathematical violations such as monotonicity breaks and range-sum inconsistencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to scan Polymarket crypto price-threshold markets for implied-CDF inconsistencies and optionally execute paper or live trades through Simmer. It is intended for advanced users who can review trading risk, configure limits, and monitor execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket trades and should be treated as capable of under-hedged or repeated positions.

Mitigation: Test in paper mode first, require deliberate review before using --live, and use a limited API key for accounts with live trading enabled.

Risk: Documented volume and concurrent-position limits may not be sufficient as hard protections.

Mitigation: Configure conservative tunables, monitor order placement, and apply independent account-level or operational limits before live use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-48h-price-curve-arb-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration]

**Output Format:** [Python script execution with console logs, configurable environment variables, and Simmer trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading unless the --live flag is used; requires SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
