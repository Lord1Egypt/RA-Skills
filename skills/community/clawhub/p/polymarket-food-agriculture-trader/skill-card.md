## Description:

Trades Polymarket prediction markets on food commodity prices, crop yields, drought-driven supply shocks, alternative protein milestones, and agricultural policy events using USDA WASDE calendar timing, commodity concentration signals, and crop season windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover and trade food and agriculture prediction markets on Polymarket. It supports paper trading by default and can place live orders only when explicitly run with live mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket orders using USDC.

Mitigation: Run in paper mode by default, require explicit live-mode activation for real orders, keep live limits low, and use a tightly scoped SIMMER_API_KEY.

Risk: Risk controls may not fully match the documented minimum-volume or maximum-position safeguards.

Mitigation: Review settings before live use and do not rely on documented volume or position safeguards until they are fixed and tested.

Risk: The skill depends on an external trading SDK and a high-value API credential.

Mitigation: Pin and review the simmer-sdk dependency before deployment and rotate or scope the SIMMER_API_KEY used by the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-food-agriculture-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls]

**Output Format:** [Console status output and trading API calls configured by environment variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and the simmer-sdk dependency; tunables control position size, market volume, spread, days to resolution, concurrent positions, thresholds, and minimum trade size.]

## Skill Version(s):

0.0.3 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
