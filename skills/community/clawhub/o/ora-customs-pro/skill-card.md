## Description:

提供海关进出口数据查询与贸易分析，支持按 HS 编码或产品、采购商、供应商及航运记录检索。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oraagent](https://clawhub.ai/user/oraagent)

### License/Terms of Use:

MIT-0

## Use Case:

外贸分析人员可用它按产品、采购商或供应商查询海关进出口记录，并查看贸易趋势、交易明细和航运信息。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Query details and API credentials are sent to the external customs service; the security review says part of the referenced client could not be fully inspected.

Mitigation: Review the client and destination before use, narrow access, send only non-sensitive customs queries, and keep credentials out of tool output.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/oraagent/skills/ora-customs-pro)
- [Topeasy China](https://www.topeasychina.com)
- [Customs query service](https://h.smtso.com/skill/botcustoms)
- [OraSKL](https://www.oraskl.com)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Text or Markdown summaries of trade statistics, rankings, trends, and records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content varies with the selected query and may include trade metrics or shipment details.]

## Skill Version(s):

1.0.5 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
