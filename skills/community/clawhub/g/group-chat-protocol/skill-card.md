## Description:

Guides Loki's participation in Telegram group chats, including when to respond, react, stay silent, and preserve group privacy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

External users can apply this skill to govern an assistant's behavior in group chats, especially Telegram conversations where the assistant receives every message. It helps the assistant decide when to contribute, react, stay silent, and avoid exposing private context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The assistant may participate or react in a group chat where members do not expect automated involvement.

Mitigation: Confirm that the group wants the assistant to participate and react before enabling the skill.

Risk: The quiet-hours behavior assumes 23:00-08:00 AEST, which may not match the group's timezone.

Mitigation: Adjust the quiet-hours assumption to the group's actual timezone before use.

Risk: Private memory, DM history, or personal context could be disclosed in a group conversation if the host agent ignores the privacy rule.

Mitigation: Configure the host agent to keep private memory, DM history, and personal context out of group replies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/group-chat-protocol)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance for chat participation and platform formatting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; provides behavioral guidance for group-chat replies, reactions, silence, formatting, and privacy.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
