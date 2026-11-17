## Description:

Helps agents monitor GitHub pull requests, issues, CI status, releases, and multi-repository maintenance work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project maintainers, technical managers, and open-source contributors use this skill to triage pull requests, track related issues, monitor CI failures, and prepare repository maintenance summaries across one or more GitHub repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires GitHub token access and does not clearly scope repository permissions.

Mitigation: Use a least-privilege token limited to the repositories and actions needed for the current task.

Risk: Automation around pull requests, issues, workflows, branches, and releases can change repository state.

Mitigation: Require explicit confirmation before merges, issue or pull request changes, workflow triggers, branch deletion, or release publication.

Risk: The artifact metadata claims no API key is needed, while the skill text says GITHUB_TOKEN is required.

Mitigation: Treat GitHub token configuration as required and review the token handling path before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/skills/huimai-github-auto)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with optional shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GitHub token for repository access; destructive actions are described as requiring user confirmation.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact changelog, released 2026-05-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
