## Description:

面向研发团队的高级Git版本控制工具,包含交互式变基、历史重写、子模块成批管控、仓库性能调优与团队协作工作流。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to plan and review advanced Git workflows such as interactive rebases, history rewrites, submodule management, bisect debugging, repository cleanup, and version tagging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: History rewrite, force-push, and aggressive cleanup commands can permanently change shared Git history or remove recovery data.

Mitigation: Review each command before execution, work from a backup or mirror clone, coordinate with collaborators, and prefer force-with-lease when pushing rewritten history.

Risk: Plaintext Git credential-store guidance can expose repository credentials on disk.

Mitigation: Avoid plaintext credential storage; use SSH keys or an operating-system-backed credential manager.

Risk: Submodule deletion and batch update commands can remove module metadata or commit unexpected dependency changes.

Mitigation: Confirm submodule paths and status first, test changes in a disposable clone when possible, and review the resulting diff before committing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Git configuration snippets, and structured JSON-style examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before execution, especially commands that rewrite history, delete submodules, alter credentials, force-push, or run aggressive cleanup.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
