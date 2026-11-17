## Description:

融合 Hermes Agent 与 JiuwenClaw 精华的自进化多Agent协作系统，让 OpenClaw 的多Agent工作流具备闭环学习、自动技能沉淀、技能自纠错、上下文瘦身、分层记忆与事件驱动协同能力。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gray163](https://clawhub.ai/user/gray163)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run a Chinese-language project-manager workflow for complex OpenClaw tasks, coordinating executor, supervisor, and QA roles while preserving reusable lessons in memory and skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may persist memories or create and modify SKILL.md files, changing future agent behavior.

Mitigation: Require explicit approval and diff review before every memory or SKILL.md write, and keep generated skills as drafts until reviewed.

Risk: Broad delegation and self-evolving behavior may introduce unexpected guidance into later tasks.

Mitigation: Deploy only when this workflow is intended, review generated instructions before reuse, and monitor delegated work before accepting results.

Risk: Sensitive data could be captured in memory or skill artifacts during experience consolidation.

Mitigation: Avoid processing secrets through the workflow and remove sensitive content before allowing persistence.

Risk: Installer behavior may vary if the installer version is not controlled.

Mitigation: Pin or otherwise verify the installer version before installation.

## Reference(s):

- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [JiuwenClaw](https://gitcode.com/openJiuwen/jiuwenclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow guidance that may propose or direct memory updates, skill creation, skill edits, task delegation, and status reporting.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
