## Description: <br>
Amazon Store Catalog helps agents query Amazon SP-API Catalog Items through LinkFox for category lookup, keyword or identifier search, and ASIN-based catalog item retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and marketplace operators use this skill to inspect Amazon product catalog data, including category nodes, search results, item summaries, images, and related Catalog Items fields for a seller account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Amazon SP-API access through a LinkFox API key and gateway. <br>
Mitigation: Install only when LinkFox is trusted for the seller account, keep LINKFOXAGENT_API_KEY out of logs and shared prompts, and rotate credentials if exposed. <br>
Risk: Seller IDs, ASIN/SKU inputs, and returned catalog data may be business-sensitive. <br>
Mitigation: Limit use to authorized users and avoid pasting catalog responses into untrusted workspaces or public channels. <br>
Risk: The skill depends on the companion LinkFox Amazon Store auth skill and correct Catalog Items permissions. <br>
Mitigation: Run the dependency check, verify the companion auth skill before use, and confirm Catalog Items roles before troubleshooting API failures. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-amazon-store-catalog) <br>
- [Catalog API Reference](references/api.md) <br>
- [Amazon SP-API listCatalogCategories](https://developer-docs.amazon.com/sp-api/reference/listcatalogcategories) <br>
- [Amazon SP-API searchCatalogItems](https://developer-docs.amazon.com/sp-api/reference/searchcatalogitems) <br>
- [Amazon SP-API getCatalogItem](https://developer-docs.amazon.com/sp-api/reference/getcatalogitem) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON-producing Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts return JSON responses from LinkFox developerProxy calls and require LINKFOXAGENT_API_KEY plus the companion auth skill.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
