## Description:

AI-powered shopping assistant that searches for products by text or image and finds prices across Amazon, Google Shopping, and brand stores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archroad](https://clawhub.ai/user/archroad)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and shopping agents use ShopGeni to search for products by text or image, compare prices across supported retailers, and present recommendations or ranked purchase options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping queries and selected product images may be sent to the ShopGeni/BeyondStyle backend.

Mitigation: Use the skill only for queries and images intended for that service, and avoid private files or sensitive photos with --image.

Risk: The API endpoint can be changed with SHOPGENI_API_URL or --api-url.

Mitigation: Check the effective API URL before running the helper and use only the default endpoint or another trusted endpoint.

Risk: The helper creates a persistent per-installation identifier.

Mitigation: Review this behavior before installing or running the skill in shared, privacy-sensitive, or managed environments.

## Reference(s):

- [ShopGeni ClawHub Skill Page](https://clawhub.ai/archroad/skills/online-price-comparison)
- [archroad ClawHub Publisher Profile](https://clawhub.ai/user/archroad)
- [Default ShopGeni API Endpoint](https://nestor-api.beyondstyle.us)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JSON from the helper script, typically summarized as Markdown tables or bullet lists by the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes assistant response text, thread_id, recommendations, and price-comparison candidates when available.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
