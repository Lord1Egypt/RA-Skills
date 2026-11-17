## Description:

通过同花顺问财按估值、资金流向、涨跌幅等条件筛选中国市场板块并展示结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee)

### License/Terms of Use:

MIT

## Use Case:

投资研究用户用自然语言筛选中国市场的行业、概念或地域板块，查看符合估值、资金流向和涨跌幅等条件的板块数据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screening queries and an API key are sent to the documented iWencai service.

Mitigation: Use a private, appropriately scoped API key and omit sensitive personal or account information from queries.

Risk: Market-screening results may be mistaken for investment advice.

Mitigation: Treat returned market data as informational and verify it before making financial decisions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/chen6896qqwee/skills/hithink-sector-selector)
- [同花顺问财数据查询](https://www.iwencai.com/unifiedwap/chat)
- [同花顺问财 SkillHub](https://www.iwencai.com/skillhub)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown table with brief explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the final screening query and credits 同花顺问财 as the data source.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
