## Description:

调用 Sorftime 研究 Walmart 美国站类目：获取完整类目树、按自然语言类目名称匹配相关 NodeId，或使用下划线分隔的 NodePath 查询类目市场数据及 Best Seller Top 80。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce researchers and operators use this skill to inspect Walmart US category hierarchy, match category names to NodeId values, and summarize category market reports with Best Seller Top 80 data.

### Deployment Geography for Use:

Global; data coverage is Walmart US.

## Known Risks and Mitigations:

Risk: The skill requires LinkFox API credentials and can expose them through setup flows or shell history if handled carelessly.

Mitigation: Store API keys in a proper secret manager or protected environment configuration, and avoid placing secrets in logs or shared shell profiles.

Risk: The onboarding flow can request phone verification codes and create payment orders.

Mitigation: Only enter verification codes or create orders when the user explicitly intends to authenticate or purchase credits, and review plan, amount, and payment method before proceeding.

Risk: Category tree and market report requests consume paid Sorftime or LinkFox credits.

Mitigation: Run one operation at a time, rely on the documented cache where appropriate, show cost fields when returned, and ask for user authorization before retries or additional operations.

Risk: The skill may send feedback reports when behavior or results mismatch intent.

Mitigation: Review feedback payload content before it is sent, especially in environments with data handling or customer confidentiality requirements.

Risk: Search results are related category matches and may not be exact classifications.

Mitigation: Confirm NodeId and nodePath before running a market report, and label Best Seller output as a maximum Top 80 scope rather than a full catalog.

## Reference(s):

- [Walmart Category Market API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-sorftime-walmart-category-market)
- [Publisher Profile](https://clawhub.ai/user/linkfox-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with JSON responses and saved response files; shell commands and configuration guidance when setup is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state the selected operation, returned requestConsumed and costToken values, compact category or market metrics, and avoid dumping large category trees into conversation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
