## Description:

Agora (agora.io). Use this skill for ANY Agora request — reading, creating, updating, and deleting data. Whenever a task involves Agora, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use the connected Agora account to inspect projects and usage, create projects, and manage project status or certificates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote CLI installer and connector implementations have not been verified, and setup may synchronize other agent skills into the environment.

Mitigation: Review the installer and connector behavior before use; consider disabling skill synchronization and keep the agent environment limited to reviewed skills.

Risk: A connected Agora account may have permissions broader than an individual task requires.

Mitigation: Use an account with only the needed permissions and retain the skill's approval requirements for project and certificate changes.

## Reference(s):

- [Agora](https://www.agora.io)
- [Agora REST API authentication documentation](https://docs.agora.io/en/signaling/rest-api/restful-authentication)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Agora skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-agora)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Command-line instructions with JSON request payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the connected Agora account; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
