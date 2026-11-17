## Description:

依托全球企业数据库查询企业员工清单与人员规模（Headcount），摸清企业内部组织架构，帮外贸销售、猎头从业者挖掘目标企业潜在对接人员。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External recruiters, sales teams, B2B lead builders, and talent researchers use this skill to retrieve a company's employee list, roles, and pagination metadata from the UpKuajing global company database. It supports prospecting, organization research, decision-maker discovery, and lead qualification when the user has a company ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use or store an UPKUAJING API key.

Mitigation: Set the API key through a secure environment or secret manager, and avoid asking the agent to print the .env file.

Risk: The skill includes paid API and recharge workflows.

Mitigation: Review and explicitly approve chargeable queries, recharge orders, and payment links before execution.

Risk: Confirmed error reports may send request context to the platform.

Mitigation: Approve error reporting only after checking that the report context does not include unnecessary sensitive data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/global-company-employee-zh)
- [UpKuajing Homepage](https://www.upkuajing.com)
- [UpKuajing Developer Platform](https://developer.upkuajing.com/)
- [UpKuajing API Pricing](https://www.upkuajing.com/web/openapi/price.html)
- [全球企业库员工列表 API 参考](references/company-employee-list-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Employee lookup results include per-record company ID, person ID, title names, pagination cursor, fee details, and request ID when returned by the API.]

## Skill Version(s):

1.0.6 (source: SKILL.md metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
