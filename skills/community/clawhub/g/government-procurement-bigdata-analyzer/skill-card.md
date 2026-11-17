## Description:

查询并分析政府采购招投标、采购意向、企业资质与中标市场数据，帮助发现政采商机。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要跟踪政府、事业单位及央国企采购的业务人员，按需查询招标中标公告、采购意向和企业市场信息，并形成摘要、统计或竞争分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional automatic signup sends a persistent device fingerprint to the provider; its retention and deletion practices are unspecified.

Mitigation: Prefer an existing API key or manual registration. If choosing automatic signup, review the device-data notice and obtain the user's consent before proceeding.

Risk: Searches are sent to Zhiliaobiaoxun and some successful queries may consume account credits.

Mitigation: Query only the information requested and check account balance or query costs when relevant.

Risk: The API key and temporary login links can grant access to the associated account.

Mitigation: Keep keys and login links private; do not include them in user-facing results or share them in chat.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhiliaobiaoxun/skills/government-procurement-bigdata-analyzer)
- [Bid search and detail API guidance](artifact/references/api-search.md)
- [Company analysis API guidance](artifact/references/api-company.md)
- [Market analysis API guidance](artifact/references/api-market.md)
- [Account API guidance](artifact/references/api-account.md)
- [Company registry API guidance](artifact/references/api-registry.md)
- [Zhiliaobiaoxun API v2](https://mcp-server.zhiliaobiaoxun.com/api_v2/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Chinese-language summaries and analysis, with Markdown tables and links where useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query results depend on selected filters and available source records; some company and market queries consume credits.]

## Skill Version(s):

1.0.10 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
