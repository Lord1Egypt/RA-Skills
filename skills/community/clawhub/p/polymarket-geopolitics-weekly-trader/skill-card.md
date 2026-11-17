## Description:

Trades weekly cyclical patterns in geopolitical prediction markets using day-of-week timing and conviction-based sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators can use this skill as a configurable Polymarket geopolitics trading template. It defaults to paper trading and can place live orders only when explicitly run with the live flag.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When run with --live, the skill can place real Polymarket orders, and evidence.security reports that some advertised live-trading safeguards are not reliably enforced.

Mitigation: Use paper mode first, review and test the safeguards before live use, keep position-size tunables conservative, and only enable --live after operational approval.

Risk: SIMMER_API_KEY grants trading authority and should be treated as a high-value credential.

Mitigation: Store the key in a managed secret store, avoid sharing it in prompts or logs, and use a least-privilege key if Simmer supports one.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-geopolitics-weekly-trader)
- [simmer-sdk PyPI package](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls]

**Output Format:** [Plain text logs, command-line execution, environment configuration, and Simmer SDK trading calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require the --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
