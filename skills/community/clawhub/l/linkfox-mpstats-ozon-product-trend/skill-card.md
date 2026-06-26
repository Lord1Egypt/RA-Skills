## Description: <br>
Returns daily MPSTATS time-series data for one Ozon Russia SKU, including sales, price, stock, ratings, and optional search-visibility signals for trend, seasonality, and anomaly checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and e-commerce analysts use this skill to inspect one Ozon SKU's day-by-day sales, price, inventory, rating, and visibility behavior. It is intended for factual trend review, stockout detection, and anomaly checks, not automated buying advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send Ozon SKU queries and a LinkFox API key to LinkFox services. <br>
Mitigation: Install only when that data flow is acceptable, keep the API key in LINKFOXAGENT_API_KEY, and avoid exposing credentials in prompts, logs, or feedback text. <br>
Risk: The artifact instructs agents to submit feedback to a separate LinkFox endpoint without clearly requiring user consent. <br>
Mitigation: Require explicit user approval before submitting feedback and exclude credentials, private prompts, customer data, and confidential business context. <br>


## Reference(s): <br>
- [MPSTATS Ozon Product Trend API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-mpstats-ozon-product-trend) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses or table-style summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and returns a single-SKU daily time series with possible missing days; the helper script can print raw JSON or a terminal summary table.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
