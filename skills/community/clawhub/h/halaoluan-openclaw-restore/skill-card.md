## Description: <br>
Restores OpenClaw data from encrypted or unencrypted backups, including latest-backup selection, checksum validation, current-data backup, and OpenClaw health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halaoluan](https://clawhub.ai/user/halaoluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to recover from data loss, device migration, failed upgrades, or disaster recovery events. It helps restore OpenClaw and ClawdBot state from selected backup archives and then verify that OpenClaw can restart successfully. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restoring a backup can replace active OpenClaw state, credentials, memories, skills, and configuration. <br>
Mitigation: Install only from a trusted publisher, restore only trusted backups, and keep an extra copy of current ~/.openclaw and ~/.clawdbot data before running restore scripts. <br>
Risk: A damaged or untrusted backup can cause a failed restore or reintroduce old credentials, sessions, memories, skills, and configuration. <br>
Mitigation: Verify backup checksums from a trusted source before restore and review the restored OpenClaw state before relying on it. <br>


## Reference(s): <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [OpenClaw Disaster Recovery Guide](https://docs.openclaw.ai/guides/disaster-recovery) <br>
- [ClawHub Skill Page](https://clawhub.ai/halaoluan/halaoluan-openclaw-restore) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and checklist-style recovery guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run restore scripts that move current OpenClaw state, copy backup contents into the user home directory, and restart the OpenClaw gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
