## Description:

OpenClaw Coach automates OpenClaw documentation sync, daily tip selection, scheduled tip delivery, and version update reminders for a local Obsidian knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rabbot42](https://clawhub.ai/user/rabbot42)

### License/Terms of Use:


## Use Case:

OpenClaw users can use this skill to keep local OpenClaw reference material current in Obsidian and receive scheduled coaching messages with selected daily tips and version reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends local tip content to a fixed OpenClaw recipient without enough user control.

Mitigation: Configure or remove the hard-coded recipient and require confirmation before scheduled sends are enabled.

Risk: Document sync writes fetched content into the local Obsidian OpenClaw directory.

Mitigation: Make document sync opt-in, document the overwrite behavior, and review the destination path before running sync.

Risk: Tip filenames are read from local state and used to load markdown content for outgoing messages.

Mitigation: Validate selected tip filenames against an allowlist before reading or sending tip content.

## Reference(s):

- [OpenClaw documentation source](https://raw.githubusercontent.com/openclaw/openclaw/main/docs)
- [OpenClaw releases API](https://api.github.com/repos/openclaw/openclaw/releases/latest)
- [OpenClaw Coach on ClawHub](https://clawhub.ai/rabbot42/skills/openclaw-coach-rabbot42)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown and shell-script driven OpenClaw messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scheduled messages, local markdown files, a daily tip JSON file, and a latest-version text file.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
