## Description:

调取全球企业资料库查询股东信息以及实际受益所有人（Beneficial Owner），梳理企业股权架构、投资关联关系，协助销售、风控人员摸清企业真实管控背景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, sales teams, and risk researchers use this skill to query overseas company shareholder information by company ID and review ownership structure, shareholder relationships, and beneficial-owner context for due diligence, investment research, competitive analysis, group-relationship mapping, and related-party checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API credentials and may persist them in local user files.

Mitigation: Use a safer secret mechanism when available, avoid commands that print ~/.upkuajing/.env, and restrict any local credential file to owner-only permissions.

Risk: Queries, key creation, recharge-order creation, and error reports may call the Upkuajing service or affect account billing workflows.

Mitigation: Confirm billable or account-affecting actions in a separate user message before running the related script.

Risk: The skill depends on a third-party service for company shareholder data and account operations.

Mitigation: Install and use the skill only when the Upkuajing service is trusted for the intended data handling and paid API use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/global-company-shareholder-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [全球企业库股东列表 API 参考](references/company-shareholder-list-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; shareholder lookup calls are paid API operations that require explicit user confirmation before execution.]

## Skill Version(s):

1.0.4 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
