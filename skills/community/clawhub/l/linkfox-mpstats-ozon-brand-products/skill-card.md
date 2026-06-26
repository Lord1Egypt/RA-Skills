## Description: <br>
Retrieves Ozon Russia products for an exact brand display name and returns per-SKU sales, revenue, price, rating, inventory, turnover, lost-profit, sorting, filtering, and currency-conversion data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, marketplace analysts, and e-commerce operators use this skill to inspect one Ozon brand's SKU structure, bestseller list, revenue mix, pricing, ratings, stock, turnover, and stockout-related lost profit. It is intended for brand benchmarking, competitor analysis, and product-level marketplace research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key, which is sensitive credential material. <br>
Mitigation: Store the key only in the LINKFOXAGENT_API_KEY environment variable, use a scoped or dedicated key when available, and avoid exposing it in prompts, logs, screenshots, or shared command history. <br>
Risk: Ozon brand research queries are sent to LinkFox's tool gateway. <br>
Mitigation: Use the skill only when LinkFox's data handling is acceptable for the query, and avoid submitting confidential business research unless that sharing is approved. <br>
Risk: Exact brand-name matching and T-1 date limits can produce empty or misleading snapshots when the brand spelling or date window is wrong. <br>
Mitigation: Verify the Ozon brand display name before querying, keep endDate no later than yesterday, and present results as a snapshot instead of a sales forecast. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-mpstats-ozon-brand-products) <br>
- [MPSTATS Ozon brand products API reference](references/api.md) <br>
- [LinkFox MPSTATS Ozon brand products endpoint](https://tool-gateway.linkfox.com/mpstats/ozon/brandProducts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples, tabular result guidance, and optional command-line JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and sends read-only Ozon brand research queries to the LinkFox tool gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
