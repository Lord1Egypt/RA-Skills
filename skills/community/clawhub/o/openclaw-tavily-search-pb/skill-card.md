## Description: <br>
Web search via Tavily API for finding sources, links, snippets, and optional short answer summaries when Brave web_search is unavailable or undesired. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[popxool868-abcd](https://clawhub.ai/user/popxool868-abcd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to run user-requested web searches through Tavily and return concise results with titles, URLs, snippets, and optional answer text. It is useful when another web search tool is unavailable or when Tavily is the preferred search provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/popxool868-abcd/openclaw-tavily-search-pb) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or compact Markdown list with query, optional answer, and search results containing titles, URLs, and snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY via environment variable or ~/.openclaw/.env. Search queries are sent to Tavily under the user's API key; avoid secrets and sensitive personal data in queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
