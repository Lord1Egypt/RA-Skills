## Description:

Manage Google Keep notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Google Workspace users use this skill to let an agent inspect Google Keep commands and prepare Google Workspace CLI operations for notes, attachments, and note permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents using this skill can access and modify Google Keep notes through configured gws credentials.

Mitigation: Install only where the agent is allowed to use those credentials, and review generated commands before execution.

Risk: Deleting a Keep note is immediate and irreversible and can remove collaborator access.

Mitigation: Require explicit confirmation before delete operations and verify the caller has the intended OWNER role.

Risk: Permission operations can change access to notes.

Mitigation: Review permission changes before execution, especially when collaborators or shared notes are involved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-keep)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and configured Google Workspace credentials.]

## Skill Version(s):

1.0.12 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
