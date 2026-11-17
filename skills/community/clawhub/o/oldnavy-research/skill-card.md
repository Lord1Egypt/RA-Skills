## Description:

Researches Old Navy, Gap, Banana Republic, and Athleta products, reviews, and local pickup availability using the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shopping assistants and their users can search storefront catalogs, compare product details and reviews, find nearby stores, and check in-store pickup availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product searches and location queries are sent to the third-party Crawlora service.

Mitigation: Only share the product identifiers and location details needed for the user's requested lookup.

Risk: Exposure of the Crawlora API key could allow unauthorized use.

Mitigation: Keep CRAWLORA_API_KEY in the environment; do not publish it or include it in queries.

Risk: Uncommon search terms can return recommended products rather than true matches.

Mitigation: Check product details and relevance before presenting results as matches.

## Reference(s):

- [Old Navy research endpoint reference](reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/oldnavy-research)
- [Crawlora API service](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Concise text or structured JSON product and store results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes catalog listings, color and size options, prices, reviews, nearby stores, and pickup stock when requested.]

## Skill Version(s):

1.0.17 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
