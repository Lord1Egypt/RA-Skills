## Description: <br>
Queries Sorftime Amazon product detail and historical trend data by ASIN across 14 marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and e-commerce analysts use this skill to query ASIN-level product details, pricing, sales, BSR, profit, and FBA fee trends for product checks and competitor comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ASIN queries, marketplace choices, trend ranges, and the LinkFox API key are sent to LinkFox/Sorftime. <br>
Mitigation: Use the skill only when sharing this business context and credential with LinkFox/Sorftime is acceptable, and keep LINKFOXAGENT_API_KEY scoped and protected. <br>
Risk: The skill instructs agents to send feedback text and business context to a separate LinkFox feedback endpoint. <br>
Mitigation: Disable or strictly control feedback submission unless users explicitly consent to sending that context. <br>


## Reference(s): <br>
- [Sorftime Product Detail API Reference](references/api.md) <br>
- [Sorftime Product Detail API endpoint](https://tool-gateway.linkfox.com/sorftime/amazon/productDetail) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-sorftime-product-detail) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with JSON API responses and optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; supports up to 10 comma-separated ASINs per query.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
