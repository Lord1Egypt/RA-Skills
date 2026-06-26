## Description: <br>
Web search via the Tavily API for looking up sources and links when Brave web_search is unavailable or undesired, returning compact result sets with titles, URLs, snippets, and optional short answer summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gyzx](https://clawhub.ai/user/gyzx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily-backed web searches from an OpenClaw workspace and return concise source links, snippets, or optional answer summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Tavily, which can expose sensitive terms or context to a third-party service. <br>
Mitigation: Avoid using the skill for secrets, personal data, confidential project names, or private research unless external sharing with Tavily is acceptable. <br>
Risk: The skill requires a Tavily API key through TAVILY_API_KEY or ~/.openclaw/.env. <br>
Mitigation: Provide the key through local environment or config only, and avoid placing it in prompts, logs, or checked-in files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gyzx/openclaw-tavily-search-0-1-0) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Text] <br>
**Output Format:** [CLI output as raw JSON, Brave-compatible JSON, or a compact Markdown list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY; max-results is clamped to 1-10 and defaults to 5.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact _meta.json reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
