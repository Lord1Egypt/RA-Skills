## Description: <br>
Web search via Tavily API as an alternative to Brave web_search, returning relevant titles, URLs, snippets, and optional short answer summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[make453](https://clawhub.ai/user/make453) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add web search through Tavily when Brave web_search is unavailable or not preferred. It is suited for retrieving compact search results with URLs, snippets, and optional answer summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and related context are sent to Tavily using the user's API key. <br>
Mitigation: Use a Tavily-specific API key with sensible limits and avoid sending secrets, sensitive personal data, or sensitive business information in queries. <br>
Risk: The included artifact metadata lists a different slug and version than the server release evidence. <br>
Mitigation: Use the server-resolved ClawHub release metadata as authoritative when confirming the installed package and version. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/make453/openclaw-tavily-search-bak) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>
- [Publisher profile](https://clawhub.ai/user/make453) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON, Markdown list, or concise text snippets with source URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TAVILY_API_KEY from the environment or ~/.openclaw/.env; max-results is clamped from 1 to 10; optional answer summaries are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
