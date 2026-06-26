## Description: <br>
Backup and restore OpenClaw configuration, agent memory, skills, workspace data, credentials, channel state, and scheduled tasks through shell scripts and an optional token-protected local HTTP interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leoyeai](https://clawhub.ai/user/leoyeai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users, operators, and developers use this skill to create encrypted-by-permission local backup archives, restore an instance after data loss, migrate to a new server, schedule recurring backups, and manage backup upload or download through a browser when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives include sensitive OpenClaw data such as API keys, bot tokens, credentials, sessions, memory, and installed skills. <br>
Mitigation: Install only when the publisher is trusted, keep backup archives protected, and avoid committing or sharing archives. <br>
Risk: The HTTP server can expose backup upload and download over the network. <br>
Mitigation: Keep the server local when possible; use a strong token and TLS for any network exposure. <br>
Risk: Restore operations overwrite persistent OpenClaw state. <br>
Mitigation: Run restore dry-runs first and review the planned changes before applying a restore. <br>
Risk: Scheduled backups modify crontab and older backup archives may be pruned automatically. <br>
Mitigation: Review scheduled backup settings and retention expectations before enabling periodic backups. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leoyeai/myclaw-backup) <br>
- [What Gets Saved](references/what-gets-saved.md) <br>
- [MyClaw Open Skills](https://myclaw.ai/skills) <br>
- [MyClaw.ai](https://myclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When its scripts are run, the skill can create tar.gz backup archives, start a token-protected HTTP backup manager, modify cron scheduling, and write restore status files.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
