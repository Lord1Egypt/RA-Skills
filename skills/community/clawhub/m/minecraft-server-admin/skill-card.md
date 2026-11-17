## Description:

Execute Minecraft Java Edition admin commands through the RCON remote console for player moderation, whitelist management, item and world state changes, broadcast messages, and recent log review on servers the user controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[en1r0py1865](https://clawhub.ai/user/en1r0py1865)

### License/Terms of Use:

MIT-0

## Use Case:

External server administrators and developers use this skill to operate Minecraft Java Edition servers through RCON, including moderation, server communication, world adjustments, and recent log review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue high-impact live server commands through RCON, including bans, operator changes, world edits, entity removal, and shutdown.

Mitigation: Use it only on Minecraft servers you control and require explicit human review before destructive or privilege-changing commands are executed.

Risk: RCON exposure or weak credentials could allow unauthorized server administration.

Mitigation: Bind RCON to localhost or a trusted tunnel/VPN and use a dedicated strong RCON password.

Risk: Recent server logs may contain player activity, chat, command history, or operational details.

Mitigation: Enable MC_SERVER_LOG only when that information is appropriate for the agent to inspect.

Risk: The release evidence flags an unnecessary unpinned npm install dependency.

Mitigation: Remove the unused dependency or pin and review it before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/en1r0py1865/skills/minecraft-server-admin)
- [Project Homepage](https://github.com/en1r0py1865/minecraft-skill)
- [Vanilla Command Reference](references/commands.md)
- [Minecraft Server Log Patterns](references/log-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON log-analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and RCON environment variables; optional log analysis reads MC_SERVER_LOG when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
