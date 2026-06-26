## Description: <br>
Manage PaperMC Minecraft servers through safe, controlled interfaces for server lifecycle management, backups, plugin operations, health monitoring, and backup-first maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanxi1024-git](https://clawhub.ai/user/yanxi1024-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, server administrators, and operators use this skill to manage PaperMC Minecraft servers with controlled scripts for health checks, backups, plugin management, upgrades, and rollback planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes publishing scripts with hardcoded ClawHub credentials and broad upload behavior. <br>
Mitigation: Remove or isolate publishing scripts before installation and rotate any exposed ClawHub token. <br>
Risk: Plugin and server update workflows can download files and replace server artifacts. <br>
Mitigation: Restrict downloads to trusted sources, verify artifacts where possible, and require human approval before file replacement or restart. <br>
Risk: Operational scripts can restart services and modify PaperMC server files. <br>
Mitigation: Configure server paths explicitly, run backups before changes, and keep rollback procedures available before production use. <br>
Risk: Cost and log helper scripts may write local files under user home directories. <br>
Mitigation: Review whether local cost and log files are acceptable for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yanxi1024-git/papermc-ai-ops) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Architecture](artifact/docs/architecture.md) <br>
- [Changelog](artifact/docs/changelog.md) <br>
- [ViaVersion Upgrade Report](artifact/viaversion_upgrade_report.json) <br>
- [Turret Plugin User Manual](artifact/docs/Turret_Plugin_User_Manual.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python command examples, JSON reports, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing instructions emphasize backup-first operation, human review for risky updates, and controlled script entry points.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
