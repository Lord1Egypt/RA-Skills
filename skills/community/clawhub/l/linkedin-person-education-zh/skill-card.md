## Description:

调取 LinkedIn 平台的用户教育履历清单，获取目标人员学历层次、毕业院校信息，梳理校友人脉网络，为客户画像搭建和商务关系挖掘提供支撑。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, HR teams, hiring managers, and business development users use this skill to retrieve LinkedIn education records for a known person ID and review schools, degrees, majors, minors, GPA, and summaries. It supports candidate screening, background review, customer profiling, and relationship discovery when the user has a valid UPKUAJING API key and confirms paid queries before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses and may store an UPKUAJING API key for authenticated third-party API calls.

Mitigation: Store only the required API key, avoid printing the full .env file in chats or logs, and rotate the key if it is exposed.

Risk: Education lookup and pagination calls are paid operations.

Mitigation: Tell the user a paid API call will occur and wait for an explicit separate confirmation before each chargeable query or pagination request.

Risk: The skill can query account balance and create recharge orders with the configured API key.

Mitigation: Confirm recharge intent separately with the user and send only the provider payment URL returned by the account script.

Risk: Optional error reporting may send request context and response details to the provider for troubleshooting.

Mitigation: Use error reporting only after user confirmation and include only information needed to diagnose the failed skill call.

## Reference(s):

- [LinkedIn人物教育经历列表 API 参考](references/linkedin-person-education-list-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)
- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/linkedin-person-education-zh)
- [upkuajing publisher profile](https://clawhub.ai/user/upkuajing)
- [跨境魔方 homepage](https://www.upkuajing.com)
- [跨境魔方开放平台](https://developer.upkuajing.com/)
- [跨境魔方开放平台价格说明](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance, Text]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns paginated education records and fee/request metadata; paid calls require explicit user confirmation.]

## Skill Version(s):

1.0.3 (source: SKILL.md metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
