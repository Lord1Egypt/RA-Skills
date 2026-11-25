## Description:

Query Instacart store, product, pricing, category, sale, pickup, suggestion, and review data across the United States and Canada, including location-specific price comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current Instacart product and store information for a ZIP code or Canadian postal code. It supports comparing product prices by store and reading related product, availability, sale, and pickup details.

### Deployment Geography for Use:

United States and Canada

## Known Risks and Mitigations:

Risk: Using the service sends the API key and request data to Scavio; the security assessment describes a benign but partial scan with a limited tool-misuse check.

Mitigation: Use the service only if you trust Scavio, keep the API key in an environment variable or secret store, and avoid including sensitive information in requests.

## Reference(s):

- [Scavio Instacart API overview](https://scavio.dev/instacart-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api)
- [Instacart price comparison endpoint](https://scavio.dev/docs/instacart-price-compare?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api)
- [Instacart product endpoint](https://scavio.dev/docs/instacart-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=instacart-api)

## Skill Output:

**Output Type(s):** [JSON data, Guidance]

**Output Format:** [Structured JSON responses with concise product and price summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested endpoint, store, location, and service type.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
