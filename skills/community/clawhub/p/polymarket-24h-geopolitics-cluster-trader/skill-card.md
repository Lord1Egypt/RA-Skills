## Description:

Trades logical inconsistencies in geopolitical event clusters on Polymarket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent discover geopolitical Polymarket clusters, check them for probability consistency issues, and submit paper or explicitly live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live execution can place real-money Polymarket trades when enabled.

Mitigation: Review before installing, keep paper and live runs in separate processes, and require explicit operator approval before using --live.

Risk: SIMMER_API_KEY provides trading authority.

Mitigation: Treat the key as a high-value credential and scope, rotate, and store it according to local secret-management policy.

Risk: Advertised open-position and volume limits may not reliably bound real exposure.

Mitigation: Do not rely on those limits unless the implementation is fixed or limits are enforced server-side.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-24h-geopolitics-cluster-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls, guidance]

**Output Format:** [Text logs, shell command invocation, configuration values, and trading API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live trading requires an explicit --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release metadata; artifact frontmatter says 1.0.0 and clawhub.json says 0.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
