## Description: <br>
Analyzes Amazon keyword traffic sources for competing ASINs, including organic search, Sponsored Products, brand ads, video ads, recommendation placements, Amazon's Choice, editorial recommendations, and top-rated placements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers, marketplace analysts, and agent operators use this skill to compare which ASINs capture traffic for a keyword and how that traffic is split across organic, paid, and recommendation channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses LinkFox API-key-backed account access and sends keywords, ASINs, marketplace filters, and date ranges to LinkFox services. <br>
Mitigation: Use a dedicated API key, restrict the environment variable to trusted runs, and avoid submitting confidential business details unless LinkFox is trusted for that data. <br>
Risk: The artifact instructs agents to auto-report broad feedback or user context to a separate LinkFox feedback endpoint. <br>
Mitigation: Disable or ignore automatic feedback reporting unless the user explicitly agrees to send the specific feedback payload. <br>
Risk: The API exposes both product-level and keyword-level score families, which can lead to misleading analysis if mixed. <br>
Mitigation: Label score scope clearly in outputs and prefer keyword-level fields when answering questions about the queried keyword. <br>


## Reference(s): <br>
- [SIF Keyword Traffic API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-sif-keyword-traffic) <br>
- [LinkFox Keyword Summary API](https://tool-gateway.linkfox.com/sif/keywordSummary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with tables and optional JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and supports keyword, marketplace, ASIN, date-window, pagination, filter, and sort parameters.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
