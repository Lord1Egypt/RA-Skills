## Description:

根据项目阶段判断制造能力层级，实现从技术原型到量产的供应链精准匹配。

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External OPC community members and procurement operators use this skill to diagnose manufacturing needs by project stage, choose internal collaboration or external supplier sourcing, compare quotes, negotiate terms, and document supplier engagement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplier forms can expose contact details, technical parameters, designs, BOMs, budgets, and delivery requirements.

Mitigation: Verify each recipient, share only the minimum required details, and use an NDA before disclosing confidential technical or commercial information.

Risk: Procurement recommendations, quote comparisons, and contract checklists may be incomplete for a specific organization or jurisdiction.

Mitigation: Route supplier selection, contract terms, payment terms, and external disclosure through the organization's procurement, legal, and approval processes.

Risk: The workflow is written for Chinese-language procurement operations and may be misapplied by teams that cannot review the forms accurately.

Mitigation: Use qualified language support or localized review before relying on generated supplier documents.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/golngod/skills/opc-supply-chain-matching)
- [OPC platform](https://opc.cn)
- [供应链需求诊断指南](references/01-供应链需求诊断指南.md)
- [内循环协作机制](references/02-内循环协作机制.md)
- [外循环供应商管理](references/03-外循环供应商管理.md)
- [供应商对接SOP](references/04-供应商对接SOP.md)
- [成本控制与议价策略](references/05-成本控制与议价策略.md)
- [供应链需求诊断单](templates/需求诊断单.md)
- [供应商需求单](templates/供应商需求单.md)
- [供应商报价比较表](templates/报价比较表.md)
- [采购合同](templates/采购合同.md)
- [交付验收报告](templates/验收报告.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance and reusable Chinese-language procurement templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces supplier matching guidance, comparison tables, contract checklists, and acceptance-report templates.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
