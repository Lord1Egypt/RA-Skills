## Description:

管理雄韬 XTOCN CRM 客户数据：新增客户（支持企查查/天眼查文本解析）、查询客户（精确/模糊/分页）、修改客户工商信息与联系方式（PATCH 语义）、设置分类标签（分组/等级/行业/来源）。同时支持线索、联系人、跟进记录的创建与查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xtoyun](https://clawhub.ai/user/xtoyun)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and CRM operators use this skill to create, search, update, and classify XTOCN CRM customer records, leads, contacts, and follow-up records while preserving confirmation gates for write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates on live XTOCN CRM records and can create or modify customers, tags, leads, contacts, and follow-up records.

Mitigation: Install it only for users who should access the live CRM and require human review before write operations.

Risk: OPENCRM_KEY provides authenticated CRM access.

Mitigation: Use a least-privilege key and do not print, share, or expose the token in agent responses.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xtoyun/skills/opencrm)
- [Field Reference](references/fields.md)
- [XTOCN OpenCRM API Base](https://my.xtocn.com/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENCRM_KEY for live CRM access.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
