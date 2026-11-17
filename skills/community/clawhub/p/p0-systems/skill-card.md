## Description:

Deploy tokens on Solana, trade on pump.fun and Jupiter, and earn creator fees through P0 APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[serpepe](https://clawhub.ai/user/serpepe)

### License/Terms of Use:


## Use Case:

Developers and external agent builders use this skill to configure P0 API access, deploy Solana tokens, trade through supported venues, manage token earnings, and administer P0 account resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes fund-moving or destructive actions such as swaps, token deployments, fee claims, credit purchases, Pro upgrades, and API-key deletion.

Mitigation: Require explicit human approval before those actions and review the skill before installation.

Risk: The P0_API_KEY grants authenticated access to P0 account and trading endpoints.

Mitigation: Use only a key you are comfortable giving to an agent, and keep it out of logs and source control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/serpepe/skills/p0-systems)
- [P0 agents documentation](https://agents.p0.systems/skill.md)
- [P0 agents homepage](https://agents.p0.systems)
- [P0 API base endpoint](https://api.p0.systems/api/x402)
- [P0 Systems](https://p0.systems)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and HTTP API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a P0_API_KEY environment variable for authenticated P0 API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
