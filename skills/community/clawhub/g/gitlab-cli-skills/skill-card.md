## Description:

Comprehensive GitLab CLI (glab) command reference and workflows for all GitLab operations. Use when working with merge requests, CI/CD pipelines, issues, releases, repositories, authentication, variables, labels, milestones, snippets, or any glab command. Covers 40+ sub-commands including glab mr, glab ci, glab issue, glab repo, glab release, glab variable, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vince-winkintel](https://clawhub.ai/user/vince-winkintel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and GitLab users use this skill as a command reference and workflow guide for GitLab operations through glab, including merge requests, issues, CI/CD, releases, authentication, and configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The merge-request test workflow may run repository-controlled code in an authenticated environment; the security scan is incomplete.

Mitigation: Review the workflow and its credential scope before installation. Consider running untrusted tests in an isolated environment without reusable credentials.

## Reference(s):

- [GitLab CLI Skills on ClawHub](https://clawhub.ai/vince-winkintel/skills/gitlab-cli-skills)
- [GitLab Model Context Protocol server documentation](https://docs.gitlab.com/user/model_context_protocol/mcp_server/)
- [GitLab CLI Minder setup source](https://gitlab.com/gitlab-org/cli/-/blob/00f5b8fe102e1a07471aadd5a2e44f6ff1befeeb/internal/commands/govern/setup/setup.go)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown with command examples and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.13.41 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
