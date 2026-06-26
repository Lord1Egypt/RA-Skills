## Description: <br>
Real-time knowledge base synchronization for AI assistants, supporting inotifywait file monitoring, Git auto-push/pull, Nutstore sync, and multi-device consistency to maintain knowledge continuity across servers and local devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alfredming-2026](https://clawhub.ai/user/alfredming-2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and AI assistant users use this skill to keep an OpenClaw knowledge workspace synchronized across servers, Nutstore or Obsidian folders, and a Git remote. It supports continuous file monitoring, automated Git backup, and multi-device consistency workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Continuous synchronization can copy private workspace files to Nutstore, Obsidian folders, and a Git remote. <br>
Mitigation: Enable the skill only for intentional sync workflows, narrow the watched paths, verify the Git remote is private, and add .gitignore plus secret-scanning protections before starting systemd or cron jobs. <br>
Risk: Mirror-delete behavior can remove files from backup destinations during directory synchronization. <br>
Mitigation: Remove or gate rsync --delete, then test synchronization against a disposable backup or dry-run environment before using production knowledge directories. <br>
Risk: Automated Git commits use --no-verify and can push unintended changes. <br>
Mitigation: Review the auto-push script before scheduling it, avoid bypassing verification hooks, and require manual review or a protected remote for sensitive repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alfredming-2026/knowledge-sync) <br>
- [Publisher profile](https://clawhub.ai/user/alfredming-2026) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides synchronization setup guidance and shell scripts for continuous file copying and Git backup.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
