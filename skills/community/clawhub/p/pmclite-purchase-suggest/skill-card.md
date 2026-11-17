## Description:

按未完工工单的 BOM 需求汇总未来物料净缺口，给出建议采购量并标明在途物料是否赶得上需求。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengjinfa](https://clawhub.ai/user/zhengjinfa)

### License/Terms of Use:

MIT-0

## Use Case:

采购人员可用此技能核对未来工单的物料缺口、建议补货量和在途物料到货情况，以便准备采购计划。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan had medium confidence and did not fully inspect assets/icon.png, leaving some release evidence incomplete.

Mitigation: Consider whether that inspection uncertainty is acceptable before installing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhengjinfa/skills/pmclite-purchase-suggest)
- [MRP-PMC installation and MCP guide](references/install.md)
- [MRP-PMC official website](https://www.pmclite.com)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Chinese Markdown with per-material shortage and suggested purchase quantities]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the requested planning horizon; explains that supplier lead times and minimum order quantities are not included.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
