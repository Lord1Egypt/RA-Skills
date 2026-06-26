## Description: <br>
Create, update, validate, or troubleshoot automated git backup workflows for OpenClaw repositories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blacktor-tor](https://clawhub.ai/user/blacktor-tor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure scheduled OpenClaw git backups that commit repository changes, push to a chosen remote branch, and validate that the backup job actually runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sets up automated commits and pushes for a selected repository, so a misconfigured remote, branch, schedule, or exclusion list could back up the wrong material or create noisy commits. <br>
Mitigation: Confirm the repository, remote, branch, schedule, and exclusion patterns before enabling the job, then force-run and inspect the result. <br>
Risk: Automated git backups can accidentally commit secrets or rely on credentials that outlive the backup need. <br>
Mitigation: Avoid committing secrets, use least-privilege or expiring credentials, and remove the cron job or credential file when automated backups are no longer needed. <br>


## Reference(s): <br>
- [Backup Scope](references/backup-scope.md) <br>
- [Cron Job Template](references/cron-job-template.md) <br>
- [ClawHub Release Page](https://clawhub.ai/blacktor-tor/openclaw-git-backup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include executable backup-script installation steps, cron configuration, git credential guidance, and validation commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
