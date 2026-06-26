## Description: <br>
Lingxing Erp helps agents call Lingxing ERP OpenAPI endpoints for e-commerce advertising, orders, listings, inventory, finance, FBA, warehouse, purchasing, customer service, and multi-platform data using Lingxing credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and e-commerce analysts use this skill to query Lingxing ERP data and run documented API calls for Amazon and multi-platform commerce workflows. It is suited for retrieving reports, orders, listings, inventory, finance, FBA, warehouse, purchasing, customer service, logistics, and advertising data from authorized Lingxing accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access broad, sensitive Lingxing ERP data, including order, finance, customer, email, and operational records. <br>
Mitigation: Use least-privilege Lingxing app credentials, restrict authorized modules to the intended workflow, and treat returned data as confidential. <br>
Risk: Some supported endpoints can perform live business actions such as refunds or price changes. <br>
Mitigation: Require explicit human approval before running write endpoints and avoid granting refund or price-change permissions unless they are needed. <br>
Risk: The Lingxing access token is cached under /tmp, which may be inappropriate on shared machines. <br>
Mitigation: Run the skill only on trusted machines, avoid shared environments for sensitive credentials, and clear the token cache when access should end. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-lingxing-erp) <br>
- [Lingxing OpenAPI calling guide](references/api.md) <br>
- [Advertising report API reference](references/newad-report.md) <br>
- [Sales API reference](references/sale-full.md) <br>
- [Finance API reference](references/finance.md) <br>
- [Warehouse API reference](references/warehouse.md) <br>
- [Lingxing OpenAPI host](https://openapi.lingxing.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples; API responses are emitted as JSON to stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINGXING_APP_ID and LINGXING_APP_SECRET; LINGXING_SID is optional for default store selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
