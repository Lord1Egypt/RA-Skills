## Description:

Process Street (process.st). Use this skill for ANY Process Street request — reading, creating, and updating data. Whenever a task involves Process Street, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to read and manage Process Street workflows and workflow runs through their connected account, including creating runs and updating form fields or task status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute unverified remote installer code, and the CLI may make broader changes to installed agent skills.

Mitigation: Review and install the CLI separately before setup, consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1, and retain user confirmation for write actions.

## Reference(s):

- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Process Street](https://www.process.st/)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and shell commands, with results summarized as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the oo CLI; action payloads follow the live connector schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
