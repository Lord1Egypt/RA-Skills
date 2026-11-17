## Description:

整理已有专利著录材料，生成保留公开号、日期、责任者、来源及缺失字段的编号参考文献。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

面向整理专利资料的研究人员、研发人员和写作者，用已有专利清单制作可追溯的编号参考文献，并标出缺失字段。需要补取数据时，可在确认发送内容和预算后使用可选在线查询。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional online lookups send query or patent data to the PatentMax service and may incur charges.

Mitigation: Before enabling lookups, confirm what information will be sent and approve a spending limit.

Risk: The online client has credential-storage gaps.

Mitigation: Use optional, securely permissioned credential storage; if secure permissions cannot be confirmed, use credentials temporarily without saving them.

Risk: Candidate CSV exports may be interpreted as spreadsheet formulas.

Mitigation: Import candidate CSV files as text with formula execution disabled.

## Reference(s):

- [本地文件处理说明](references/local-workflow.md)
- [API 参考](references/api-reference.md)
- [PatentMax API 平台](https://api.ip930.com/features/api-platform)
- [PatentMax API 服务](https://api.ip930.com)

## Skill Output:

**Output Type(s):** [Files, CSV, Markdown, JSON]

**Output Format:** [CSV bibliography and source-field table, Markdown reference list, and JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source order and row references; marks missing fields and duplicate identifiers for review.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
