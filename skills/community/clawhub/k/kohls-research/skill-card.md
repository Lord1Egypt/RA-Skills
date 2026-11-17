## Description:

Researches Kohl's categories, product reviews, nearby stores, and search suggestions through the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and retail researchers use this skill to browse Kohl's products and reviews, discover category options, and find nearby stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retail searches and store-lookup locations are sent to a third-party API.

Mitigation: Use the service only when comfortable sharing those queries; prefer a city or ZIP instead of a full home or work address.

Risk: Exposing the Crawlora API key could permit unauthorized use.

Mitigation: Keep CRAWLORA_API_KEY in the environment; never include it in requests, source files, or commits.

## Reference(s):

- [Kohl's endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/kohls-research)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown with example shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Category product grids include page 1 only; reviews require a product web_id.]

## Skill Version(s):

1.0.16 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
