## Description: <br>
AI-powered shopping assistant. Search for products by text or image, and find the best prices across Amazon, Google Shopping, and brand stores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archroad](https://clawhub.ai/user/archroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use ShopGeni to search for products from natural-language or image inputs, compare prices across retailers, and continue shopping conversations with thread IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping queries, product image URLs, and selected local images are sent to the ShopGeni/BeyondStyle remote service. <br>
Mitigation: Use only with data you are comfortable sharing with that service, and avoid private photos, screenshots, or proprietary images. <br>
Risk: The helper stores and sends a persistent per-installation identifier that may link activity across sessions. <br>
Mitigation: Review this behavior before deployment and reset or remove ~/.config/nestor/skill_id if persistent linkage is not acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/archroad/online-price-comparison) <br>
- [ShopGeni API Service](https://nestor-api.beyondstyle.us) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from the helper script, typically presented by the agent as markdown tables or bullet lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses can include assistant text, a thread ID, product recommendations, and ranked price-comparison candidates.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
