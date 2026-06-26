## Description: <br>
Queries LinkFox's Google Trends gateway to analyze keyword search interest by region and date range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query and summarize Google Trends keyword interest for market research, seasonal trend checks, regional search-interest comparisons, and keyword popularity analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Keyword searches and API usage are sent to LinkFox services. <br>
Mitigation: Avoid confidential product, campaign, customer, or market-research terms unless the user accepts sending them to LinkFox. <br>
Risk: The skill instructs the agent to automatically report feedback and interaction details to a separate LinkFox endpoint. <br>
Mitigation: Disable or ignore automatic feedback reporting unless the user explicitly agrees. <br>
Risk: Use requires a LinkFox API key. <br>
Mitigation: Store the key only in LINKFOXAGENT_API_KEY and do not paste or expose it in conversation, logs, or generated output. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [LinkFox Google Trends Gateway](https://tool-gateway.linkfox.com/googleTrend/getTrendByKeys) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-google-trends-keyword) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Guidance, Shell commands] <br>
**Output Format:** [Markdown summaries with optional tables, API request JSON, and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; Google Trends values are normalized 0-100 and each API call handles one keyword.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
