## Description:

Manage Google Meet conferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Workspace admins, developers, and support agents use this skill to inspect Google Meet resources and prepare gws CLI commands for conference records, participants, recordings, smart notes, transcripts, and meeting spaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on the external gws CLI, so commands run with the user's configured Google Workspace authentication and permissions.

Mitigation: Confirm the gws CLI installation, account, scopes, and shared gws authentication guidance before executing Meet operations.

Risk: Meet operations may read or modify conference records, meeting spaces, recordings, transcripts, and related meeting data.

Mitigation: Inspect each method with gws schema and review proposed parameters before running commands against production Google Workspace data.

## Reference(s):

- [Gws Meet ClawHub Skill](https://clawhub.ai/googleworkspace-bot/skills/gws-meet)
- [googleworkspace-bot Publisher Profile](https://clawhub.ai/user/googleworkspace-bot)
- [Google Meet API: End Active Conference](https://developers.google.com/workspace/meet/api/guides/meeting-spaces#end-active-conference)
- [Google Meet API: Get a Meeting Space](https://developers.google.com/workspace/meet/api/guides/meeting-spaces#get-meeting-space)
- [Google Meet API: Update a Meeting Space](https://developers.google.com/workspace/meet/api/guides/meeting-spaces#update-meeting-space)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands rely on the external gws CLI and the user's configured Google Workspace permissions.]

## Skill Version(s):

1.0.13 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
