## Description:

Guides agents through GitHub-centered project workflows covering repository setup, branching, commits, pull requests, CI/CD, releases, secrets management, and work logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kretkas](https://clawhub.ai/user/kretkas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to manage GitHub repositories with consistent branching, pull request, CI, release, secret-handling, and task-continuity practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly applies a GitHub workflow to coding tasks and may lead an agent to create or change repository artifacts.

Mitigation: Install it only for GitHub-centered work, require explicit user approval before branch, commit, issue, pull request, merge, release, secret, workflow, branch-protection, or work-log writes, and avoid enabling it globally for unrelated tasks.

Risk: GitHub authentication and repository secrets are part of the workflow.

Mitigation: Use `gh auth status` to verify authentication, set secrets interactively with `gh secret set`, and never print or log tokens, secrets, or credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kretkas/skills/github-project-workflow)
- [API Queries, Search & Audit](references/api-queries.md)
- [CI / GitHub Actions](references/ci-actions.md)
- [Pull Requests](references/pull-requests.md)
- [Releases & Versioning](references/releases.md)
- [Repo Setup & Branch Protection](references/repo-setup.md)
- [Secrets & Environments](references/secrets-envs.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workflow checklists, confirmation warnings for write operations, and secret-handling guidance.]

## Skill Version(s):

1.3.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
