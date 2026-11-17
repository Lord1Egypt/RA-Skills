## Description:

Provides structured grocery data for Kroger, QFC, and Fred Meyer, including product search and details, store-level prices, store lookup, weekly deals, coupons, and search suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use the skill to find grocery products, store-specific prices and availability, product details, nearby stores, weekly deals, and digital coupons across supported Kroger banners.

### Deployment Geography for Use:

United States (Kroger nationwide; QFC in Washington and Oregon; Fred Meyer in the Pacific Northwest and Alaska).

## Known Risks and Mitigations:

Risk: Grocery search terms and, when supplied, ZIP code, city, or store details are shared with Scavio; the security evidence notes a privacy disclosure gap.

Mitigation: Review Scavio's privacy practices and avoid sharing location details that are not needed for the request.

Risk: The security scan was partial because some local path-like references could not be resolved, leaving the assessment incomplete.

Mitigation: Review the skill and its referenced resources before relying on it in a sensitive environment.

## Reference(s):

- [Scavio Kroger search documentation](https://scavio.dev/docs/kroger-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data)
- [Scavio Kroger API overview](https://scavio.dev/kroger-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data)
- [ClawHub release page](https://clawhub.ai/scavio-ai/skills/kroger-grocery-data)

## Skill Output:

**Output Type(s):** [JSON data, Guidance]

**Output Format:** [Structured JSON data with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices are integer cents and refer to a specific store; availability and promotions can change.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
