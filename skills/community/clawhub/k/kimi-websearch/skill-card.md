## Description: <br>
Provides web search assistance through Kimi/Moonshot for questions that need current or external information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henryzhuhr](https://clawhub.ai/user/henryzhuhr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to turn a user's information need into a focused web-search query, call Kimi/Moonshot search, and summarize results with source URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search questions are sent to the external Moonshot/Kimi API. <br>
Mitigation: Use a dedicated API key, monitor quota or billing, and avoid sending secrets, private documents, or sensitive personal data in search queries. <br>
Risk: Search results can be incomplete or time-sensitive. <br>
Mitigation: Include source URLs in answers and state when available results appear incomplete or may be stale. <br>


## Reference(s): <br>
- [Kimi Websearch on ClawHub](https://clawhub.ai/henryzhuhr/kimi-websearch) <br>
- [Moonshot API Keys](https://platform.moonshot.cn/console/api-keys) <br>
- [Moonshot API endpoint](https://api.moonshot.cn/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with source URLs and optional shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KIMI_API_KEY or MOONSHOT_API_KEY and the openai Python package.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
