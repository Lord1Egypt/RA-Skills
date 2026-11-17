## Description:

Skill/Agent发布前的标准化质量把控工具，确保产出经过案例支撑、一致性和合规检查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and OPC creators use this skill to review a Skill or Agent before release, major version updates, marketplace evaluation, or IP preparation. It guides quality checks for case coverage, consistency, differentiation, commercialization, IP compliance, and safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is written in Chinese and is specific to an OPC-oriented release workflow, which may make the checklist or templates easy to misapply in other teams or languages.

Mitigation: Translate and adapt the templates before operational use, and confirm that thresholds and review steps match the target release process.

Risk: Optional integrations that update IP or management records could affect authoritative business records if granted write access without review.

Mitigation: Review each integration separately and grant only the minimum required permissions after the write behavior is understood.

Risk: Checklist outputs may be mistaken for final legal, IP, commercialization, or safety approval.

Mitigation: Use the generated reports as review inputs and require accountable human approval before release or IP submission.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/golngod/skills/hutian-opc-pre-publish-check)
- [发布前自查向导](README.md)
- [Prompt迭代文档模板](references/Prompt迭代文档模板.md)
- [一致性检测方法](references/一致性检测方法.md)
- [创新点提炼模板](references/创新点提炼模板.md)
- [发布前自查评分表](references/发布前自查评分表.md)
- [商业化审核与校正手册](references/商业化审核与校正手册.md)
- [竞品分析与卡位方法](references/竞品分析与卡位方法.md)
- [Coze Platform](https://coze.cn)
- [OPC Platform](https://opc.cn)

## Skill Output:

**Output Type(s):** [guidance, markdown, analysis, configuration]

**Output Format:** [Markdown checklists, report templates, scoring tables, and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown-only skill guidance; security evidence reports no executable code or hidden high-risk behavior.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
