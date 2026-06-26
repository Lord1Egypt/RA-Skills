## Description: <br>
Guides agents to query Jiimore product discovery data to find Amazon products by keyword using conversion, click growth, profitability, review, seller-origin, and marketplace filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and e-commerce analysts use this skill to search Jiimore product discovery data for keyword-matched products and screen them by market, conversion, click growth, reviews, margin, listing age, and seller origin. <br>

### Deployment Geography for Use: <br>
Global, with product-discovery queries limited to Amazon US, JP, and DE marketplaces. <br>

## Known Risks and Mitigations: <br>
Risk: Amazon product-discovery queries and filters are sent to LinkFox services. <br>
Mitigation: Use the skill only when external LinkFox processing is acceptable, and avoid entering sensitive business, customer, or confidential product-planning data. <br>
Risk: The skill includes feedback behavior that can send user-derived feedback to a separate LinkFox endpoint. <br>
Mitigation: Require explicit user approval before submitting feedback and include only the minimum necessary context. <br>
Risk: Broad trigger language may route general product research requests into this integration. <br>
Mitigation: Confirm the user wants Jiimore/LinkFox-backed Amazon product discovery before making API calls. <br>


## Reference(s): <br>
- [Jiimore Product Discovery API Reference](artifact/references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-jiimore-product-discovery) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown summaries and tables, JSON API request/response examples, and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; keyword is required; page size is capped at 100; supported marketplaces are US, JP, and DE.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
