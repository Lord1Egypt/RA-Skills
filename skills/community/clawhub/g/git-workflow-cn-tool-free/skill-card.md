## Description:

Git 分支管理、冲突解决与提交规范助手，覆盖个人开发者日常版本控制场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for Chinese-language Git workflow guidance, including branch management, merge-conflict handling, rollback steps, and Conventional Commits message drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest Git commands that modify repositories, push to remotes, change global Git configuration, or delete local untracked work, branches, and stashes.

Mitigation: Review generated commands before execution, prefer preview or safer variants first, and keep backups for important work.

Risk: Cleanup and force-delete Git examples can remove local work when used without understanding repository state.

Mitigation: Check repository status, create a backup branch or stash, and use preview commands such as git clean -n before destructive cleanup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/git-workflow-cn-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Git shell commands and commit-message templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language responses focused on Git command guidance and review-before-execution workflows.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
