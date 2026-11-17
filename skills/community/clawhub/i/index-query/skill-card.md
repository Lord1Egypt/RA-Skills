## Description:

查询证券指数的基础信息、成分股、收益风险、估值、基本面和行情，并以适合普通投资者的方式说明数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[e-fintech](https://clawhub.ai/user/e-fintech)

### License/Terms of Use:

MIT-0

## Use Case:

投资者和使用智能体的用户可检索、筛选和比较证券指数，查看成分、估值与最新行情。结果用于信息查询，不构成投资建议，也不能替代基金产品数据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs an API key stored in a local plaintext file and sends requests to the provider's HTTPS API.

Mitigation: Install only if comfortable with those access requirements; protect the credential with filesystem permissions and use --skip-api-verify to avoid the setup-time connectivity check.

Risk: Stale or incomplete market data can mislead investors if presented as current or as investment advice.

Mitigation: State the data date or quote time and any missing data; present factual comparisons with the required disclaimer, not buy or sell recommendations.

## Reference(s):

- [ClawHub index-query release](https://clawhub.ai/e-fintech/skills/index-query)
- [指数直通车 AI Skills 帮助文档](https://cdn.efunds.com.cn/eda/h5/itcenter/pd/ai-skills-doc/help.pdf)
- [指数查询接口与字段参考](artifact/references/catalog-index.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese-language Markdown prose, lists and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes data dates or quote times, measurement context and a non-advice disclaimer.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata; bundled artifact labels itself 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
