## Description: <br>
Retrieves structured Amazon product details by ASIN, including titles, images, bullet points, specifications, A+ content, pricing, ratings, reviews, variants, and related listing data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, Amazon sellers, and researchers use this skill to retrieve and compare current Amazon product-page data for ASIN lookup, listing analysis, cross-marketplace price checks, review and rating inspection, variant review, and product specification extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ASIN queries and optional delivery postal codes are sent to LinkFox. <br>
Mitigation: Use the skill only when users are comfortable sharing those query details, avoid unnecessary postal-code inputs, and prefer a dedicated LinkFox API key. <br>
Risk: The feedback workflow may send user feedback or conversation details to a separate LinkFox endpoint. <br>
Mitigation: Avoid or disable feedback reporting unless the user explicitly agrees to send feedback or conversation details. <br>
Risk: The tool is billed per ASIN and supports batches of up to 40 ASINs. <br>
Mitigation: Query only the ASINs needed for the task and avoid broad exploratory batches. <br>


## Reference(s): <br>
- [API Reference](artifact/references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-amazon-product-detail) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, Code] <br>
**Output Format:** [Markdown guidance with JSON API parameters, shell command examples, and structured product-detail JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports comma-separated batches of up to 40 ASINs and optional marketplace, language, ZIP code, device, bought-together, related-products, and review fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
