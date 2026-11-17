## Description:

Atomic node skill to delete an email via Gmail using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to move a specified Gmail message to trash through the gog CLI, with retries and error reporting when deletion fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move Gmail messages to trash from broad instructions without requiring explicit confirmation.

Mitigation: Use it only where the agent confirms the exact Gmail message before running the trash command.

Risk: The gog CLI may act on whichever Gmail account is authenticated.

Mitigation: Ensure gog is authenticated only to the Gmail account intended for management before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zvirb/skills/gmail-delete-email)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI and a Gmail message ID.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
