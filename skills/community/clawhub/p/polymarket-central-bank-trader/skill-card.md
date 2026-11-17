## Description:

Trades Polymarket prediction markets on central bank decisions, interest rates, inflation prints, and Fed/ECB/Riksbank policy moves using keyword-based market discovery, conviction sizing, and central-bank cycle biasing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to discover central-bank and monetary-policy prediction markets, compute trade signals, and run paper or live Polymarket trading through Simmer. It is intended for configured trading workflows where the operator supplies credentials and risk limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading controls are under-scoped for a funded Polymarket account.

Mitigation: Keep the skill in paper mode until the dependency is pinned and the volume, exposure, and classification safeguards are fixed.

Risk: Trading authority depends on a high-value SIMMER_API_KEY credential.

Mitigation: Use a tightly permissioned API key and avoid running the skill on a funded account without external account-level limits.

Risk: Some documented safeguards are not actually enforced.

Mitigation: Review the skill carefully before installing and require independent limits before enabling live trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-central-bank-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, API calls, Configuration]

**Output Format:** [Plain text console logs with Simmer or Polymarket trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading unless live execution is explicitly enabled; requires SIMMER_API_KEY and configurable risk tunables.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
