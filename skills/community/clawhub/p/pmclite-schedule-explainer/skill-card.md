## Description:

把轻排给出的排程讲清楚：产线来源、工时模型、日期推导、顺延与降级原因，只读不写库。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengjinfa](https://clawhub.ai/user/zhengjinfa)

### License/Terms of Use:

MIT-0

## Use Case:

轻排 MRP-PMC 用户和排产评审人员可用它理解已有工单的产线分配、工时模型、完工日期，以及顺延或降级原因。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan is benign with medium confidence, but coverage is incomplete because the referenced icon could not be fully analyzed.

Mitigation: Review the icon and remaining unscanned component before installation.

Risk: An explanation based on incomplete or unconfirmed schedule data could misstate why an order was assigned or delayed.

Mitigation: Confirm the work order and supporting schedule fields, and state which evidence is missing instead of filling gaps with assumptions.

## Reference(s):

- [MRP-PMC installation and MCP connection guide](references/install.md)
- [Demo mode and data source notes](references/demo.md)
- [轻排 MRP-PMC 官网](https://www.pmclite.com)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown explanation with a conclusion and a breakdown table; a timeline or labeled sample may be included.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only explanations grounded in available schedule data; demonstration data is explicitly labeled as a sample.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
