## Description: <br>
GitHub Issue Resolver discovers, analyzes, and fixes open GitHub issues, then helps test and prepare draft pull requests under repository, branch, path, command, and approval guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ashwinhegde19](https://clawhub.ai/user/Ashwinhegde19) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and maintainers use this skill to discover, analyze, fix, test, and prepare draft pull requests for open GitHub issues while applying repository, branch, path, command, and approval guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate through local git and an authenticated GitHub CLI account, including pushing branches and opening pull requests. <br>
Mitigation: Use only with repositories you intend to grant access to, review the target repository and branch before each run, and keep push and pull request creation under explicit user approval. <br>
Risk: The included pull request helper may push code and create pull requests without fully matching the documented approval and draft safeguards. <br>
Mitigation: Review, fix, or disable scripts/create_pr.py before relying on it; require shell-free subprocess argument lists, input validation, explicit confirmation, and draft pull requests by default. <br>
Risk: Audit logs may contain sensitive repository context or diffs from private codebases. <br>
Mitigation: Review and clear local audit logs after use on private repositories, especially when logs may contain sensitive diffs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ashwinhegde19/github-issue-resolver) <br>
- [Guardrails guide](references/guardrails-guide.md) <br>
- [Quick reference](references/quick-reference.md) <br>
- [GitHub CLI](https://cli.github.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON from helper scripts, code changes, commits, and draft pull request links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a one-issue-at-a-time workflow with approval gates for code changes, commits, pushes, pull request creation, dependency installation, and dangerous commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
