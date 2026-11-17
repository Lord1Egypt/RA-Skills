## Description:

Trades structural mispricings in equity and stock price-threshold markets by reconstructing implied probability curves across strike levels and detecting monotonicity, range-sum, and bin-sum inconsistencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and trading-system developers use this skill to scan Polymarket equity strike-ladder markets, identify internally inconsistent probability curves, and place paper or explicitly enabled live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates Polymarket trading and can place real USDC trades when live mode is enabled.

Mitigation: Keep the default paper-trading mode until reviewed, require explicit --live use for real trading, and apply account-level trading limits.

Risk: Live-trading safeguards and dependency controls need review before use.

Mitigation: Use a tightly limited API key, verify volume and position-limit safeguards, and pin the simmer-sdk dependency before live deployment.

## Reference(s):

- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/)
- [Simmer SDK GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console status text and Simmer trade requests configured by environment variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading unless the --live flag is supplied; requires SIMMER_API_KEY and simmer-sdk.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
