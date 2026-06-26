## Description: <br>
Web search via Tavily API for OpenClaw agents when the user asks to search the web, look up sources, or find links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lym20220107](https://clawhub.ai/user/lym20220107) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to retrieve concise web search results with titles, URLs, snippets, and optional short answers. It is useful when a built-in Brave-style web search is unavailable or when Tavily-backed search is preferred. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to AISA/Tavily, which can expose sensitive prompts or project details to an external provider. <br>
Mitigation: Use the skill only when that provider relationship is approved, and avoid sending secrets, private customer data, or confidential project details in search queries. <br>
Risk: The skill requires an API key from the environment or ~/.openclaw/.env. <br>
Mitigation: Provide the key through approved secret-management practices and avoid committing local environment files or API keys to shared repositories. <br>
Risk: Web search results may be incomplete, outdated, or misleading. <br>
Mitigation: Review returned URLs and snippets before relying on them, and fetch or verify full source pages when accuracy matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lym20220107/lym-tavily-search) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or Markdown search results with query, title, URL, snippet or content, and optional answer fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to five results, supports basic or advanced search depth, and clamps max results to 1-10.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
