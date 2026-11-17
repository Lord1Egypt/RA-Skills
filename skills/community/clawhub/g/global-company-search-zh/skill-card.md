## Description:

依托全球企业数据库，通过产品品类、所属行业、企业规模筛选目标公司，助力外贸从业者挖掘潜在客户、优质供应商以及长期合作伙伴。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External sales, export, market research, and B2B sourcing users use this skill to search Upkuajing's global company database by product, company name, industry, country, contact availability, or website URL and retrieve company lead records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid Upkuajing API key and can initiate account recharge payment links.

Mitigation: Require explicit user confirmation before paid API calls, high-volume searches, or recharge order creation; use the documented pricing check rather than estimating fees.

Risk: The skill reads or creates an API key in the environment or `~/.upkuajing/.env`.

Mitigation: Set the key through a secure environment mechanism, avoid printing the full key in chat or logs, and rotate it if exposure occurs.

Risk: Diagnostic error reporting can send request context and response details to the platform.

Mitigation: Send diagnostic reports only after user confirmation and avoid including unnecessary sensitive business or credential data.

Risk: Search results may include company contact and business profile data.

Mitigation: Use results for legitimate lead research or sourcing workflows and review applicable privacy, consent, and outreach requirements before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/global-company-search-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [全球企业库公司列表 API](references/global-company-list-api.md)
- [Agent调用Skill异常上报 API](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance]

**Output Format:** [Chinese natural-language guidance, shell commands, JSON API responses, and JSONL result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; company search results are saved as task-scoped JSONL files.]

## Skill Version(s):

1.0.3 (source: evidence release and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
