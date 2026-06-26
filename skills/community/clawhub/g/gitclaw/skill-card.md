## Description: <br>
Back up the OpenClaw agent workspace to a GitHub repo and keep it synced via a cron-driven commit/push script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marian2js](https://clawhub.ai/user/marian2js) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to set up automatic workspace backup to a GitHub repository and keep it synchronized on a cron schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring GitHub backups may upload workspace files that contain secrets or private project data. <br>
Mitigation: Use a private repository and review the workspace for secrets or sensitive files before the first push. <br>
Risk: The setup flow can install system packages, configure GitHub authentication, create repositories, and add a cron job. <br>
Mitigation: Require explicit user confirmation before sudo installs, GitHub authentication, repository creation, and cron setup. <br>
Risk: A persistent cron job and backup script can continue pushing workspace changes after initial setup. <br>
Mitigation: Record the crontab entry and script path and verify the user knows how to remove both. <br>


## Reference(s): <br>
- [GitClaw homepage](https://gitclaw.ai) <br>
- [ClawHub skill page](https://clawhub.ai/marian2js/gitclaw) <br>
- [Publisher profile](https://clawhub.ai/user/marian2js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local git configuration, GitHub CLI authentication state, a backup shell script, and a crontab entry when followed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
