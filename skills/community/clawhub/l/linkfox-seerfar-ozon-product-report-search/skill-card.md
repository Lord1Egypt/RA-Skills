## Description:

Searches Seerfar Ozon product reports and returns product-level rows filtered by sales, revenue, growth, conversion, price, rating, reviews, brand, seller, fulfillment, listing age, margin, returns, and related metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, marketplace analysts, and developers use this skill to screen Ozon products by product-report metrics and inspect comparable product rows for selection, competitor analysis, best-seller mining, and price or conversion-band filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires LinkFox account credentials or API keys to access the product-report service.

Mitigation: Install only if sharing those credentials with this skill is acceptable, and prefer session or environment-specific secrets over broadly persisted shell startup configuration.

Risk: Product-search results and cache entries can be written to local workspace storage.

Mitigation: Review saved LinkFox output directories for sensitive commercial data and remove cached or persisted files when they are no longer needed.

Risk: Queries consume paid LinkFox compute credits and the artifact includes payment and billing onboarding flows.

Mitigation: Confirm expected credit use before repeated calls, and require explicit user approval before creating purchase orders or continuing after billing errors.

Risk: The release evidence reports under-scoped automatic feedback behavior.

Mitigation: Do not allow automatic feedback submission unless the exact feedback payload and reason are visible and acceptable to the user.

## Reference(s):

- [Seerfar Ozon Product Report Search API Reference](artifact/references/api.md)
- [Authentication and Billing Onboarding](artifact/references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-seerfar-ozon-product-report-search)
- [LinkFox Publisher Profile](https://clawhub.ai/user/linkfox-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown summaries or tables with optional shell commands and persisted JSON response files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large responses may be summarized while the full response is saved locally; authentication or billing failures may produce setup guidance.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
