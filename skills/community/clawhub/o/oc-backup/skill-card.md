## Description: <br>
Backs up key OpenClaw configuration, workspace, skill, memory, cron, and device files, with dry-run, JSON output, retention cleanup, and recovery guide support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neverland83](https://clawhub.ai/user/neverland83) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create local backups of OpenClaw configuration, workspace files, custom skills, memory, cron jobs, and device data before changes or on a schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives can include sensitive OpenClaw data such as .env secrets, device data, memory, and user configuration. <br>
Mitigation: Keep backups private, restrict filesystem access, and encrypt archives or storage locations when sensitive files are included. <br>
Risk: Broad conversational triggers or default full backups may copy more OpenClaw data than intended. <br>
Mitigation: Run the skill with --dry-run first and choose explicit backup categories when only part of the OpenClaw state should be copied. <br>
Risk: Retention cleanup can delete older backup directories when --retain is used. <br>
Mitigation: Preview cleanup with --clean --retain <days> --dry-run before allowing deletion. <br>


## Reference(s): <br>
- [Backup File List](artifact/references/FILE_LIST.md) <br>
- [Recovery Guide Template](artifact/references/RECOVERY_GUIDE_TEMPLATE.md) <br>
- [Configuration Example](artifact/config/config.example.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/neverland83/oc-backup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Compressed tar.gz backup, JSON manifest, Markdown recovery guide, and optional JSON or console text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run previews, category-specific backups, custom output directories, and retention cleanup.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md; package.json reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
