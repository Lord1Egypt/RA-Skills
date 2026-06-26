## Description: <br>
Searches and filters Amazon products with Keepa data across marketplace, category, price, BSR, monthly sales, reviews, ratings, package dimensions, fulfillment, and historical rank criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Amazon sellers and e-commerce researchers use this skill to turn product-research intent into structured Keepa-backed searches, compare candidate products, and filter by sales, rank, price, category, fulfillment, rating, review, size, weight, and history signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product-research queries and optional feedback are sent to LinkFox. <br>
Mitigation: Use the skill only when sharing those queries with LinkFox is acceptable, and avoid including sensitive business strategy in feedback. <br>
Risk: The skill uses LINKFOXAGENT_API_KEY for authenticated API calls. <br>
Mitigation: Provide the key through the environment, keep it out of prompts and files, and rotate it if it may have been exposed. <br>
Risk: Incorrect marketplace selection can produce irrelevant Amazon product results. <br>
Mitigation: Confirm the target marketplace before running searches outside the default US marketplace. <br>


## Reference(s): <br>
- [Keepa Product Search API Reference](references/api.md) <br>
- [ClawHub Release Page](https://clawhub.ai/linkfox-ai/linkfox-keepa-product-search) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, JSON] <br>
**Output Format:** [Markdown guidance with JSON request examples, shell command examples, and structured product-search results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses LINKFOXAGENT_API_KEY for authenticated LinkFox API calls; results may include product tables, pagination details, price conversions, BSR explanations, and error guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
