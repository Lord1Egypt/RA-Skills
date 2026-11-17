## Description:

Search IKEA catalogs, compare market-specific prices, inspect product details and reviews, and check store availability across supported markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can look up IKEA products, compare prices across supported countries, read product information and reviews, and check store or stock details.

### Deployment Geography for Use:

Global; IKEA data is available in 55 supported markets.

## Known Risks and Mitigations:

Risk: Lookup requests are sent to Scavio; home-delivery availability checks may share a postal code without a privacy warning.

Mitigation: Use only the product and store details needed, omit postal codes unless required, and confirm that sharing them with Scavio is acceptable.

Risk: The security review reports a benign verdict with medium confidence because scanner coverage is partial.

Mitigation: Treat the scan as incomplete and avoid sending sensitive information through the skill.

## Reference(s):

- [Scavio IKEA compare API documentation](https://scavio.dev/docs/ikea-compare?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api)
- [Scavio IKEA API overview](https://scavio.dev/ikea-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=ikea-api)
- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/ikea-api)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON data with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices are reported in each market's local currency and are not converted.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
