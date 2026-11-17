## Description:

OpenClaw Installer Cn helps agents diagnose OpenClaw installation problems, propose fixes for common errors, and generate recommended configuration for Chinese-language users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to check Node.js, npm, network, architecture, disk, and OpenClaw configuration issues, then receive repair guidance and configuration snippets for OpenClaw installation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repair guidance may include high-impact shell commands that change system permissions or dependency files.

Mitigation: Review each command and rollback plan before execution, especially commands using sudo or modifying /usr/local, ~/.npm, node_modules, or package lock files.

Risk: The skill may suggest piping a remote install script into bash or persisting shell and configuration changes.

Mitigation: Independently inspect remote scripts and generated configuration before running them or writing changes to ~/.zshrc or OpenClaw config files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/openclaw-installer-cn)
- [Publisher profile](https://clawhub.ai/user/yang1002378395-cmyk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with diagnostic findings, shell command snippets, and JSON or shell configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that modify npm settings, file permissions, dependency state, shell startup files, and OpenClaw configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
