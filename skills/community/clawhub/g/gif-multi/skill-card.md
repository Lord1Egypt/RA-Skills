## Description:

Search and send GIF reactions on any messaging platform (Telegram, WhatsApp, Discord, Signal, etc). Auto-detects your enabled channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chdlc](https://clawhub.ai/user/chdlc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Giphy, convert GIF reactions for the active messaging channel, and send them through supported chat platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GIF search terms are sent to Giphy.

Mitigation: Avoid sending sensitive or private conversation content as GIF search queries.

Risk: Natural mode allows the skill to send GIFs without an explicit user request.

Mitigation: Set the mode to `on_request` when explicit user confirmation is required before sending media.

Risk: Security evidence flags under-scoped message-sending and cleanup behavior that can affect local files or unsafe shell cleanup if channel names are attacker-influenced.

Mitigation: Use trusted channel identifiers, keep cache cleanup constrained, and review cleanup behavior before deployment.

## Reference(s):

- [Giphy Developers](https://developers.giphy.com)
- [GIF Multi on ClawHub](https://clawhub.ai/chdlc/skills/gif-multi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script returns JSON that can include a generated media path, selected channel, format, query, warnings, errors, or setup help.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
