## Description:

依托 LinkedIn 数据，结合人员与企业信息检索同事和团队成员清单，梳理企业内部人际关联与组织架构，发掘可对接的潜在商务联系人。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, sales teams, and B2B lead builders use this skill to find colleagues and team members associated with a LinkedIn person and company ID, supporting relationship mapping, organization research, and contact-list expansion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Use with a real UPKUAJING_API_KEY can expose account credentials if the local environment file is printed or logged.

Mitigation: Do not print ~/.upkuajing/.env in chat or terminal logs; keep restrictive permissions on the file and use a virtual environment.

Risk: Lookup, recharge, and some account operations may affect a paid balance.

Mitigation: Run paid lookup, recharge, or error-report commands only after explicit user confirmation.

Risk: The server security summary marked the release suspicious because API keys and paid account operations deserve review before installation.

Mitigation: Review the skill before installing when it will use a real API key or paid balance.

## Reference(s):

- [LinkedIn colleague list API reference](references/linkedin-person-colleague-list-api.md)
- [Skill error report API reference](references/skill-error-report-api.md)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/linkedin-person-colleague-zh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; colleague lookup calls are paginated and paid per API call.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
