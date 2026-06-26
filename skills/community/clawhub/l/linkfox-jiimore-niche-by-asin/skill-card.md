## Description: <br>
Finds Amazon products in the same niche as a reference ASIN and filters competitor results by conversion, clicks, sales, reviews, rating, price, FBA fees, and gross margin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and analysts use this skill to query LinkFox for ASIN-based Amazon same-niche competitor discovery across supported marketplaces. It helps compare objective product metrics such as conversion rates, clicks, sales volume, reviews, prices, and margins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ASIN research queries, filters, and API credentials are sent to LinkFox services. <br>
Mitigation: Use only with an approved LINKFOXAGENT_API_KEY, avoid sending sensitive business context beyond the required query parameters, and review outbound requests before use. <br>
Risk: The artifact instructs agents to submit broad feedback to a separate LinkFox endpoint without interrupting the user. <br>
Mitigation: Disable or ignore feedback submissions unless the user explicitly opts in, and never include private business details, secrets, or sensitive prompt content in feedback. <br>
Risk: The API supports only US, JP, and DE marketplaces and requires ASIN-based same-niche lookup. <br>
Mitigation: Confirm the marketplace and ASIN before invoking the skill; route keyword-level or unsupported-marketplace requests to a more appropriate workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/linkfox-ai/linkfox-jiimore-niche-by-asin) <br>
- [API reference](references/api.md) <br>
- [LinkFox tool gateway endpoint](https://tool-gateway.linkfox.com/jiimore/pageAsinsByAsin) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, markdown] <br>
**Output Format:** [Markdown guidance with JSON request examples and optional JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and an ASIN; API results are paginated and limited to supported marketplaces US, JP, and DE.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
