## Description:

驱动轻排 MRP-PMC 桌面程序完成工单排程、交期评审、插单评估与物料齐套检查；排程结果可解释、可复现，写库前必须经用户确认。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengjinfa](https://clawhub.ai/user/zhengjinfa)

### License/Terms of Use:

MIT-0

## Use Case:

生产计划人员可用此技能查询工单与生产看板、预演排程、评审交期、检查物料齐套、评估插单并记录报工；所有写入操作都需先取得用户明确确认。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence notes a possible mismatch between bulk-import scope and the skill's stated purpose.

Mitigation: Review the import scope and schema before importing, and require explicit user confirmation for the write.

Risk: The security scan had medium confidence and did not fully inspect one image, so its evidence is incomplete.

Mitigation: Review the uninspected image and relevant release files before deployment.

## Reference(s):

- [轻排 MRP-PMC 官网](https://www.pmclite.com)
- [安装与 MCP 接入指南](artifact/references/install.md)
- [ClawHub 技能页面](https://clawhub.ai/zhengjinfa/skills/pmclite-scheduler)
- [发布者资料](https://clawhub.ai/user/zhengjinfa)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown tables with concise explanations and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduling conclusions depend on connected MRP-PMC data; database writes require explicit user confirmation.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
