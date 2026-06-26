## Description: <br>
Backs up OpenClaw workspace, config, and state with the built-in `openclaw backup create` command, and supports retention cleanup and health verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeyiptk](https://clawhub.ai/user/joeyiptk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to create, verify, schedule, and clean up local backups of OpenClaw state and workspace data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can include sensitive local OpenClaw data such as credentials, session history, workspace files, skills, and settings. <br>
Mitigation: Review the backup destination and permissions before use, treat archives as secrets, and prefer encrypted storage. <br>
Risk: The skill can configure automatic daily backups, which may copy sensitive data on a recurring schedule. <br>
Mitigation: Enable the cron job only after reviewing the schedule, retention expectations, and storage location. <br>
Risk: Cleanup commands can delete existing backup archives when run with `--execute`. <br>
Mitigation: Run cleanup in dry-run mode first and review the listed archives before deleting them. <br>


## Reference(s): <br>
- [Setup Guide](references/SETUP_GUIDE.md) <br>
- [ClawHub release page](https://clawhub.ai/joeyiptk/openclawbackup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and verifies local backup archives under the configured backup directory when the commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, version.txt, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
