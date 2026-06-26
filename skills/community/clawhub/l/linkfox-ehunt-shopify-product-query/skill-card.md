## Description: <br>
Queries EHunt Shopify product data through LinkFox to filter Shopify products by keyword or URL, price, weekly sales, publish date, Facebook ads, competition, supplier status, and shipping country. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and ecommerce product researchers use this skill to find and compare Shopify products for independent-store sourcing and dropshipping research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox/EHunt API key, so credentials could be exposed if shared in prompts, logs, or committed files. <br>
Mitigation: Set LINKFOXAGENT_API_KEY only in trusted environments and avoid storing or sharing the key. <br>
Risk: Large Shopify product responses may include business, pricing, or other sensitive data saved to disk. <br>
Mitigation: Use a temporary output directory outside git working trees and delete persisted response files when finished. <br>
Risk: Product data and route behavior depend on the live LinkFox/EHunt gateway. <br>
Mitigation: Review API errors and returned fields before relying on results for product-sourcing decisions. <br>


## Reference(s): <br>
- [EHunt Shopify Product Query API Reference](references/api.md) <br>
- [LinkFox Tool Gateway Route](https://tool-gateway.linkfox.com/ehunt/shopify/productQuery) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-ehunt-shopify-product-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with JSON API parameters and optional shell commands; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; large API responses can be persisted locally for selective reading.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
