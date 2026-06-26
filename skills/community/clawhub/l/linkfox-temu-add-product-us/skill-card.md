## Description: <br>
Temu Add Product US helps agents use LinkFox gateway scripts and reference docs to call Temu Partner US product APIs for V2 product publishing, attributes, variations, image upload, product listing, detail, editing, category mapping, inventory, and supply-price workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and marketplace operators use this skill to prepare and execute Temu US product-management API calls through LinkFox, including product publishing, category and attribute lookup, image upload, stock updates, and price queries. It is not intended for order, fulfillment, or logistics workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill and LinkFox gateway require access to Temu seller credentials. <br>
Mitigation: Use least-privilege, short-lived tokens where possible and install only when the credential exposure is acceptable. <br>
Risk: Saved Temu access tokens may be stored locally and could be revealed if unmasked. <br>
Mitigation: Avoid local token storage when possible, protect the token store path, and do not print or unmask saved tokens. <br>
Risk: The skill can perform live product, inventory, and pricing actions on a marketplace account. <br>
Mitigation: Require explicit human review before product publication, inventory changes, or price changes go live. <br>
Risk: The generic proxy can call broad Temu API types beyond narrowly reviewed workflows. <br>
Mitigation: Prefer the task-specific scripts and avoid using the generic proxy for unreviewed actions. <br>


## Reference(s): <br>
- [API Reference](artifact/references/api.md) <br>
- [Temu Access Token Authorization](artifact/references/access-token.md) <br>
- [Authorization Flow](artifact/references/authorization-flow.md) <br>
- [Partner US Catalog](artifact/references/partner-us-catalog.md) <br>
- [Product Publish APIs](artifact/references/product-publish-apis.md) <br>
- [Product Query APIs](artifact/references/product-query-apis.md) <br>
- [Product Edit APIs](artifact/references/product-edit-apis.md) <br>
- [Category and Specification APIs](artifact/references/category-spec-apis.md) <br>
- [Stock and Price APIs](artifact/references/stock-price-apis.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-temu-add-product-us) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LinkFox gateway credentials and a Temu seller access token or saved store key.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
