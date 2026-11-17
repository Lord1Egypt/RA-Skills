## Description:

老默 GitHub 助手 - 多账户管理、PR 一键推送/清理、代码审查、通知推送。v2.0 完整功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrzhangkris](https://clawhub.ai/user/mrzhangkris)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to automate common GitHub workflows, including multi-account GitHub CLI management, pull request creation and cleanup, local PR review, and notifications to team chat services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change GitHub repositories and pull requests using the current GitHub CLI identity.

Mitigation: Install only when the publisher is trusted, verify the active GitHub CLI account before use, and review repository and pull request targets before executing mutating commands.

Risk: Account add and switch workflows may log out the current GitHub CLI session.

Mitigation: Use explicit account aliases, validate the active account after switching, and avoid running account changes in shared or production automation sessions.

Risk: Branch cleanup and PR merge actions can delete remote branches or alter repository state.

Mitigation: Use dry-run modes where available and manually review cleanup targets before approving destructive operations.

Risk: Notification commands may send repository metadata or custom messages to external chat services.

Mitigation: Configure webhooks only for approved destinations and avoid sending sensitive repository details in notification content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrzhangkris/skills/laomo-github)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown]

**Output Format:** [Markdown with inline bash code blocks and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate through the local GitHub CLI identity and configured notification webhooks.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json, released 2026-03-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
