## Description:

Jiimore-商品发现 helps Amazon sellers discover keyword-matched products using Jiimore data, with filters for conversion, click growth, profitability, reviews, price, and listing age.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and e-commerce operators use this skill to query Jiimore product discovery data for keyword-driven product mining, opportunity validation, and competitive benchmarking across supported marketplaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a LinkFox API key and includes onboarding paths for account login, API-key issuance, and paid order creation.

Mitigation: Install only when LinkFox account and billing access are acceptable, confirm any plan or payment selection before order commands, and store API keys with a secret manager or similarly protected environment mechanism.

Risk: Product discovery calls consume paid compute credits and complete API responses are persisted locally.

Mitigation: Use specific queries, avoid repeated high-frequency calls without user approval, and review the local linkfox session data and cache for retained product responses.

Risk: The skill supports configurable LinkFox endpoints and automatic feedback reporting.

Mitigation: Prefer the default LinkFox endpoints unless a trusted deployment requires otherwise, and review feedback reports before sending when they may include task context.

## Reference(s):

- [Jiimore Product Discovery API Reference](references/api.md)
- [Authentication and Billing Onboarding Guide](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-jiimore-product-discovery)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with JSON request examples, shell commands, tabular product summaries, and saved JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved under a local linkfox session data directory; larger responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
