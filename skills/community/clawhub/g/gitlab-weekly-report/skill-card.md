## Description:

Generates weekly reports by querying GitLab API for a user's commits over a date range and organizing them by project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhoutianwang](https://clawhub.ai/user/zhoutianwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and employees use this skill to collect their GitLab commits for the current or previous week and turn them into a structured weekly report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitLab personal access tokens may be exposed through command-line arguments or curl invocation.

Mitigation: Edit the script before use to avoid passing tokens via --token or curl arguments; use a least-privilege token and rotate any token used with this version.

Risk: Authenticated API requests disable normal certificate verification and network protections.

Mitigation: Remove curl -k and --noproxy * before installation so standard TLS and proxy protections remain enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhoutianwang/skills/gitlab-weekly-report)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown weekly report with command-line script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GitLab API access, a user ID, a date range, and local configuration of the GitLab instance URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
