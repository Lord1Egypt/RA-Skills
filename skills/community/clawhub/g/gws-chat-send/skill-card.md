## Description:

Google Chat: Send a message to a space.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to have an agent prepare and run the `gws chat +send` command for sending plain-text messages to a specified Google Chat space, with user confirmation before posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command posts a message to Google Chat, so an incorrect space or message could send content to the wrong audience.

Mitigation: Confirm the selected space and message text with the user before executing the send command.

Risk: The skill depends on the local `gws` CLI and the Google account configuration it uses.

Mitigation: Install and run it only where the `gws` CLI and configured account are trusted for the intended workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-chat-send)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the `gws` CLI and a clearly selected Google Chat space and message text.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
