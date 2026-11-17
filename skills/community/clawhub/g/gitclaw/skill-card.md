## Description:

Back up the OpenClaw agent workspace to a GitHub repo and keep it synced via a cron-driven commit/push script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marian2js](https://clawhub.ai/user/marian2js)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to configure recurring GitHub backups for an agent workspace, including prerequisite checks, GitHub CLI authentication, repository setup, and scheduled sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can repeatedly push the full agent workspace to GitHub, which may expose secrets or private files.

Mitigation: Use strong ignore rules or an allowlist, review the first staged file list, and choose a private repository unless public exposure is intentional.

Risk: The skill may use sudo to install software and enable cron-based automation.

Mitigation: Require explicit approval for package installation and cron registration before allowing persistent changes.

Risk: The backup behavior is designed to run quietly and recur on a schedule.

Mitigation: Review the generated script and schedule before installation, and monitor the backup log after the first run.

## Reference(s):

- [GitClaw homepage](https://gitclaw.ai)
- [ClawHub skill page](https://clawhub.ai/marian2js/skills/gitclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and bash script content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup steps for Git, GitHub CLI authentication, repository creation, a recurring backup script, cron configuration, and validation output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
