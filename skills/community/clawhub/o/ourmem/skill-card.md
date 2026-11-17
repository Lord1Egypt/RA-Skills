## Description:

ourmem gives AI agents shared persistent memory across sessions, devices, agents, and teams, available as a hosted or self-deployed service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhyyz](https://clawhub.ai/user/yhyyz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to set up and operate persistent agent memory, including hosted or self-hosted deployment, memory storage and search, imports, sharing through Spaces, analytics, and platform-specific plugin configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles credentials for hosted or self-hosted memory services.

Mitigation: Use trusted endpoints, treat API keys as secrets, avoid showing full keys in chat, and verify authentication before storing memories.

Risk: Memory import and sharing workflows can expose or propagate user data with too much automatic authority.

Mitigation: Preview files before import, confirm the intended recipient or Space before sharing, and avoid using another user's API key as a sharing identifier.

Risk: Installation paths may run packages, Docker images, release binaries, or workspace configuration edits.

Mitigation: Pin or verify packages, Docker images, and release binaries before execution, and review configuration changes before restart.

## Reference(s):

- [ourmem API Quick Reference](references/api-quick-ref.md)
- [ourmem Hosted Setup Guide](references/hosted-setup.md)
- [ourmem Self-Hosted Setup Guide](references/selfhost-setup.md)
- [ourmem ClawHub skill page](https://clawhub.ai/yhyyz/skills/ourmem)
- [ourmem hosted API](https://api.ourmem.ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose installing packages, editing agent configuration files, calling hosted or self-hosted APIs, importing local files, and verifying memory round trips.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
