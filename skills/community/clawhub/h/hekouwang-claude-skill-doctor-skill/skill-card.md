## Description:

体检 Agent Skill：默认 check.py 评 SKILL.md 触发/篇幅/渐进披露/可移植/安全；可选套件可检查项目说明文档与本机开发环境；可选 SkillSpector 深度扫描与 trigger_eval（会把 query/description 发给外部模型）；给评分卡并可代重构

This skill is ready for commercial/non-commercial use.

## Publisher:

[huiyonghkw](https://clawhub.ai/user/huiyonghkw)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to inspect Agent Skills and SKILL.md files for trigger clarity, structure, portability, and security, then receive a scorecard and practical repair guidance. Optional checks can assess related project documentation and development environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial: 17 of 19 components were fully inspected, leaving some checks incomplete.

Mitigation: Review the skill files and decide whether the available scan coverage is sufficient before installing.

Risk: The optional trigger evaluation sends query text and the tested skill description to an external model service; sensitive content could be exposed and calls may incur costs.

Mitigation: Avoid sensitive queries and descriptions, review the disclosed service and expected charges, and use isolated credentials when running the evaluation.

Risk: The Docker examples rely on image references that should be checked before use.

Mitigation: Review the image source and pinned digest before running the Docker examples.

## Reference(s):

- [Project homepage](https://github.com/huiyonghkw/hekouwang-claude-skill-doctor-skill)
- [ClawHub release page](https://clawhub.ai/huiyonghkw/skills/hekouwang-claude-skill-doctor-skill)
- [SkillSpector](https://github.com/NVIDIA/skillspector)
- [Trigger evaluation guide](references/trigger-eval.md)
- [Doctor suite guide](references/doctor-suite.md)
- [Skill writing vocabulary](references/skill-writing-vocab.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown, Guidance]

**Output Format:** [Text or JSON scorecard with Markdown repair guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional trigger evaluation sends queries and the tested description to an external model service and may incur usage costs.]

## Skill Version(s):

1.8.7 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
