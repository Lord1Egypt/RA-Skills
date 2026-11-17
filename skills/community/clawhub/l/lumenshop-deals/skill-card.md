## Description:

Searches Shopify products across shoes, clothes, and bags and presents matching results as image-and-text product cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carlos-zen](https://clawhub.ai/user/carlos-zen)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to search LumenShop-indexed Shopify products by keyword, category, price range, and quantity, then compare product cards with image, title, price, brand, store, and link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping searches, filters, and bearer credentials can be sent to a configurable remote endpoint.

Mitigation: Use only a trusted HTTPS API origin, avoid real API keys unless the endpoint is approved, and prefer environment-managed credentials over command-line arguments.

Risk: Returned product links and image URLs are external content.

Mitigation: Treat product links and images as untrusted, review destinations before opening, and avoid presenting results as endorsed vendors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/carlos-zen/skills/lumenshop-deals)
- [LumenShop API endpoint](https://lumenshop.vercel.app)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown]

**Output Format:** [Raw JSON from the search script, followed by Markdown product cards with image links and product metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The agent usually presents up to 12 product cards; the script supports keyword, category, price range, limit, API URL, and API key options.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
