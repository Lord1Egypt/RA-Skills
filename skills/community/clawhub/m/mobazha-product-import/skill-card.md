## Description: <br>
Import products from Shopify, Amazon, Etsy, or CSV into a Mobazha store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengzie](https://clawhub.ai/user/fengzie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators and developers use this skill to migrate or copy product listings from Shopify, Amazon, Etsy, WooCommerce, or CSV into a Mobazha store. It helps prepare import JSON, package product images, configure shipping profiles, and choose between bulk import and individual listing creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be used on catalogs or product content the user is not authorized to migrate. <br>
Mitigation: Use it only for the user's own Mobazha store and product catalogs they own or are authorized to move. <br>
Risk: Downloading product images from supplied URLs can fetch unexpected private-network, oversized, or excessive media. <br>
Mitigation: Review source URLs before download, avoid localhost and private-network links, set practical size and count limits, and delete temporary ZIP and media files after import. <br>
Risk: Imported product data such as prices, shipping profiles, and product descriptions can be stale or inaccurate. <br>
Mitigation: Review generated import JSON before upload, verify pricing and shipping data, and confirm that physical goods include valid shipping profiles. <br>


## Reference(s): <br>
- [Mobazha Product Import on ClawHub](https://clawhub.ai/fengzie/mobazha-product-import) <br>
- [Universal field mapping](references/mapping.md) <br>
- [Shopify data export reference](references/shopify-api.md) <br>
- [Amazon product scraping reference](references/amazon-scrape.md) <br>
- [Shopify Products API](https://shopify.dev/docs/api/admin-rest/current/resources/product) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration guidance, API calls] <br>
**Output Format:** [Markdown guidance with JSON payloads, API examples, shell commands, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Mobazha import JSON, image filename mappings, ZIP packaging guidance, and progress-oriented migration steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
