## Description:

Google Workflow: Announce a Drive file in a Chat space.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Google Workspace operators use this skill to prepare the gws command and required inputs for announcing a Google Drive file in a Google Chat space.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command reads a Drive file name and posts a message to a user-specified Chat space.

Mitigation: Install only for users who intend to grant the gws CLI the needed Google Workspace permissions, and verify the file ID, Chat space, and message before execution.

Risk: Authentication and global security behavior are defined in a referenced shared gws skill.

Mitigation: Review the shared gws auth and security instructions from the same publisher before using this workflow.

## Reference(s):

- [Gws Workflow File Announce on ClawHub](https://clawhub.ai/googleworkspace-bot/skills/gws-workflow-file-announce)
- [gws-shared auth and global flags](../gws-shared/SKILL.md)
- [gws-workflow command collection](../gws-workflow/SKILL.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and Google Workspace authorization; the described command sends a Chat message to the specified space.]

## Skill Version(s):

1.0.12 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
