## Description:

Google Chat: Manage Chat spaces and messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to inspect and run Google Chat CLI operations for spaces, messages, custom emojis, media, and user-related Chat resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutating Google Chat operations can delete spaces, delete emojis, update spaces, upload media, or make administrative changes.

Mitigation: Require explicit confirmation before destructive or admin-access operations and review target resources, parameters, and schemas before execution.

Risk: Incorrect parameters can affect the wrong Google Chat space, message, emoji, media item, or user-related resource.

Mitigation: Inspect the method schema with gws schema chat.<resource>.<method> and verify identifiers before building --params or --json flags.

## Reference(s):

- [ClawHub Gws Chat Skill](https://clawhub.ai/googleworkspace-bot/skills/gws-chat)
- [Learn about custom emojis in Google Chat](https://support.google.com/chat/answer/12800149)
- [Manage custom emoji permissions](https://support.google.com/a/answer/12850085)
- [Upload media as a file attachment](https://developers.google.com/workspace/chat/upload-media-attachments)
- [Import data into Google Chat](https://developers.google.com/workspace/chat/import-data)
- [Create a space](https://developers.google.com/workspace/chat/create-spaces)
- [Delete a space](https://developers.google.com/workspace/chat/delete-spaces)
- [Update a space](https://developers.google.com/workspace/chat/update-spaces)
- [Search for and manage spaces](https://developers.google.com/workspace/chat/search-manage-admin)
- [Google Chat app authentication and authorization](https://developers.google.com/workspace/chat/authenticate-authorize-chat-app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command-reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI. The skill directs agents to inspect commands with gws chat --help and schemas with gws schema chat.<resource>.<method> before building parameters.]

## Skill Version(s):

1.0.14 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
