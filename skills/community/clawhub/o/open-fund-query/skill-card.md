## Description:

查询并比较场外指数基金和 ETF 联接基金的基本信息、费率、持仓、收益及分红。

This skill is ready for commercial/non-commercial use.

## Publisher:

[e-fintech](https://clawhub.ai/user/e-fintech)

### License/Terms of Use:

MIT-0

## Use Case:

个人投资者和使用智能体的用户可查询中国场外指数基金与 ETF 联接基金的数据，并按规模、费率、历史表现等客观指标比较产品；不用于投资建议或交易操作。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key is stored locally and used to access the fund data service.

Mitigation: Use only if you trust the service; protect the credential file at ~/.config/index-hub/api_key and do not share the key.

Risk: Installation can replace an existing open-fund-query folder and may contact the service to verify the key.

Mitigation: Review installer options and back up existing skill files; use --skip-api-verify when remote verification is inappropriate.

Risk: Fund data or automated comparisons could be mistaken for current prices or personalized investment advice.

Mitigation: Check each fund's data date, distinguish NAV from intraday ETF prices, and avoid treating the output as a trading recommendation.

## Reference(s):

- [ClawHub 技能页面](https://clawhub.ai/e-fintech/skills/open-fund-query)
- [指数直通车使用说明](https://cdn.efunds.com.cn/eda/h5/itcenter/pd/ai-skills-doc/help.pdf)
- [场外基金查询字段与接口参考](references/catalog-oef.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with comparison tables and dated fund data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes data dates and a non-investment-advice notice.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
