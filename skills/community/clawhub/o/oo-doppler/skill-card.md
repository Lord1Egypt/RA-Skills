## Description:

Doppler (doppler.com). Use this skill for ANY Doppler request — reading, creating, updating, and deleting data. Whenever a task involves Doppler, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to manage Doppler projects, environments, configs, secrets, integrations, and change requests through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute unverified downloads.

Mitigation: Review and approve a fixed CLI release before installation.

Risk: The CLI may synchronize additional agent skills during startup.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before use, or review synchronized skills before relying on them.

Risk: Doppler actions can access and return secrets.

Mitigation: Connect a narrowly scoped Doppler key and handle returned secrets carefully.

## Reference(s):

- [Doppler](https://www.doppler.com)
- [Doppler API documentation](https://docs.doppler.com/reference/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON action results and concise text, with shell commands shown in Markdown code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs follow the live action schema. Results may include secret values.]

## Skill Version(s):

1.0.6 (source: release evidence metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
