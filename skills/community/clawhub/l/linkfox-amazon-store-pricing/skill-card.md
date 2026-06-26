## Description: <br>
Amazon Store Pricing helps agents use LinkFox to retrieve Amazon SP-API Product Pricing data for ASIN/SKU pricing, listing and item offers, batch pricing, featured offer expected price, and competitive summary workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ecommerce operators use this skill to query Amazon store pricing, offer, and competitive summary data through LinkFox-authenticated SP-API pricing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive LinkFox credentials, seller identifiers, request bodies, and Amazon access tokens. <br>
Mitigation: Treat LINKFOXAGENT_API_KEY, seller identifiers, request bodies, and Amazon access tokens as secrets, following the release security guidance. <br>
Risk: Overriding the gateway base URL can send store pricing requests and credentials to a different endpoint. <br>
Mitigation: Only override STORE_API_BASE_URL or SPAPI_BASE_URL when the replacement endpoint is intentionally controlled and trusted. <br>


## Reference(s): <br>
- [Amazon Store Product Pricing API Reference](references/api.md) <br>
- [getPricing](https://developer-docs.amazon.com/sp-api/reference/getpricing) <br>
- [getCompetitivePricing](https://developer-docs.amazon.com/sp-api/reference/getcompetitivepricing) <br>
- [getListingOffers](https://developer-docs.amazon.com/sp-api/reference/getlistingoffers) <br>
- [getItemOffers](https://developer-docs.amazon.com/sp-api/reference/getitemoffers) <br>
- [getItemOffersBatch](https://developer-docs.amazon.com/sp-api/reference/getitemoffersbatch) <br>
- [getListingOffersBatch](https://developer-docs.amazon.com/sp-api/reference/getlistingoffersbatch) <br>
- [getFeaturedOfferExpectedPriceBatch](https://developer-docs.amazon.com/sp-api/reference/getfeaturedofferexpectedpricebatch) <br>
- [getCompetitiveSummary](https://developer-docs.amazon.com/sp-api/reference/getcompetitivesummary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses LINKFOXAGENT_API_KEY and Amazon seller request parameters; responses follow LinkFox gateway and Amazon SP-API schemas.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
