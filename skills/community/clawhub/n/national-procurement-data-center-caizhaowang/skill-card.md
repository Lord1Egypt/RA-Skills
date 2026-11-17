## Description:

全国采招大数据中心-采招网，当用户需要跨省份、跨行业的全盘数据检索或综合企业画像分析时调用，需综合运用检索与企业画像接口，提供全景式的数据展现。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pkuycl](https://clawhub.ai/user/pkuycl)

### License/Terms of Use:

MIT-0

## Use Case:

面向采购、供应商和市场分析人员，按需检索中国招投标公告，并分析企业登记、投标表现与市场趋势。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Search terms and company names are sent to the service, and queries can consume account credits.

Mitigation: Limit queries to the user's requested scope and check the account balance before broad research.

Risk: Optional automatic enrollment collects device attributes, including a persistent MAC hash; saved API keys and generated login links also need protection.

Mitigation: Use an existing API key to skip enrollment when available; otherwise obtain consent before enrollment, and protect stored credentials and login links.

## Reference(s):

- [标讯搜索接口参考](artifact/references/api-search.md)
- [企业分析接口参考](artifact/references/api-company.md)
- [企业工商记录口径与边界](artifact/references/api-registry.md)
- [市场分析接口参考](artifact/references/api-market.md)
- [账户查询接口参考](artifact/references/api-account.md)
- [可选账户注册流程](artifact/references/auto-register.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [中文 Markdown 摘要、表格和说明文字]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.11 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
