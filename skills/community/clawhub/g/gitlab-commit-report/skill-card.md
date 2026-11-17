## Description:

GitLab group push events collector and daily commit report generator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bondli](https://clawhub.ai/user/bondli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team leads use this skill to collect GitLab group push events from an authenticated browser session and generate daily Markdown commit activity reports for a configured group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependencies are not locked, including the shared browser connection helper.

Mitigation: Review or pin dependencies and install with a lockfile before deployment.

Risk: Commit metadata, author names, repository names, and commit messages are stored locally.

Mitigation: Run the skill only against the intended GitLab host and group, and delete local stored reports and event data when retention is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bondli/skills/gitlab-commit-report)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown reports and JSON event files, with shell commands for collection and report generation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores daily GitLab push event data locally with commit id deduplication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
