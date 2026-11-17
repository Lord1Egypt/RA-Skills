## Description:

全周期项目发布管控：覆盖版本创建、开发、预发布、发布、验证、运维和下版本规划的 13 步标准流程，支持交互式配置、版本一致性检测、可持续性评分和热更新。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongjie-oss](https://clawhub.ai/user/dongjie-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to standardize Docker-based releases that combine GitHub workflows, ACR image publishing, version metadata, changelog handling, deployment checks, and next-version planning. It is suited to teams that need an agent-guided release checklist with explicit confirmation before external actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad release and deployment actions, including Git pushes, tags, Docker image publishing, and remote deployment.

Mitigation: Require explicit user confirmation for release execution, review the exact staged files and diff before any push, and keep external operations gated by a human approval step.

Risk: Weak scoping around git staging and triggers can cause unintended files or release actions to be included.

Mitigation: Use explicit invocation phrases, inspect staged changes before commit, and run secret scanning before publishing.

Risk: Root SSH deployment increases operational impact if credentials or commands are misused.

Mitigation: Replace root SSH deployment with a dedicated least-privilege deploy account or a CI/CD-controlled deployment path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongjie-oss/skills/github-acr-release)
- [ClawHub publisher profile](https://clawhub.ai/user/dongjie-oss)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, shell commands, and generated script/configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file updates, release commands, checks, Docker operations, Git pushes, tags, and deployment verification steps for user review.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
