## Description:

依托全球企业数据库，结合姓名、任职公司、所属行业以及个人资料 URL 筛选目标人员，助力外贸从业者找到采购负责人、企业对接人员以及高层决策人。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

招聘人员、销售团队和 B2B 线索构建者可用该技能按姓名、公司、行业、国家和档案 URL 查找全球公司数据库中的人员记录。它适合候选人寻源、客户联系人发现和联系数据丰富工作流。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed if the local credential file is printed or stored with broad permissions.

Mitigation: Use a secure environment variable when possible, avoid displaying the key, and keep ~/.upkuajing/.env owner-only if file storage is used.

Risk: People-search results may contain sensitive contact or profile information.

Mitigation: Use the skill only for lawful, appropriate recruiting, sales, or B2B contact discovery, and delete stored task_data results when they are no longer needed.

Risk: Normal searches can incur paid API charges.

Mitigation: Confirm pricing and expected call volume before running searches, especially when the requested result count requires multiple API calls.

## Reference(s):

- [全球企业库人物列表 API](references/global-company-person-list-api.md)
- [Skill 异常上报 API](references/skill-error-report-api.md)
- [ClawHub skill release](https://clawhub.ai/upkuajing/skills/global-company-person-search-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer portal](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; executed scripts return JSON summaries and JSONL result files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY. Searches are paid API calls and may store people-search results under task_data.]

## Skill Version(s):

1.0.3 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
