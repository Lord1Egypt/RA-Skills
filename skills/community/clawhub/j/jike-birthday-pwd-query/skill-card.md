## Description:

生日密码 - 即刻数据帮助代理按 MM-DD 生日查询幸运、健康、建议、名人、塔罗、箴言、优点和缺点信息，数据由即刻数据开放接口提供。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to answer birthday-related cultural, lifestyle, or compatibility queries from an MM-DD date. The skill runs a Python command that calls the Jike API and returns Chinese text by default or JSON when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A modified runtime environment can set JIKE_API_BASE_URL so the AppKey is sent to an unexpected server.

Mitigation: Run the skill only in trusted environments and keep JIKE_API_BASE_URL unset or restricted to https://api.jikeapi.cn.

Risk: The Jike AppKey is a secret and is sent in the request URL.

Mitigation: Use a dedicated low-privilege key where possible, avoid sharing command output or logs that may include request URLs, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jikeapi-cn/skills/jike-birthday-pwd-query)
- [Jike API Homepage](https://www.jikeapi.cn/)
- [Birthday Password API Endpoint](https://api.jikeapi.cn/v1/birthday/pwd)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Plain text or JSON from a Python CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AppKey through JIKE_BIRTHDAY_PWD_QUERY_KEY or JIKE_APPKEY; accepts an optional birthday in MM-DD format.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
