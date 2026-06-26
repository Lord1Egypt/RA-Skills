## Description: <br>
Searches and analyzes TikTok Shop product data across 16 marketplaces, including sales, influencer promotion data, pricing, ratings, GMV, and commission rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, marketers, and e-commerce analysts use this skill to discover TikTok Shop product opportunities, compare product performance, and filter products by sales, GMV, price, rating, commission, influencer activity, and marketplace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TikTok Shop search queries, filters, and feedback may reveal sensitive commercial intent to LinkFox. <br>
Mitigation: Avoid submitting sensitive business plans, private customer data, secrets, or confidential market strategy in queries. <br>
Risk: The artifact asks agents to auto-detect and report feedback without interrupting the user's flow. <br>
Mitigation: Disable automatic feedback reporting or require explicit user consent before sending feedback about intent, results, dissatisfaction, or praise. <br>


## Reference(s): <br>
- [EchoTik-TikTok Product Search API Reference](references/api.md) <br>
- [LinkFox Tool Gateway EchoTik List Product Endpoint](https://tool-gateway.linkfox.com/echotik/listProduct) <br>
- [Echotik Product Search on ClawHub](https://clawhub.ai/linkfox-ai/linkfox-echotik-product-search) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses LINKFOXAGENT_API_KEY for authenticated requests to the LinkFox tool gateway.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
