## Description: <br>
Queries and analyzes recent Google Trends rising searches for a selected time window and supported country or region. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover recent Google search trends, compare rising topics by region, and summarize breakout queries for market or content research. <br>

### Deployment Geography for Use: <br>
Global, with trend lookups limited to the 18 supported regions listed by the skill. <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs external Google Trends-style lookups through a LinkFox gateway. <br>
Mitigation: Use only the minimum needed region and time-window parameters, and avoid including personal, confidential, or business-sensitive information in requests. <br>
Risk: The helper script requires an API key through the LINKFOXAGENT_API_KEY environment variable. <br>
Mitigation: Provide the key through the runtime environment or secret manager, and do not hardcode it in prompts, scripts, or shared files. <br>
Risk: The skill includes a non-core feedback endpoint. <br>
Mitigation: Send feedback only when relevant to skill quality, and omit sensitive user or business details unless the user has clearly consented. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-google-trends-rising) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, guidance] <br>
**Output Format:** [Markdown summaries and tables, JSON API responses, and optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include query, relative search volume, percentage increase, observation timestamps, and optional chart configuration when returned by the API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
