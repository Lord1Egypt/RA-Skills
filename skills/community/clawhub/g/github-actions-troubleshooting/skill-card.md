## Description:

Troubleshoot GitHub Actions workflows, particularly for Go projects. Diagnose failing workflows, distinguish between code and environment issues, interpret logs, and apply fixes for common CI/CD problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[irook661](https://clawhub.ai/user/irook661)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to diagnose failing GitHub Actions workflows, inspect logs and artifacts, separate code failures from CI environment issues, and apply common Go CI fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub CLI commands operate against repositories and workflow runs supplied by the user, so incorrect targets may expose or modify the wrong project context.

Mitigation: Confirm the repository owner/name and run identifiers before executing commands, and use accounts with least necessary repository access.

Risk: Downloaded workflow artifacts may contain untrusted files, scripts, or binaries.

Mitigation: Download artifacts into an isolated directory, review artifact names and sources, avoid directly running downloaded content, and delete artifacts when analysis is complete.

Risk: Suggested Go CI fixes such as dependency cleanup or linter configuration changes can alter project behavior if applied without review.

Mitigation: Review proposed changes in version control and run the relevant tests or workflow checks before merging.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/irook661/skills/github-actions-troubleshooting)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GitHub CLI and Git; examples assume the user supplies the target repository and workflow run identifiers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
