## Description: <br>
Queries the Jungle Scout Product Database through LinkFox to filter Amazon products across 10 marketplaces by category, price, sales, revenue, reviews, ratings, BSR, LQS, seller type, and related criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers and product researchers use this skill to search product opportunities and compare marketplace items using multi-condition product database filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send user-derived feedback about interactions to a separate LinkFox feedback service without explicit user consent. <br>
Mitigation: Do not include confidential business details, customer data, or sensitive product strategy in feedback, and confirm that feedback sharing is acceptable before using that behavior. <br>
Risk: Queries and API-key-backed usage are shared with LinkFox services. <br>
Mitigation: Use an appropriate API key, limit queries to information approved for external processing, and avoid entering sensitive business or customer data unless that sharing is acceptable. <br>


## Reference(s): <br>
- [Jungle Scout Product Database API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-junglescout-product-database) <br>
- [LinkFox tool gateway product database endpoint](https://tool-gateway.linkfox.com/tool-jungle-scout/product-database/query) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown tables and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY for API-backed queries; product data may not be real time.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
