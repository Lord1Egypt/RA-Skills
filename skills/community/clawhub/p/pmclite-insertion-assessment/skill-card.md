## Description:

测算急单插入现有排程后对其他工单的影响，并比较换线等方案，支持交期决策。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengjinfa](https://clawhub.ai/user/zhengjinfa)

### License/Terms of Use:

MIT-0

## Use Case:

PMC and production-planning teams use this skill to assess whether an urgent order can fit into the current schedule, identify affected work orders and delay days, and compare alternatives such as changing production lines. It provides a preview to support delivery decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial: the referenced icon was not fully inspected, so the evidence is incomplete despite a benign verdict.

Mitigation: Consider this scan limitation when deciding whether to install.

Risk: Treating a schedule preview as a confirmed change could lead to unapproved delivery commitments.

Mitigation: Keep the result as a preview, confirm affected delivery dates, and route any schedule write to the scheduling workflow for confirmation.

## Reference(s):

- [演示模式说明](artifact/references/demo.md)
- [MRP-PMC 安装与 MCP 接入指南](artifact/references/install.md)
- [轻排 MRP-PMC 官网](https://www.pmclite.com)
- [ClawHub skill release](https://clawhub.ai/zhengjinfa/skills/pmclite-insertion-assessment)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Chinese Markdown summary with a before-and-after work-order impact table and recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview-based assessment; does not write changes to the production schedule.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
