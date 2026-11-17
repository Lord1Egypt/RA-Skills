## Description:

查询全球公司数据库中的学校详情，包括名称、类型、地理位置、网站和社交媒体链接，帮助核验教育机构并补充机构数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

招聘人员、研究人员和分析师可使用此技能按学校 ID 查询全球学校详情，用于学历核验、院校研究、机构数据补全和学术关系网分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses an API key from the user's environment or home directory.

Mitigation: Do not print or paste API keys in chat or terminal transcripts, and set restrictive permissions on ~/.upkuajing and its .env file.

Risk: The skill performs paid API calls and can direct users to recharge or payment URLs.

Mitigation: Confirm paid operations before execution, verify current pricing through the vendor, and review any recharge or payment URL before use.

Risk: Optional error reporting may include request context or sensitive data.

Mitigation: Ask for user confirmation before reporting errors, and decline or redact reports that would include personal or sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/global-company-person-school-detail-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [全球学校详情 API 参考](references/school-detail-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Chinese guidance with shell command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [School detail results include fee and request identifiers when the API call succeeds.]

## Skill Version(s):

1.0.3 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
