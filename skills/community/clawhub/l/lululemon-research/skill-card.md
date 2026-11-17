## Description:

Researches Lululemon categories, products, outfits, reviews, and stores through the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and research assistants use this skill to explore Lululemon products, compare prices and availability, review outfit suggestions, and find stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Crawlora API receives the API key and Lululemon lookup parameters.

Mitigation: Keep the key in CRAWLORA_API_KEY rather than hardcoding it, and exclude unrelated private data from queries.

## Reference(s):

- [Lululemon endpoint reference](artifact/reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/lululemon-research)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text summaries or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Category, product, outfit, review, and store details depend on available catalog data.]

## Skill Version(s):

1.0.16 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
