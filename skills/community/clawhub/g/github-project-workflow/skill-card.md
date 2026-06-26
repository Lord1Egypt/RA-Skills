## Description: <br>
Professional GitHub workflow skill for AI agents covering repository setup, Git Flow branching, atomic commits, pull requests, code review, CI/CD monitoring, semantic versioning, releases, secrets management, and security rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kretkas](https://clawhub.ai/user/kretkas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to apply a structured GitHub project workflow for repository setup, branching, work logs, pull requests, CI checks, releases, and credential-safe operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through repository writes, merges, releases, branch protection changes, archives, deletes, and secret updates. <br>
Mitigation: Confirm the target repository and GitHub account before actions, require explicit user approval for irreversible or security-sensitive changes, and review proposed commands before execution. <br>
Risk: The skill depends on GitHub credentials and may operate around sensitive repository secrets. <br>
Mitigation: Use least-privilege tokens, prefer interactive secret entry, and keep tokens, secret values, and credentials out of logs and command output. <br>


## Reference(s): <br>
- [GitHub Workflow on ClawHub](https://clawhub.ai/kretkas/github-project-workflow) <br>
- [API Queries, Search & Audit](references/api-queries.md) <br>
- [CI / GitHub Actions](references/ci-actions.md) <br>
- [Pull Requests](references/pull-requests.md) <br>
- [Releases & Versioning](references/releases.md) <br>
- [Repo Setup & Branch Protection](references/repo-setup.md) <br>
- [Secrets & Environments](references/secrets-envs.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and workflow templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GitHub account, gh CLI authentication, and careful handling of repository secrets.] <br>

## Skill Version(s): <br>
1.3.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
