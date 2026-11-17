## Description:

基于 kiro-spec-engine (kse) 的 CLI 开发工作流，帮助代理使用 kse 命令创建规格文档、管理项目结构、增强文档质量、检查环境并推进 spec-driven 开发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sougannkyou](https://clawhub.ai/user/sougannkyou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to run a CLI-centered KSE workflow: initialize a project, create specs, write requirements/design/tasks documents, enhance documentation, check the local environment, and validate implementation against acceptance criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow recommends installing kiro-spec-engine as an unpinned global npm CLI, which can expose users to unexpected package changes or broad local command execution.

Mitigation: Review the package source, pin a trusted version before installation, and avoid elevated privileges when installing or running the CLI.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and project-file conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces procedural CLI workflow guidance; no structured machine-readable output is specified.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
