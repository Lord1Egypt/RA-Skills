## Description:

Generates an operational resume card before Claude context compaction so the next session can recover the prior branch, commit, recent intent, work mode, and next step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nadalpiantini](https://clawhub.ai/user/nadalpiantini)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code use this skill to preserve operational context across compaction events and automatically restore a compact resume card when a new session starts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores transcript backups and a resume card that may contain sensitive chat or project context.

Mitigation: Use it only in projects where transcript retention is acceptable, keep thinking/session-logs/ and .claude/session-resume-card.md out of version control, and avoid placing secrets in chats or memory files.

Risk: SessionStart reloads prior context automatically, which may reintroduce stale, overly broad, or unsanitized information.

Mitigation: Review restored resume-card content, narrow hook matchers where practical, and add sanitization or confirmation before restored text is treated as active context.

Risk: Shell hooks run inside the project and perform file reads and writes.

Mitigation: Review scripts before installing and prefer a pinned or manual install path so the executed hook code is known.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nadalpiantini/skills/pre-compact-resume-card)
- [Publisher profile](https://clawhub.ai/user/nadalpiantini)
- [Hook settings example](artifact/references/settings-example.json)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration]

**Output Format:** [Markdown resume card and hook configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes .claude/session-resume-card.md and retains up to 30 transcript backups in thinking/session-logs/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
