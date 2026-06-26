## Description: <br>
Searches and filters Amazon products through Sorftime across multiple marketplaces to help sellers discover products, compare competitors, and explore market opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and e-commerce analysts use this skill to search products, filter by marketplace and product attributes, compare competitors, explore categories or brands, and review supported historical snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Amazon product-search queries and API credentials are sent to LinkFox/Sorftime. <br>
Mitigation: Use a dedicated LinkFox API key, avoid including sensitive business data beyond the required search parameters, and rotate or revoke the key if exposure is suspected. <br>
Risk: The skill asks agents to send free-form feedback to a separate LinkFox endpoint without clear consent. <br>
Mitigation: Require explicit approval before submitting feedback and remove personal, confidential, proprietary, or full conversation details from feedback content. <br>


## Reference(s): <br>
- [Sorftime Product Search API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-sorftime-product-search) <br>
- [LinkFox Sorftime productQuery API](https://tool-gateway.linkfox.com/sorftime/amazon/productQuery) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tables, JSON request examples, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses LinkFox API responses to present product-search results, pagination notes, ranking caveats, and error explanations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
