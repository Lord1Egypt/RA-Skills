## Description:

Search JCPenney product, deal, coupon, store-stock, review, and Q&A data through Scavio and return structured results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and shopping research agents can search JCPenney products and deals, compare prices and coupons, check nearby store availability, and retrieve product reviews and questions with source labels.

### Deployment Geography for Use:

United States and Puerto Rico

## Known Risks and Mitigations:

Risk: Product and location lookup details are sent to Scavio, including the ZIP code used for nearby store availability.

Mitigation: Use location lookup only when needed and avoid sharing a location if its disclosure to Scavio is not acceptable.

Risk: The security scan was partial, so the benign verdict has medium confidence and does not establish that every aspect was reviewed.

Mitigation: Review the skill and relevant references before use; treat the scan result as limited rather than comprehensive.

## Reference(s):

- [Scavio JCPenney product API documentation](https://scavio.dev/docs/jcpenney-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data)
- [Scavio JCPenney API overview](https://scavio.dev/jcpenney-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON product and retail data with concise summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live prices, coupons, reviews, and stock data reflect the API response; store lookup uses a ZIP code or coordinates.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
