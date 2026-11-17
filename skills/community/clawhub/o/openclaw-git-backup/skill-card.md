## Description:

Create, update, validate, or troubleshoot automated git backup workflows for OpenClaw repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blacktor-tor](https://clawhub.ai/user/blacktor-tor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, configure, validate, and troubleshoot scheduled git backup workflows for OpenClaw repositories, including commit summaries, push behavior, credential setup, and cron execution checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled git backup can automatically commit and push broad repository contents, including unintended files.

Mitigation: Confirm the repository, remote, branch, schedule, and exclude rules before enabling the job; treat the first run as a review run and inspect what would be staged.

Risk: Secrets, credentials, local state, or scheduler noise may be captured if ignored or excluded paths are incomplete.

Mitigation: Verify ignore rules and BACKUP_EXCLUDES before running, and document any runtime state that lives outside the repository or needs a separate backup path.

Risk: HTTPS push credentials can be exposed if tokens are embedded in remotes or stored with weak controls.

Mitigation: Prefer SSH deploy keys, a keychain, or narrowly scoped short-lived credentials; never place tokens in remote URLs and restrict any credential file permissions.

Risk: Scheduler command templating can execute an unintended command when values are not safely quoted.

Mitigation: Avoid the bash -lc cron template with unescaped values; use direct script invocation or a safely quoted scheduler configuration.

## Reference(s):

- [Backup Scope](references/backup-scope.md)
- [Cron Job Template](references/cron-job-template.md)
- [ClawHub Skill Page](https://clawhub.ai/blacktor-tor/skills/openclaw-git-backup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation results, commit or push status, and backup-scope notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
