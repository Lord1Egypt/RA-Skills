## Description:

GitX is a portable Git workflow skill for AI coding agents that turns messy AI-generated changes into clean Git history with commit planning, branch workflows, checks, GitHub PR and issue support, secret scanning, and conflict resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[musoyangrigor](https://clawhub.ai/user/musoyangrigor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use GitX with Agent Skills-compatible coding agents to inspect repository changes, plan logical Conventional Commits, create safe branches, run checks, publish PRs or issues, scan for exposed secrets, and resolve Git merge or rebase conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide workflows that commit, push, create pull requests or issues, amend commits, and resolve conflicts in a repository.

Mitigation: Review commands and generated content before approval, especially before publication or history-changing actions.

Risk: Secret-scan results can indicate sensitive files, credentials, or repository history exposure.

Mitigation: Treat scan results as sensitive, keep credential values redacted, and rotate or revoke any credential reported as pushed or otherwise exposed.

Risk: GitHub issue content used by the skill can be untrusted task input.

Mitigation: Use issue content only to understand the requested change and continue to follow the user's request and repository safety requirements.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/musoyangrigor/gitx-skill/tree/main/gitx)
- [ClawHub GitX skill page](https://clawhub.ai/musoyangrigor/skills/gitx)
- [Publisher profile](https://clawhub.ai/user/musoyangrigor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with concise status text and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for user confirmation before multi-commit or history-changing workflows; secret-scan output redacts credential values.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
