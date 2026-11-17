## Description:

Operate Chatwork by reading rooms, messages, contacts, and tasks, and by creating, updating, or deleting messages and tasks through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents working in Chatwork can use this skill to inspect rooms, members, messages, contacts, and tasks, and to manage messages and tasks through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run remote installer code that has not been verified and may introduce broader agent changes that the skill does not explain.

Mitigation: Review setup before enabling the skill, install a verified CLI release, and review or disable automatic skill synchronization using the publisher's controls.

Risk: Chatwork requests use OOMOL-managed credentials, and write or delete actions can change shared Chatwork data.

Mitigation: Connect Chatwork intentionally and retain approval for posting, editing, creating or updating tasks, and deleting messages; confirm the target and payload before execution.

## Reference(s):

- [Chatwork skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-chatwork)
- [Chatwork](https://go.chatwork.com)
- [Chatwork API documentation](https://developer.chatwork.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON action results with natural-language summaries or instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Chatwork action; obtain approval before actions that create, change, or delete data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
