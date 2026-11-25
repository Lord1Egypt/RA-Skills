## Description:

为法律工作者识别 AI harness，并安全生成、增量合并和核对 AGENTS.md/CLAUDE.md。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT-0

## Use Case:

法律工作者可用此技能为 AGENTS.md 或 CLAUDE.md 建立和更新 AI 协作基线，选择合适的平台与项目范围，并记录配置和人工核对状态。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a possible consent bypass when updating an existing configuration.

Mitigation: Review the proposed diff and confirm the intended changes before writing to an existing configuration.

Risk: The security review says some scripts and references were only partly analyzed.

Mitigation: Review the relevant scripts and references before installation, especially those used for file writes or shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cat-xierluo/skills/legal-harness-init)
- [Project homepage](https://github.com/cat-xierluo/legal-skills)
- [支持矩阵与完整示例](artifact/references/23-support-and-walkthrough.md)
- [隐私与上下文](artifact/references/18-privacy-and-context.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration files, Shell commands, Guidance]

**Output Format:** [Markdown instructions and AGENTS.md/CLAUDE.md configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports configuration and declared verification status; behavior verification requires trusted runtime evidence.]

## Skill Version(s):

0.5.3 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
