## Description:

Queries MPSTATS data for Ozon Russia products under an exact brand display name, returning SKU-level sales, revenue, price, rating, stock, turnover, lost-sales, and related metrics with filters, sorting, pagination, and currency conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace analysts, e-commerce operators, and agents use this skill to retrieve brand-scoped Ozon SKU metrics for competitor audits, SKU structure analysis, bestseller review, stockout checks, and currency-normalized reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ozon brand queries, API keys, account credentials, and returned analytics can be sent to LinkFox services and analytics responses are stored locally.

Mitigation: Use only approved data, keep API keys in secure secret storage, and restrict access to the linkfox output directory.

Risk: The onboarding flow can handle account registration and paid credit purchases.

Mitigation: Review onboarding commands before execution and confirm any credit purchase with the user before ordering.

Risk: Endpoint override environment variables can redirect API and account traffic.

Mitigation: Avoid override variables unless the runtime is controlled, and verify the environment before using credentials.

Risk: Automatic feedback reporting may send usage feedback to LinkFox.

Mitigation: Review feedback payloads and organizational policy before enabling or relying on automatic reporting.

## Reference(s):

- [MPSTATS Ozon Brand Products API Reference](references/api.md)
- [Authentication and Credit Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-mpstats-ozon-brand-products)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and tables, JSON API responses, and local JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full responses are saved under a linkfox session directory; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
