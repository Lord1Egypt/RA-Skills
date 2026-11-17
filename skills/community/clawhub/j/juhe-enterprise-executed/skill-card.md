## Description:

企业被执行人信息查询（公示中及历史）。根据企业名称、统一社会信用代码、工商注册号或关键词查询被执行案件，返回案号、执行法院、执行标的、立案时间、案件状态。通过聚合数据（juhe.cn）API 实时查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and business users use this skill to query Juhe for Chinese enterprise enforcement records by company name, unified social credit code, registration number, keyword, case number, date range, province, or city. It helps present case numbers, executing courts, execution amounts, filing dates, current or historical disclosure status, and pagination details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup terms and the Juhe API key are sent to Juhe when the skill performs live queries.

Mitigation: Use the skill only for intended Chinese enterprise enforcement-record lookups and confirm ambiguous lookup requests before execution.

Risk: Passing the API key on the command line can expose it through shell history or process inspection.

Mitigation: Prefer the documented JUHE_ENTERPRISE_EXECUTED_KEY environment variable and avoid command-line key arguments.

Risk: Storing the API key in an unprotected .env file can expose credentials on shared systems.

Mitigation: Keep any .env file access-restricted and avoid committing or sharing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-enterprise-executed)
- [Publisher profile](https://clawhub.ai/user/juhemcp)
- [Juhe Enterprise Executed Person API documentation](https://www.juhe.cn/docs/api/id/842)
- [Juhe data service](https://www.juhe.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and JSON query results, often summarized in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the JUHE_ENTERPRISE_EXECUTED_KEY environment variable or another documented API key source.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
