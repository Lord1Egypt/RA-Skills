## Description: <br>
Searches and filters Amazon product-level data from SellerSprite across supported marketplaces by price, sales, BSR, ratings, gross margin, fulfillment, seller origin, badges, and related attributes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Amazon sellers and ecommerce analysts use this skill to discover product opportunities, compare product performance, and screen niches using SellerSprite product-search data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product research queries and related user intent are sent to LinkFox/SellerSprite services. <br>
Mitigation: Use the skill only with product research data appropriate for that provider and follow applicable data-handling policies. <br>
Risk: The skill's instructions may send feedback about user intent or satisfaction to a separate LinkFox feedback endpoint without a separate confirmation step. <br>
Mitigation: Gate or disable feedback reporting unless user consent and organizational policy allow that data sharing. <br>


## Reference(s): <br>
- [SellerSprite Product Search API Reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-sellersprite-product-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown tables and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include query suggestions, result summaries, pagination notes, BSR explanations, and error guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
