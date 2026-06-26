## Description: <br>
Searches Shopify products for shoes, clothes, and bags and presents matching deals as image-rich product cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carlos-zen](https://clawhub.ai/user/carlos-zen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill to search for fashion products, apply category or price filters, and present useful product cards with images, prices, brands, stores, and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping searches, budgets, and filters are sent to LumenShop. <br>
Mitigation: Avoid including sensitive personal details in shopping queries. <br>
Risk: Changing the API URL while using a real API key can expose credentials to an untrusted host. <br>
Mitigation: Use the default or another trusted API URL, and do not pass real credentials to untrusted endpoints. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/carlos-zen/lumenshop-deals) <br>
- [LumenShop API](https://lumenshop.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [JSON search results with Markdown product-card presentation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filters can include keyword, category, result limit, and USD price range.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
