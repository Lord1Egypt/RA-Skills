## Description:

面向团队协作与企业研发场景的 Git 工作流专业工具，提供 Git Flow、GitHub Flow、GitLab Flow、多分支管理、冲突处理、发布分支和版本标签策略的操作指导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to plan and execute Git workflows for branch management, release management, conflict handling, tagging, changelog generation, and team collaboration practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose Git commands that alter branches, tags, remotes, global Git configuration, or commit history.

Mitigation: Review the exact commands, target branches, remotes, and repository state before execution; create backups or restore points before destructive operations.

Risk: Examples for remote deletion, reset, and force-push can remove shared references or rewrite shared history.

Mitigation: Treat these operations as manual confirmation-required actions; require team approval and prefer protected branches, backups, and force-with-lease safeguards.

Risk: Broad activation language may cause the skill to be used outside Git workflow governance tasks.

Mitigation: Use the skill for Git workflow planning, configuration, and command review, and supervise any command that changes repository state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/git-workflow-cn-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes structured Git workflow recommendations, command examples, configuration guidance, and error-handling notes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
