## Description: <br>
Macro News Signal is an intelligent market analysis skill that transforms real-time global news and key macro indicators into actionable investment insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhelincheng](https://clawhub.ai/user/zhelincheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market analysts use this skill to collect macroeconomic and financial news, compare key indicators, and produce structured market signal reports for decision support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches financial news and market data from external providers, including URLs passed to scripts/format.py. <br>
Mitigation: Install only where outbound requests to the listed financial-news and market-data providers are acceptable, and pass only trusted public provider URLs. <br>
Risk: Unrestricted URL fetching could be misused against internal, localhost, metadata-service, or private network targets. <br>
Mitigation: Do not pass internal, localhost, metadata-service, or private URLs to scripts/format.py. <br>
Risk: Fetch requests could expose confidential trading strategy, proprietary research terms, or secrets. <br>
Mitigation: Avoid putting confidential trading strategy, proprietary research terms, or secrets into fetch requests. <br>


## Reference(s): <br>
- [Macro News Signal on ClawHub](https://clawhub.ai/zhelincheng/macro-news-signal) <br>
- [News API Reference](references/news_apis.md) <br>
- [Output Format Reference](references/output_format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown report with tables, linked news items, signal labels, market data summaries, and optional JSON-formatted market data from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include a coverage window, event summary, signal level, impact strength, market moves, asset-class recommendations, and a risk note.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
