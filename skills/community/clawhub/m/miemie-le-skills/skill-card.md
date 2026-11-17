## Description:

Interactive wizard for creating a brand-new OpenClaw skill folder with a required SKILL.md file and optional helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[somkh](https://clawhub.ai/user/somkh)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to turn a user's idea into a deployable OpenClaw skill directory through a structured requirements, generation, deployment, testing, and repair workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, replace, back up, and repair local OpenClaw skill folders.

Mitigation: Review generated files before deployment, confirm exact source and destination paths, and keep backups before replacement or repair.

Risk: The security summary notes broad local changes and auto-install guidance without enough containment.

Mitigation: Do not allow unattended package installs or sudo/admin commands; require explicit user approval before installing tools or modifying deployed skills.

Risk: Untrusted users could influence writable OpenClaw directories through symlinks or modified contents.

Mitigation: Run the skill only in trusted local OpenClaw directories and avoid locations where untrusted users can create symlinks or edit .openclaw contents.

## Reference(s):

- [README](artifact/README.md)
- [Skill Generator Protocol](artifact/SKILL.md)
- [Skill Design Reference](artifact/references/design-reference.md)
- [Tool Setup Guide](artifact/references/tool-setup-guide.md)
- [Error Report Template](artifact/references/error-report-template.md)
- [ClawHub Skill Page](https://clawhub.ai/somkh/skills/miemie-le-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance, generated SKILL.md content, optional helper scripts, shell commands, and JSON status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local OpenClaw skill folders through user-guided auto or manual workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-05-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
