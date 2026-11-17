## Description:

龙虾记忆体系统 - 模块化、版本化、自动备份的 AI 记忆管理方案

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzhqqq123](https://clawhub.ai/user/wzhqqq123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-assistant users use this skill to set up a modular, versioned memory system with long-term and short-term memory, configuration files, daily backups, and self-improvement notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill asks users to run PowerShell setup commands with execution-policy bypass from scripts that are not included in the release artifact.

Mitigation: Inspect the actual scripts from a trusted source before running them, and prefer manual setup or narrowly scoped permissions when possible.

Risk: The security evidence says automated backups may copy sensitive memory, configuration, preferences, project data, and agent behavior files.

Mitigation: Treat backup archives as sensitive data, restrict access to the backup location, and review retention and encryption settings before enabling scheduled backups.

Risk: The security guidance flags the recursive full-control permission repair command as potentially broad.

Mitigation: Avoid recursive full-control permission changes unless the scope and impact are understood; use narrower permissions for the memory-system directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzhqqq123/skills/lobster-memory-system)
- [Project homepage](https://github.com/openclaw/lobster-memory-system)
- [INSTALL.md](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples and PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or update memory, configuration, backup, and audit-log files.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.yaml, _meta.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
