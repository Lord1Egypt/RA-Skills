## Description: <br>
OpenClaw Backup YYC backs up and restores selected OpenClaw data under ~/.openclaw after exact bilingual trigger commands and user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teldyang](https://clawhub.ai/user/teldyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to create backup archives of default OpenClaw configuration, workspace, agent, cron, and media data, and to restore those items from trusted backup archives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local scripts that read and rewrite OpenClaw data. <br>
Mitigation: Review the scripts before installation, avoid running them as root, and create or retain a current backup before restoring. <br>
Risk: Restore operations can replace or rename existing OpenClaw workspace, agent, cron, and media directories. <br>
Mitigation: Restore only archives you personally trust, confirm the selected archive carefully, and restart OpenClaw Gateway after a successful restore. <br>
Risk: The backup script contacts public IP services to generate an SCP command example. <br>
Mitigation: Run the backup only in environments where this outbound network lookup is acceptable, or review and modify the script before use. <br>
Risk: Only the default OpenClaw paths are backed up. <br>
Mitigation: Manually identify and save any OpenClaw-related files stored outside ~/.openclaw/openclaw.json, workspace, agents, cron, and media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teldyang/openclaw-backup-yyc) <br>
- [Publisher profile](https://clawhub.ai/user/teldyang) <br>
- [Author blog](https://blog.tag.gg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Shows backup file paths, file sizes, restore choices, confirmation prompts, warnings, and SCP download command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
