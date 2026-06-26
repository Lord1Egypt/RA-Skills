## Description: <br>
Searches and filters TikTok Shop product data from FastMoss across supported global markets using keywords, categories, shop type, sales, GMV, commission, creator-count, and sorting filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, marketers, and ecommerce analysts use this skill to find TikTok Shop products, compare sales and GMV metrics, and inspect commission, creator-promotion, price, rating, and shop attributes. Developers and agents can also call the included script or API reference to run structured FastMoss product-search queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key and sends TikTok product-search queries to the LinkFox/FastMoss gateway. <br>
Mitigation: Use a scoped credential where possible, store it in LINKFOXAGENT_API_KEY, and avoid sending confidential product, customer, or business strategy details in search queries. <br>
Risk: The artifact instructs agents to auto-detect and submit feedback to a separate LinkFox endpoint without interrupting the user. <br>
Mitigation: Disable or gate feedback submission unless the user explicitly agrees, and exclude user statements, business context, raw errors, and other sensitive content from any feedback report. <br>


## Reference(s): <br>
- [FastMoss TikTok Product Search API Reference](references/api.md) <br>
- [LinkFox FastMoss Product Search on ClawHub](https://clawhub.ai/linkfox-ai/linkfox-fastmoss-product-search) <br>
- [FastMoss Product Search API Endpoint](https://tool-gateway.linkfox.com/fastmoss/productSearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples, shell command examples, and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY for live API calls; product result pages are limited to at most 10 items.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
