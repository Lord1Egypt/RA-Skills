## Description:

Send iMessage notifications from a Mac through Apple's Messages app, including text, media files, audio, documents, and URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankxia2013](https://clawhub.ai/user/frankxia2013)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to have an agent send iMessage alerts, task completion notices, screenshots, reports, links, or other local files from a configured macOS machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages and files may be sent to a hard-coded personal Apple ID.

Mitigation: Replace hard-coded Apple IDs with explicit local configuration and confirm the recipient before sending sensitive content.

Risk: AppleScript is constructed directly from user-provided text and paths.

Mitigation: Pass user input to AppleScript as arguments or apply robust escaping before enabling the scripts.

Risk: The skill can send local media and document files through Messages.

Mitigation: Review selected file paths and require confirmation for sensitive attachments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frankxia2013/skills/imessage-notify)
- [Publisher profile](https://clawhub.ai/user/frankxia2013)
- [Skill definition](artifact/SKILL.md)
- [Text message script](artifact/scripts/send-imessage.sh)
- [Media message script](artifact/scripts/send-imessage-media.sh)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured macOS Messages/iMessage environment before commands can send messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
