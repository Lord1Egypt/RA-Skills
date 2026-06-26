## Description: <br>
Uses EchoTik data to retrieve daily TikTok Shop new product rankings across 16 regional markets for product scouting and trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, e-commerce operators, and analysts use this skill to query daily TikTok Shop new product rankings, compare product performance by market, and present results in tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags the release as suspicious because it involves sensitive marketplace access and includes automatic feedback reporting without clear user opt-in. <br>
Mitigation: Install only if you trust LinkFox, protect the LINKFOXAGENT_API_KEY, and require confirmation before sending user feedback or business context to feedback endpoints. <br>
Risk: EchoTik ranking data is a daily snapshot and may be incomplete for long-range trend, pricing, or business decisions. <br>
Mitigation: Present the returned date, region, currency, and pagination context with results, and avoid treating one-day rankings as strategic advice. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/linkfox-ai/linkfox-echotik-new-product-rank) <br>
- [EchoTik API reference](references/api.md) <br>
- [LinkFox tool gateway API](https://tool-gateway.linkfox.com/echotik/listNewProductRank) <br>
- [LinkFox feedback API](https://skill-api.linkfox.com/api/v1/public/feedback) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables for user-facing results; JSON responses when using the helper script or API directly] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a query date; supports optional region, pageNum, and pageSize parameters. Direct script or API use requires LINKFOXAGENT_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
