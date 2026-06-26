## Description: <br>
Helps agents manage Amazon store listings through LinkFox-mediated SP-API calls for Listings Items, Listings Restrictions, and Product Type Definitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and developers use this skill to inspect, search, update, create, delete, and validate Amazon listing data and product type requirements through authorized store access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete live Amazon store listings. <br>
Mitigation: Require exact seller ID, SKU, marketplace, and explicit human approval before running PATCH, PUT, or DELETE operations. <br>
Risk: The skill requires sensitive Amazon seller credentials and listing data access. <br>
Mitigation: Install and run it only where LinkFox is trusted with those credentials and data. <br>


## Reference(s): <br>
- [Amazon Store Listings API Reference](references/api.md) <br>
- [getListingsItem](https://developer-docs.amazon.com/sp-api/reference/getlistingsitem) <br>
- [searchListingsItems](https://developer-docs.amazon.com/sp-api/reference/searchlistingsitems) <br>
- [patchListingsItem](https://developer-docs.amazon.com/sp-api/reference/patchlistingsitem) <br>
- [putListingsItem](https://developer-docs.amazon.com/sp-api/reference/putlistingsitem) <br>
- [deleteListingsItem](https://developer-docs.amazon.com/sp-api/reference/deletelistingsitem) <br>
- [getListingsRestrictions](https://developer-docs.amazon.com/sp-api/reference/getlistingsrestrictions) <br>
- [searchDefinitionsProductTypes](https://developer-docs.amazon.com/sp-api/reference/searchdefinitionsproducttypes) <br>
- [getDefinitionsProductType](https://developer-docs.amazon.com/sp-api/reference/getdefinitionsproducttype) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-amazon-store-listings) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request or response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LinkFox API credentials and an authorized Amazon seller account.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
