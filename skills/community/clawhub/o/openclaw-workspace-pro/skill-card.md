## Description:

Sets up an OpenClaw workspace with artifact folders, persistent agent guidance, secrets handling patterns, memory compaction guidance, and long-running work conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eugene9d](https://clawhub.ai/user/eugene9d)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to bootstrap a structured OpenClaw workspace for long-running agent work, including artifact organization, memory maintenance, and credential handling conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently changes future agent instructions by appending workspace guidance.

Mitigation: Review the AGENTS.md additions before installation and keep only guidance that matches the workspace's operating policy.

Risk: The provided tool guidance includes broad network and task-tracking behavior.

Mitigation: Remove or narrow Vikunja, Telegram, wildcard, and other network permissions unless they are required for the deployment.

Risk: External task updates may expose sensitive project or credential context if used without clear handling rules.

Mitigation: Add explicit approval and redaction rules before allowing agents to send updates to external task or messaging systems.

Risk: Uninstall commands remove workspace files and directories.

Mitigation: Inspect the targets and backups before running the provided rm commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eugene9d/skills/openclaw-workspace-pro)
- [OpenAI Shell, Skills, and Compaction guidance](https://developers.openai.com/blog/skills-shell-tips)
- [Artifact README](artifact/README.md)
- [Memory compaction workflow](artifact/templates/MEMORY-COMPACTION.md)
- [Workspace agent additions](artifact/templates/AGENTS-additions.md)
- [Workspace tool additions](artifact/templates/TOOLS-additions.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, markdown, guidance]

**Output Format:** [Markdown guidance and shell commands that install or update workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates workspace directories and templates, appends guidance to AGENTS.md and TOOLS.md when present, and preserves backups for existing files.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md frontmatter, package.json, CHANGELOG released 2026-02-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
