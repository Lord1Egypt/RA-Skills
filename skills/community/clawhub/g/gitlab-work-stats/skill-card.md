## Description:

Generates read-only GitLab user work-statistics reports covering merge requests, commits, and code review activity for a specified user and date range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[endcy](https://clawhub.ai/user/endcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering managers, and authorized operations staff use this skill to produce Markdown activity reports from GitLab Omnibus data for a specified user and time window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires SSH and database access to GitLab, which can expose sensitive work activity and repository metadata if access is over-privileged.

Mitigation: Use only with explicit authorization, a dedicated least-privilege read-only GitLab account, verified SSH host keys, and secrets stored outside the project directory.

Risk: The documented SQL patterns may be unsafe when usernames, dates, or keywords come from untrusted input.

Mitigation: Replace those patterns with real parameterization and enforce a technically read-only database role before using untrusted inputs.

Risk: Generated reports contain sensitive work activity statistics.

Mitigation: Limit reports to authorized users and time ranges, then protect and distribute them according to organizational data handling rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/endcy/skills/gitlab-work-stats)
- [GitLab PostgreSQL database guide](references/database-guide.md)
- [Report template](references/report-template.md)
- [Server configuration template](references/server-config.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with SQL, shell, and Python command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only GitLab activity summaries scoped to an authorized username and date range.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
