## Description:

Chinese-language OPC customer-acquisition subcontracting workflow support for project posting, bidding, subcontract matching, contracts, delivery milestones, settlement, and reputation updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External OPC mentors, entrepreneurs, community operators, and project leads use this skill to structure customer-acquisition subcontracting workflows from demand intake through bidding, modular subcontracting, agreement generation, milestone acceptance, settlement, and mutual evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow covers bid awards, credit changes, public postings, account freezes, document writes, and settlement or payment steps.

Mitigation: Require explicit human approval before any of those actions are executed or treated as final.

Risk: Generated contracts and settlement documents may include customer, contact, banking, invoice, tax, and reputation data.

Mitigation: Apply privacy rules, minimize sensitive fields, and keep generated outputs in a dedicated restricted folder.

Risk: Scoring and matching helpers influence bid ranking, subcontract allocation, and reputation outcomes.

Mitigation: Validate inputs and review scoring results before using them for awards, payouts, or credit updates.

Risk: The artifact is designed for a Chinese-language OPC subcontracting process and may not match other legal or business contexts.

Mitigation: Use it only for the intended workflow and have contracts, settlement rules, and dispute handling reviewed by qualified operators before live deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/opc-customer-acquisition-platform)
- [项目挂榜指南](artifact/references/01-项目挂榜指南.md)
- [接榜挂帅竞标规则](artifact/references/02-接榜挂帅竞标规则.md)
- [项目分包机制](artifact/references/03-项目分包机制.md)
- [签约流程与协议体系](artifact/references/04-签约流程与协议体系.md)
- [执行交付与里程碑管理](artifact/references/05-执行交付与里程碑管理.md)
- [分账结算与纠纷处理](artifact/references/06-分账结算与纠纷处理.md)
- [评价沉淀与信用更新](artifact/references/07-评价沉淀与信用更新.md)
- [Skill矩阵整合接口](artifact/references/08-Skill矩阵整合接口.md)
- [冷启动运营手册](artifact/references/09-冷启动运营手册.md)
- [OPC platform](https://opc.cn)
- [Coze platform](https://coze.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown templates, structured text, Python-generated reports, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include contract templates, scoring reports, project workflow checklists, generated files, and operational guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
