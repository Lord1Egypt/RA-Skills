## Description:

Trades Polymarket prediction markets on geopolitical events such as wars, ceasefires, sanctions, diplomatic breakthroughs, and regime changes using keyword discovery, conviction-based sizing, and geopolitical bias adjustments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run or adapt a Polymarket trading agent for geopolitical prediction markets. It can identify candidate markets, compute trade direction and size, and execute simulated trades by default or live trades when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket trades and create financial loss.

Mitigation: Keep the skill in paper mode unless live trading is intentional, and use only a limited Simmer/Polymarket credential.

Risk: Documented financial safeguards may not match or be fully enforced by the artifact.

Mitigation: Correct and test the volume, spread, resolution-date, position-count, and max-position safeguards before relying on the skill for live trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-geopolitics-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text and agent guidance with configurable environment variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and the simmer-sdk Python package; paper trading is the default mode.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
