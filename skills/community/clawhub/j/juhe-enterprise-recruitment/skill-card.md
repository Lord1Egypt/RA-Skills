## Description:

根据企业全名、注册号或统一社会信用代码查询企业在招职位，并返回岗位、薪资、地点、要求、招聘人数、职位描述和来源链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to help users look up recruitment listings for a specific enterprise by company name, registration number, or unified social credit code. It is suited for presenting current job openings, salary ranges, work locations, requirements, hiring counts, descriptions, and source links from Juhe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends company identifiers to Juhe for recruitment lookup.

Mitigation: Use the skill only when the user is comfortable with Juhe processing the company identifier.

Risk: The skill handles a Juhe API key.

Mitigation: Prefer a managed JUHE_ENTERPRISE_RECRUITMENT_KEY environment variable, avoid passing the key on the command line or in URLs, and do not commit scripts/.env.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-enterprise-recruitment)
- [Juhe Enterprise Recruitment API documentation](https://www.juhe.cn/docs/api/id/852)
- [Juhe](https://www.juhe.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown-style query results with command examples and structured JSON from the script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Juhe API key, preferably supplied through JUHE_ENTERPRISE_RECRUITMENT_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
