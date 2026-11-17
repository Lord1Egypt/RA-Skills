## Description:

Fetches a full MPSTATS product card for one Ozon Russia SKU, including price, discount, rating, reviews, stock, sales, revenue, listing date, delivery scheme, and image fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve and summarize marketplace metrics for a single known Ozon SKU, including competitor product checks, stock-out impact review, fulfillment comparison, and period-over-period sales comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports sensitive onboarding, credential, billing, storage, and automatic feedback behaviors.

Mitigation: Install only after reviewing those behaviors and confirming that LinkFox handling product queries and related account or billing workflows is acceptable.

Risk: Endpoint and credential settings can affect where requests and API keys are sent.

Mitigation: Verify endpoint environment variables are not overridden, avoid sharing SMS codes unless registration or login is intended, and avoid storing API keys in shell startup files.

Risk: Billing flows can create payment orders and display payment QR codes or links.

Mitigation: Review the selected package, payment method, amount, and order details before scanning or opening any payment QR code or URL.

Risk: Local linkfox output folders may contain full API responses and payment artifacts.

Mitigation: Treat local linkfox data folders as sensitive and avoid sharing them without review.

## Reference(s):

- [MPSTATS Ozon Product Detail API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-mpstats-ozon-product-detail)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown-facing summaries with JSON API responses and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes full API responses to local linkfox session data, uses a 24-hour local cache for repeated parameters, and summarizes large responses unless inline output is requested.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
