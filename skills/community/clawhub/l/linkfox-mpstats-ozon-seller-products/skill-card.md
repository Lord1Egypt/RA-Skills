## Description: <br>
Drills into Ozon Russia products for a numeric seller ID and returns per-SKU sales, revenue, price, rating, stock, turnover, lost-profit, ranking, and related marketplace metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cross-border e-commerce analysts and marketplace operators use this skill to audit an Ozon seller's SKU portfolio, identify top sellers and stockout loss signals, and compare competitor store structures. It is data-only and is not intended to provide buying advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Ozon seller queries to LinkFox-operated endpoints and requires an API key. <br>
Mitigation: Use only in environments where LinkFox may receive those queries, keep the API key in the LINKFOXAGENT_API_KEY environment variable, and avoid prompts containing unnecessary secrets or confidential business context. <br>
Risk: The security summary flags an automatic feedback-reporting path to a separate LinkFox endpoint. <br>
Mitigation: Prefer deployments where feedback submission is disabled, reviewed, or requires explicit confirmation before sending user-interaction details. <br>
Risk: The skill reports marketplace analytics and lost-profit estimates that can be outdated or incomplete. <br>
Mitigation: Treat results as data for review rather than buying advice, respect the T-1 data limitation, and verify important business decisions against source systems. <br>


## Reference(s): <br>
- [MPSTATS Ozon Seller Products API Reference](references/api.md) <br>
- [LinkFox Tool Gateway Endpoint](https://tool-gateway.linkfox.com/mpstats/ozon/sellerProducts) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-mpstats-ozon-seller-products) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON responses and concise Markdown tables or summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and accepts seller ID, date range, pagination, sorting, currency, FBS inclusion, and numeric filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
