## Description: <br>
Optimized OpenClaw backup skill for creating full snapshots with workspace archive splitting, change summaries, restore instructions, and Discord notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cccarv82](https://clawhub.ai/user/cccarv82) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install, configure, and run automated backups of OpenClaw home data, generate snapshot reports, schedule cron jobs, and follow restore instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backup workflow can copy sensitive OpenClaw data to a remote Git repository. <br>
Mitigation: Use a private repository you control, review exactly what files are included, avoid storing secrets in the backup, and consider encrypting data before upload. <br>
Risk: Automatic force pushes may overwrite remote backup history. <br>
Mitigation: Use a dedicated backup repository or branch, understand the force-push behavior before enabling automation, and verify that local history retention meets recovery needs. <br>


## Reference(s): <br>
- [Backup skill configuration](references/CONFIG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, environment variable examples, and a Node.js backup script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or copy a local backup script and configuration values for scheduled OpenClaw backups.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
