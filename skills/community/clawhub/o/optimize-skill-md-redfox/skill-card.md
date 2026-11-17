## Description:

按照《Skills MD 标准书写格式》对现有 SKILL.md 进行结构化优化，提升描述质量、章节组织、内容简洁度和格式规范性。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit and standardize SKILL.md files, including frontmatter descriptions, section structure, concise content, formatting, and required authentication guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can add RedFox API-key instructions to other skills, even when those instructions are unrelated to the target skill.

Mitigation: Review generated SKILL.md changes before accepting them and remove unrelated credential guidance from skills that do not use RedFox.

Risk: The bundled record script reports usage to a third-party endpoint after each run.

Mitigation: Prefer a local-only version with telemetry removed, or disable the reporting script before deployment.

## Reference(s):

- [Skills MD Standard Format](artifact/references/standard-format.md)
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/optimize-skill-md-redfox)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and concise change summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to SKILL.md and provide validation statistics.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
