## Description:

依托 LinkedIn 数据，结合人员与企业信息调取校友及离职前员工清单，挖掘彼此共同求学背景和过往任职关联，发掘潜在商务合作机会。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

招聘人员、销售团队和 B2B 线索构建者可用此技能按人员 ID 与学校 ID 查询 LinkedIn 校友关系，扩展人才寻源、院校关系研究和商务线索清单。该技能需要 Upkuajing API 凭据，且查询和分页调用可能产生费用。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid Upkuajing API credential and billable LinkedIn alumni lookup calls.

Mitigation: Confirm each paid lookup, pagination request, recharge action, or pricing check before allowing the agent to run the related command.

Risk: The API key may be persisted in ~/.upkuajing/.env and could be exposed if the file is printed or left with broad permissions.

Mitigation: Prefer an environment variable or presence-only credential check, never print ~/.upkuajing/.env, and restrict the file permissions if the skill creates it.

Risk: Error reports may include sensitive request context if the agent sends raw request or response details.

Mitigation: Review and minimize error-report context before submission, and avoid including sensitive request or response data.

Risk: The skill performs platform housekeeping calls such as version checks in addition to the requested lookup.

Mitigation: Review network activity expectations before use and install only if those platform calls are acceptable.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/upkuajing/skills/linkedin-person-alumni-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing API pricing](https://www.upkuajing.com/web/openapi/price.html)
- [领英校友列表 API 参考](references/linkedin-person-alumni-list-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; API responses include alumni data, fee information, and request identifiers.]

## Skill Version(s):

1.0.5 (source: release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
