## Description:

GitHub team collaboration toolkit for managing team workflows, code reviews, issue tracking, sprint planning, and team metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate GitHub pull requests, issue triage, sprint milestones, and collaboration metrics for repository workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform write actions on GitHub repositories, including assigning reviewers and creating issues.

Mitigation: Require explicit user confirmation before write actions and use a least-privilege GitHub token scoped only to the needed repositories and permissions.

Risk: Running the helper script directly can print the first characters of the GitHub token.

Mitigation: Remove token-prefix printing before direct execution and avoid logging credentials.

Risk: Dependencies are specified with lower bounds only.

Mitigation: Pin and review dependency versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/github-team-collaboration)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GitHub API operations that require a GITHUB_TOKEN environment variable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
