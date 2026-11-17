## Description:

Searches the web through the Tavily API when an agent needs sources, links, snippets, or short answer summaries as an alternative to Brave web_search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[make453](https://clawhub.ai/user/make453)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to let an agent run small, source-oriented Tavily web searches and return URLs, snippets, and optional summaries when built-in web search is unavailable or undesired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tavily receives the search queries submitted through this skill.

Mitigation: Use the skill only when that disclosure is acceptable, avoid sensitive queries, and review Tavily account and API usage policies separately.

Risk: The skill reads TAVILY_API_KEY from the environment or ~/.openclaw/.env.

Mitigation: Keep ~/.openclaw/.env limited to intended OpenClaw secrets and protect access to the Tavily API key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/make453/skills/openclaw-tavily-search-bak)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JSON or compact Markdown search results with titles, URLs, snippets, and optional answer summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are capped by the script and the skill recommends keeping max-results small, typically 3 to 5.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
