## Description: <br>
Guides agents to query and filter Shopee product data across 11 marketplaces for product sourcing and market analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, sourcing teams, and ecommerce analysts use this skill to search and filter Shopee products by marketplace, keyword, price, sales, ratings, listing date, category, and shop attributes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires network access to LinkFox and uses LINKFOXAGENT_API_KEY credentials. <br>
Mitigation: Install only when network access to LinkFox is acceptable, store the API key in the environment, and avoid exposing it in prompts, logs, or shared outputs. <br>
Risk: Shopee search queries are sent to LinkFox. <br>
Mitigation: Avoid sending private business context or sensitive query details unless the user has approved that disclosure. <br>
Risk: The artifact instructs agents to report feedback about user interactions to a separate LinkFox endpoint without clear opt-in. <br>
Mitigation: Disable or ignore automatic feedback reporting unless the user explicitly agrees and the feedback content is redacted. <br>


## Reference(s): <br>
- [YouYing Shopee Product Search API Reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-youying-shopee-product-search) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>
- [LinkFox tool gateway API](https://tool-gateway.linkfox.com/youying/shopee/getProductInfos) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and sends Shopee search queries to LinkFox.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
