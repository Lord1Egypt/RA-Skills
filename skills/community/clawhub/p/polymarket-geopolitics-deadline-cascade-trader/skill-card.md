## Description:

Trades temporal inconsistencies across geopolitical markets with different deadlines and detects diplomacy-versus-escalation inversions within the same conflict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to scan Polymarket geopolitical markets for deadline-based probability inconsistencies and generate paper or live trading actions through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-trading safeguards can fail and may place real trades or exceed intended limits.

Mitigation: Keep the skill in paper mode until reviewed, use tightly limited credentials, and enforce order-size plus account-wide exposure limits outside the skill.

Risk: The Simmer dependency is declared without a pinned version.

Mitigation: Pin and review the dependency before enabling live trading.

Risk: SIMMER_API_KEY grants trading authority and is a high-value credential.

Mitigation: Use a scoped credential with minimal balances or permissions and rotate it if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-geopolitics-deadline-cascade-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk source repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, API calls, Shell commands, Configuration]

**Output Format:** [Console text with Simmer trade API calls controlled by CLI flags and environment variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require --live and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
