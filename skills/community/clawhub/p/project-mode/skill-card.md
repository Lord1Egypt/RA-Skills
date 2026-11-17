## Description:

激活项目制多智能体开发协议，用于处理复杂的代码开发和系统搭建需求，并在后台拆解任务、调度程序员和测试员、更新 dev_project.md、处理错误重试。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tincomking](https://clawhub.ai/user/tincomking)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to manage complex software projects through a project-mode workflow that decomposes requirements, coordinates implementation and testing roles, tracks progress in dev_Project.md, and reports status to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overwrite persistent project state in dev_Project.md with weak scoping.

Mitigation: Review the target dev_Project.md before use, keep backups, and run the workflow only in the intended OpenClaw workspace.

Risk: The skill enables broad background development automation that can change code or project-tracking files.

Mitigation: Review generated task plans and changes before continuing to implementation or final delivery.

Risk: The documented memory-viewer command may expose local workspace data.

Mitigation: Avoid running the memory-viewer command unless you understand what local data it displays and who can access it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tincomking/skills/project-mode)
- [Publisher profile](https://clawhub.ai/user/tincomking)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown status reports with generated task descriptions, code-oriented guidance, shell commands, and project tracking updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update persistent OpenClaw project tracking files such as dev_Project.md.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
