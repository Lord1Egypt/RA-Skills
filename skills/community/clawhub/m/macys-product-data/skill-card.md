## Description:

Search and browse Macy's products, track prices, read reviews, and check store pickup availability using structured product data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and shopping assistants can find Macy's products, compare current and sale prices, review customer feedback, and check pickup options near a location.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Store lookup can involve sharing a ZIP code, coordinates, or city and state with Scavio.

Mitigation: Use store lookup only when needed and provide only the location detail required for the search.

Risk: API requests use the SCAVIO_API_KEY credential.

Mitigation: Keep the key in an environment variable or secret store and out of source code.

## Reference(s):

- [Scavio Macy's API documentation](https://scavio.dev/docs/macys-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data)
- [Scavio Macy's API overview](https://scavio.dev/macys-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data)

## Skill Output:

**Output Type(s):** [JSON data, Guidance]

**Output Format:** [Structured JSON responses with Markdown usage instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product, price, review, store, pickup, and autocomplete data; nine endpoints at one credit per call.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
