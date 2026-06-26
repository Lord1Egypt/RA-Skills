## Description: <br>
Backs up OpenClaw data with manual or scheduled runs, optional AES-256 encryption, SHA256 checksums, and cloud-sync oriented workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halaoluan](https://clawhub.ai/user/halaoluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to create local or encrypted backups of OpenClaw configuration, memory, skills, and related state, and to schedule recurring backup jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may contain sensitive OpenClaw data such as API keys, tokens, memory, conversation history, and channel login state. <br>
Mitigation: Prefer the encrypted backup script, use a strong password stored outside the backup archive, and avoid uploading plaintext archives to cloud folders. <br>
Risk: The scheduling script creates or replaces cron entries that run backup commands automatically. <br>
Mitigation: Inspect the generated crontab entry, confirm the script path and log destination, and remove or adjust the cron job if it does not match the intended schedule. <br>
Risk: Documented cleanup commands using rm, find, xargs, or delete flags can remove files if copied without review. <br>
Mitigation: Preview matched files before deletion and run destructive cleanup commands only after confirming the target backup directory and patterns. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/halaoluan/halaoluan-openclaw-backup) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenSSL documentation](https://www.openssl.org/docs/) <br>
- [cron manual](https://man.openbsd.org/cron.8) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command snippets and shell-script execution instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create backup archives, encrypted backup archives, SHA256 checksum files, and cron entries when the user runs the provided scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
