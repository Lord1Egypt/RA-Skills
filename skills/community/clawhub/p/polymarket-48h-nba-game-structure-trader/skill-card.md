## Description:

Trades structural inconsistencies across correlated NBA game markets on Polymarket by grouping moneyline, spread, full-game and first-half over/under, and first-half moneyline markets for the same game.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to scan Polymarket NBA game markets for cross-market structural inconsistencies and optionally place simulated or live trades through Simmer. The skill is intended for users who can assess trading risk and configure least-privilege market access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live Polymarket trades when explicitly run in live mode, and scanner evidence says some advertised live-trading safeguards are not actually enforced.

Mitigation: Use paper mode first, grant only a least-privilege Simmer/Polymarket key, and enforce account-side spending limits before any live deployment.

Risk: The required SIMMER_API_KEY has trading authority.

Mitigation: Store the key securely, scope it to the minimum permissions available, and rotate or revoke it if the execution environment is shared or compromised.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-48h-nba-game-structure-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text with trading decisions and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to simulated trading unless run with the live flag.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
