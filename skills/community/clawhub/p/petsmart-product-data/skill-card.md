## Description:

Search PetSmart products and deals, compare prices and Autoship offers, and check nearby stores and live stock through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to retrieve PetSmart product details, national prices, Autoship offers, nearby store information, stock counts, and current deals.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Lookup terms and any ZIP code provided are sent to Scavio, and requests consume API credits.

Mitigation: Send only the lookup and location details needed, and monitor the account's credit balance.

Risk: An exposed SCAVIO_API_KEY could allow unauthorized API requests that use credits.

Mitigation: Keep the key in an environment variable or secret store and out of committed source files.

Risk: Prices and store inventory can change after a response is fetched.

Mitigation: Fetch current data again before relying on a price or stock count.

## Reference(s):

- [PetSmart API overview](https://scavio.dev/petsmart-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data)
- [PetSmart search documentation](https://scavio.dev/docs/petsmart-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data)
- [PetSmart product documentation](https://scavio.dev/docs/petsmart-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data)
- [PetSmart stores documentation](https://scavio.dev/docs/petsmart-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data)
- [PetSmart store stock documentation](https://scavio.dev/docs/petsmart-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data)
- [PetSmart availability documentation](https://scavio.dev/docs/petsmart-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data)
- [PetSmart deals documentation](https://scavio.dev/docs/petsmart-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=petsmart-product-data)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON responses with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Endpoint-specific product, pricing, promotion, store, and stock data; each endpoint call uses one API credit.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
