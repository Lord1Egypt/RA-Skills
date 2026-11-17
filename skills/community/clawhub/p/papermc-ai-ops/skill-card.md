## Description:

Manage PaperMC Minecraft servers through safe, controlled interfaces for server lifecycle management, backups, plugin operations, and health monitoring with a backup-first safety policy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanxi1024-git](https://clawhub.ai/user/yanxi1024-git)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and server operators use this skill to manage PaperMC Minecraft servers through controlled scripts for status checks, logs, backups, restarts, plugin installation, health monitoring, and upgrade planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is reported to include an exposed ClawHub token.

Mitigation: Do not install or run the release until the publisher removes the token and confirms it has been revoked.

Risk: Publishing utilities and broad upload scripts are included in the runtime package.

Mitigation: Remove publishing utilities from deployed copies and review packaged scripts before installation.

Risk: The skill can download executable plugin JARs from external locations.

Mitigation: Restrict downloads to trusted verified sources and manually inspect every downloaded JAR before use.

Risk: Server restart logic may terminate processes or affect availability.

Mitigation: Run under a dedicated unprivileged server account and require explicit operator confirmation for restart actions.

## Reference(s):

- [PaperMC AI Operations ClawHub Release](https://clawhub.ai/yanxi1024-git/skills/papermc-ai-ops)
- [Publisher Profile](https://clawhub.ai/user/yanxi1024-git)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [Architecture](artifact/docs/architecture.md)
- [Changelog](artifact/docs/changelog.md)
- [ViaVersion Upgrade Report](artifact/viaversion_upgrade_report.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, Python code examples, configuration notes, and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed by an operator before applying downloads, restarts, or other server-changing actions.]

## Skill Version(s):

2.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
