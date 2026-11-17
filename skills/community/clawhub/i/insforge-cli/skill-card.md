## Description:

Guides agents through InsForge CLI workflows for backend infrastructure management, including projects, databases, functions, storage, deployments, secrets, schedules, and logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonychang04](https://clawhub.ai/user/tonychang04)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate InsForge Backend-as-a-Service projects from an agent session. It supports schema changes, function deployment, storage, frontend hosting, secrets, schedules, logs, backup, and restore workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad backend administration actions, including database changes, deployments, schedules, storage, and secrets.

Mitigation: Install and use it only for intended InsForge projects, review proposed commands before execution, and use least-privilege or short-lived credentials.

Risk: Some workflows include mutable installs or automatic skill installation.

Mitigation: Prefer pinned CLI versions and confirm any additional skill installation before allowing it.

Risk: Destructive or high-impact commands can remove storage buckets, truncate imported data, deploy code, or change schedules.

Mitigation: Avoid blanket confirmation flags for destructive actions and verify target project, resource names, and backups first.

Risk: Commands and exports may expose credentials, secrets, or sensitive data in shell history, transcripts, or files.

Mitigation: Do not place real secrets in command lines or transcripts, protect database exports, and use secret references where supported.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tonychang04/skills/insforge-cli)
- [insforge create](references/create.md)
- [insforge db export](references/db-export.md)
- [insforge db import](references/db-import.md)
- [insforge db query](references/db-query.md)
- [insforge deployments deploy](references/deployments-deploy.md)
- [insforge functions deploy](references/functions-deploy.md)
- [insforge login](references/login.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, code snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that affect live InsForge backend resources and credentials.]

## Skill Version(s):

0.1.0 (source: server release metadata; skill frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
