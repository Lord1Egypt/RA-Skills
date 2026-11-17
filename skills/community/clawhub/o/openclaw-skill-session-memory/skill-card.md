## Description:

Automatically saves conversations daily with sensitive data redacted and supports fast keyword search across recent sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiaotucodes](https://clawhub.ai/user/qiaotucodes)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to keep local, date-organized Markdown records of agent conversations and search recent sessions by keyword when they need prior context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation history is persistently copied into local searchable Markdown files with weak scoping and incomplete privacy protections.

Mitigation: Install only where conversation recording is expected, use explicit session scoping, restrict file permissions, and define retention, deletion, and opt-in controls.

Risk: Sensitive details may remain in saved memory files despite redaction.

Mitigation: Avoid recording sensitive sessions and review generated memory files before sharing, syncing, or using them on shared systems.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qiaotucodes/skills/openclaw-skill-session-memory)
- [README.md](artifact/README.md)
- [README-CN.md](artifact/README-CN.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown conversation records and terminal search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local searchable conversation files and returns keyword-search matches from recent sessions.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
