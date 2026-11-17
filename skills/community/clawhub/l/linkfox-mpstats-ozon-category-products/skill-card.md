## Description:

This skill queries MPSTATS Ozon Russia category product data by full Russian category path and returns per-SKU sales, revenue, price, rating, stock, turnover, ranking, and related metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace analysts, e-commerce operators, and developers use this skill to inspect product-level performance within an Ozon Russia category for bestseller discovery, niche analysis, category ranking review, and brand landscape scanning. The skill is data-oriented and does not provide business advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses LinkFox API credentials and can guide users through account onboarding.

Mitigation: Store API keys in a secret manager or protected environment variables, avoid sharing logs that contain credentials, and verify endpoint environment variables before use.

Risk: The onboarding flow can list paid plans and create payment orders.

Mitigation: Review the selected plan, payment method, and generated order before confirming any purchase.

Risk: The skill writes full marketplace query responses and cache data to local LinkFox session directories.

Mitigation: Treat saved response files as potentially sensitive business data and remove or protect them according to the workspace retention policy.

Risk: The skill documentation describes automatic feedback reporting when results or user sentiment indicate an issue or praise.

Mitigation: Review feedback behavior before deployment and make feedback submission opt-in when user queries or results may contain sensitive information.

## Reference(s):

- [MPSTATS Ozon Category Products API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-mpstats-ozon-category-products)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API parameters, shell commands, and saved JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes complete API responses to a local LinkFox session data file; small responses may also be printed inline, and large responses are summarized.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
