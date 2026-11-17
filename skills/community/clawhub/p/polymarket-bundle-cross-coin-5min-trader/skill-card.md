## Description:

Trades cross-coin divergence in 5-minute crypto Up/Down bundles on Polymarket, sizing mean-reversion positions by divergence magnitude.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to identify cross-coin divergence across 5-minute crypto Up/Down markets on Polymarket and run simulated or explicit live mean-reversion trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that some advertised live-trading safeguards are not actually enforced and that the trading SDK install is unpinned.

Mitigation: Use paper mode first, use a limited API key, review the unpinned SDK risk, and independently enforce volume or concurrent-position limits before live use.

Risk: The artifact can place real Polymarket trades when run with --live.

Mitigation: Run without --live unless intentional live execution is approved, and use credentials with limited trading authority.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-bundle-cross-coin-5min-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, API Calls]

**Output Format:** [Plain text logs, Python execution, configuration values, and optional trading API actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to simulated trading and uses live Polymarket execution only when run with --live.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
