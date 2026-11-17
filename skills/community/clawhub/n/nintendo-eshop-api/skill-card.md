## Description:

This skill retrieves Nintendo eShop prices by country, searches the catalog, and returns product, deal, release, and DLC data for Nintendo Switch and Switch 2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use it to retrieve and compare Nintendo eShop prices by country and currency, find deals and releases, and inspect product and DLC details.

### Deployment Geography for Use:

Global; supported eShop markets vary by endpoint.

## Known Risks and Mitigations:

Risk: Requests are sent to Scavio's API, and the supplied security evidence does not establish how the service retains or handles submitted data.

Mitigation: Use only queries you are comfortable sending to Scavio, and review the service's data-handling terms before connecting an API key.

## Reference(s):

- [Nintendo eShop API overview](https://scavio.dev/nintendo-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api)
- [Nintendo search documentation](https://scavio.dev/docs/nintendo-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api)
- [Nintendo product documentation](https://scavio.dev/docs/nintendo-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api)
- [Nintendo prices documentation](https://scavio.dev/docs/nintendo-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api)
- [Nintendo deals documentation](https://scavio.dev/docs/nintendo-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api)
- [Nintendo releases documentation](https://scavio.dev/docs/nintendo-releases?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api)
- [Nintendo DLC documentation](https://scavio.dev/docs/nintendo-dlc?utm_source=agent-skills&utm_medium=skill&utm_campaign=nintendo-eshop-api)

## Skill Output:

**Output Type(s):** [JSON, API data, Guidance]

**Output Format:** [Structured Nintendo eShop data returned as JSON, with usage guidance as needed.]

**Output Parameters:** [1D (requested game, country, or endpoint)]

**Other Properties Related to Output:** [Prices remain in the eShop country's currency.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
