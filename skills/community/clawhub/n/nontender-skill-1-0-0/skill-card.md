## Description:

国企非招标采购领域的合规辅助AI，基于用户上传的企业采购制度与招投标法规体系，辅助判定非招标采购方式的适用条件、识别依法必须招标边界与方式选择风险。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

国企采购经办人、法务合规人员、纪检监察人员和采购管理部门负责人 use this skill to check whether a non-tender procurement route is appropriate, identify mandatory tendering boundaries, and produce internal reference compliance analysis. It supports procurement method selection, risk scanning, and decision-record drafting, but does not replace the enterprise decision maker.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The workflow may request procurement rules, project facts, supplier names, exact amounts, or other sensitive procurement context.

Mitigation: Redact secrets, personal data, supplier names, exact amounts, and confidential business details before use.

Risk: Outputs may be mistaken for final procurement decisions or legal conclusions.

Mitigation: Use outputs as internal reference only and route final procurement decisions through the enterprise's responsible decision body and legal or compliance review.

Risk: Using government-procurement terminology or unsupported direct-procurement exceptions could mislead SOE procurement method selection.

Mitigation: Verify method choices against uploaded enterprise rules, the cited Chinese tendering-law framework, and the skill's direct-procurement validation checklist before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/nontender-skill-1-0-0)
- [非招标采购法规索引（P2-P5）](references/法规索引.md)
- [四种非招标采购方式对照表](references/四种采购方式对照表.md)
- [直接采购七类情形详解](references/直接采购七类情形详解.md)
- [场景路由映射表](references/场景路由映射表.md)
- [非招标采购负面案例库](references/负面案例库.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Configuration]

**Output Format:** [Markdown with structured tables, risk labels, cited source tiers, and decision-record templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory compliance references based on user-provided procurement facts and configured reference materials; users are prompted to redact sensitive procurement, supplier, personal, and amount details.]

## Skill Version(s):

1.0.0 (source: frontmatter, manifest, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
