## Description:

Habitica (habitica.com). Use this skill for ANY Habitica request — reading, creating, updating, and deleting data. Whenever a task involves Habitica, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Habitica users use the skill to read and manage their tasks and tags through the OOMOL-connected Habitica service, using the oo CLI. Developers and operators can use it to check the supported action schemas before submitting requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup instructs users to run an installer downloaded from the internet without checking it first.

Mitigation: Review the installer source and its installation behavior through a separate process before running it.

Risk: The safety text treats task scoring as read-only even though scoring changes Habitica task state.

Mitigation: Treat scoring as a write and get approval for the specific task, direction, and effect before executing it.

Risk: The OOMOL-mediated Habitica connection may access account credentials and may involve OOMOL billing; the connector implementation is unverified.

Mitigation: Check the connector's permissions and billing implications before connecting or using it.

## Reference(s):

- [Habitica API Usage Guidelines](https://github.com/HabitRPG/habitica/wiki/API-Usage-Guidelines)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Habitica](https://habitica.com)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
