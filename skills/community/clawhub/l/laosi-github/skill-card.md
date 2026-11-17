## Description:

GitHub操作助手 - PR/Issue/代码搜索/仓库管理，基于gh CLI。v2新增：CI状态监控、Release管理、Code Review辅助

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate GitHub repositories with gh CLI commands for pull requests, issues, repository browsing, code search, code review support, CI status monitoring, and release management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to use an authenticated GitHub CLI session for repository-changing actions such as merging pull requests or closing issues.

Mitigation: Use a least-privilege GitHub account or token, verify the target repository before commands run, and require explicit user confirmation before write actions.

Risk: The skill depends on the local gh CLI authentication context, so commands may affect whichever GitHub account and repository are active.

Mitigation: Confirm gh authentication status and repository scope before use, especially in shared or multi-repository workspaces.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/534422530/skills/laosi-github)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline bash commands and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the GitHub CLI binary and an authenticated gh session.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
