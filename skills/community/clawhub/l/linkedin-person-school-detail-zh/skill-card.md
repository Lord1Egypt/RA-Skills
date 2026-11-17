## Description:

从 LinkedIn 数据按学校 ID 查询学校名称、类型、地理位置、网站与社交媒体链接等详细信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, researchers, analysts, and agents use this skill to verify educational institutions, enrich organization records, and inspect academic relationship data from LinkedIn-derived school records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an Upkuajing API key and may store it under `~/.upkuajing/.env`.

Mitigation: Use a dedicated API key, keep the `.env` file out of chats and logs, and restrict local file permissions before running the scripts.

Risk: School lookup API calls can incur per-call charges after user confirmation.

Mitigation: Confirm the exact query and current pricing before execution, and do not run paid calls until the user confirms in a separate message.

Risk: Error reports can upload request context and response details to the platform.

Mitigation: Review report contents for sensitive information and submit reports only after user confirmation.

## Reference(s):

- [LinkedIn 学校详情 API 参考](references/linkedin-school-detail-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)
- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/linkedin-person-school-detail-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer portal](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup output includes school detail data, fee information, and request identifiers when returned by the API.]

## Skill Version(s):

1.0.5 (source: server evidence release.version and SKILL.md metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
