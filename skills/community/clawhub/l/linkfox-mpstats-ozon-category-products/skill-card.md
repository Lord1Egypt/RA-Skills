## Description: <br>
This skill drills into all Ozon Russia products under a full Russian category path and returns SKU-level sales, revenue, price, rating, stock, turnover, lost-profit, ranking, and related marketplace metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketplace operators, analysts, and e-commerce agents use this skill to inspect Ozon category-level SKU performance, surface bestsellers or blue-ocean niches, and compare brands or products within a known Russian category path. It is a data retrieval and analysis aid, not a business-advice generator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the configured API key and Ozon category queries to LinkFox's tool gateway. <br>
Mitigation: Install only when LinkFox is trusted for the submitted marketplace queries, keep LINKFOXAGENT_API_KEY in environment configuration, and avoid exposing the key in prompts, logs, or shared outputs. <br>
Risk: The skill may send skill-feedback events to a separate LinkFox feedback API. <br>
Mitigation: Submit feedback only when it is relevant to skill quality and avoid including sensitive query details or credentials in feedback content. <br>
Risk: Incomplete or stale category analysis can result from partial category paths, translated paths, page limits, or same-day end dates. <br>
Mitigation: Use the full Russian Ozon category path, state the T-1 data constraint, report totals and pagination, and tighten filters rather than assuming one page represents a large category. <br>
Risk: Marketplace metrics can be mistaken for direct business advice. <br>
Mitigation: Present the retrieved data and caveats clearly, preserve source labels and currencies, and avoid making unsupported business recommendations. <br>


## Reference(s): <br>
- [MPSTATS Ozon category products API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-mpstats-ozon-category-products) <br>
- [LinkFox MPSTATS Ozon category products endpoint](https://tool-gateway.linkfox.com/mpstats/ozon/categoryProducts) <br>
- [LinkFox skills catalog](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON request and response examples, shell command examples, and compact product-metric tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and a full Russian Ozon category path; API responses are paginated with up to 100 rows per page.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
