## Description:

Enforces monotonicity constraints on crypto price-level markets on Kalshi and trades violations by buying underpriced lower-threshold contracts and selling overpriced higher-threshold ones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use this skill to monitor Kalshi BTC and ETH price-level markets for monotonicity violations and propose or execute paired trades. It defaults to dry-run behavior, with live financial execution only when explicitly invoked with --live.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can make real financial changes, including buying paired positions and selling existing BTC/ETH-related positions.

Mitigation: Run in dry-run mode first, require an explicit --live decision for execution, and review expected trades before providing live authority.

Risk: The skill requires high-value trading and wallet credentials.

Mitigation: Use tightly limited credentials and a dedicated low-balance wallet; do not expose SOLANA_PRIVATE_KEY for dry-run use.

Risk: The runtime depends on simmer-sdk without an evidence-pinned version.

Mitigation: Review and pin the exact simmer-sdk version before installation or live execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-crypto-monotonicity-trader)
- [Simmer Markets skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk source repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Shell commands, Configuration]

**Output Format:** [Terminal text with optional JSON automaton report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; --live permits real trades using configured credentials.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
