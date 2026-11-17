## Description:

Search and filter independent Shopify stores by name or domain, country, store age, product count, ad count, monthly visits, monthly orders, and social follower metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce analysts, marketers, and sellers use this skill to discover Shopify stores and compare independent-store metrics for prospecting, competitor research, and market analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes LinkFox account, login, billing, and payment-order flows in addition to Shopify store querying.

Mitigation: Review those flows before installation and use them only when the user intends to create or recover an account, configure access, or buy credits.

Risk: Custom gateway or login URL environment variables could redirect requests away from trusted LinkFox services.

Mitigation: Use the default LinkFox endpoints unless a trusted administrator provides an approved override.

Risk: API keys, SMS codes, and phone numbers may be exposed if pasted into chat logs or shell startup files without care.

Mitigation: Store API keys in a proper secret manager or protected environment configuration, and share SMS codes or phone numbers only when intentionally completing LinkFox onboarding.

Risk: Queries consume credits dynamically based on returned store count, so broad filters or pagination can increase cost.

Mitigation: Warn users before running broad searches, use narrower filters and page sizes when possible, and ask for confirmation before follow-up pages.

## Reference(s):

- [Shopify Store Query API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopify-store-query)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API results and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large API responses may be saved as JSON files and summarized in text.]

## Skill Version(s):

1.0.9 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
