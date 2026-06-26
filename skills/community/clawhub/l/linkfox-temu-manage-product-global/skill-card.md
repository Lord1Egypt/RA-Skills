## Description: <br>
Supports Temu Partner Global Manage Product workflows for non-US/EU sellers through LinkFox gateway scripts covering 24 bg.local and temu.local product APIs with site=global defaults. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Temu sellers, operators, and developers use this skill to query, update, delete, and manage inventory/status details for global Temu products through LinkFox-mediated Temu APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temu seller API credentials can authorize changes or deletion of live product data. <br>
Mitigation: Use short-lived tokens where possible, keep credentials off shared machines, and install only in environments trusted to access seller operations. <br>
Risk: Mutation scripts can update inventory, product content, sale status, compliance fields, or delete goods. <br>
Mitigation: Verify every goodsId, SKU, site, and request payload before execution, especially for edit, stock, status, compliance, and delete calls. <br>
Risk: Local token storage keeps Temu access tokens in plaintext by default. <br>
Mitigation: Avoid saving tokens locally unless the machine is private and protected; prefer passing tokens only when needed. <br>
Risk: Generic proxy and file-download helpers can be used beyond narrowly scoped product-management calls. <br>
Mitigation: Restrict use to expected Temu API types and trusted file URLs, and review gateway responses before taking follow-up action. <br>


## Reference(s): <br>
- [API reference](references/api.md) <br>
- [Temu accessToken authorization](references/access-token.md) <br>
- [Partner Global catalog](references/partner-global-catalog.md) <br>
- [Manage Product API index](references/apis/README.md) <br>
- [Product query APIs](references/product-query-apis.md) <br>
- [Product edit and delete APIs](references/product-edit-delete-apis.md) <br>
- [Property and compliance APIs](references/property-compliance-apis.md) <br>
- [Stock, price, and status APIs](references/stock-price-status-apis.md) <br>
- [Temu Partner Global documentation](https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=2a343c65a03d42d380e9ad835aa7b54b) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-temu-manage-product-global) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request/response payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses LinkFox and Temu access tokens; helper scripts print JSON results from gateway calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
