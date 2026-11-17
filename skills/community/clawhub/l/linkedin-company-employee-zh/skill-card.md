## Description:

调取 LinkedIn 企业主页数据获取员工清单与整体人员规模，剖析企业内部组织架构，挖掘潜在商务联系人以及核心岗位决策人员。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, sales teams, and B2B lead builders use this skill to retrieve LinkedIn-sourced employee lists and job titles for a known company ID. It supports talent research, organization analysis, team-structure checks, and lead qualification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Upkuajing API key and may read or create a local credential file.

Mitigation: Use a managed secret mechanism where possible, avoid printing or pasting the API key, and restrict file permissions on the local credential file.

Risk: Employee lookup and pagination calls can incur charges.

Mitigation: Confirm paid API use in a separate user message before each chargeable call and check current pricing through the documented pricing endpoint or pricing page.

Risk: Recharge and diagnostic-reporting flows can send account, request, or troubleshooting data to the provider.

Mitigation: Review payment URLs and diagnostic payloads before use, and send error reports only after explicit user approval.

Risk: The skill performs a version check and writes a local version cache.

Mitigation: Review this network call and local cache behavior before deployment in environments with strict outbound-network or persistence controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/linkedin-company-employee-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [领英员工列表 API 参考](references/linkedin-company-employee-list-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Employee list responses include pagination cursor, employee identifiers, title names, fee information, and request IDs when returned by the API.]

## Skill Version(s):

1.0.3 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
