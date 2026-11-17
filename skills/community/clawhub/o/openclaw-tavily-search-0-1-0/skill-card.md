## Description:

Web search via Tavily API for looking up sources, finding links, and returning concise result sets when Brave web_search is unavailable or undesired.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyzx](https://clawhub.ai/user/gyzx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run Tavily-powered web searches from an OpenClaw workspace and return compact search results, optional answer summaries, or Markdown lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and the Tavily API key are sent to Tavily's API when the skill runs.

Mitigation: Use this skill only when Tavily-backed web search is intended, keep the Tavily key scoped to Tavily, and avoid submitting sensitive queries unless that use is approved.

Risk: The skill can read TAVILY_API_KEY from ~/.openclaw/.env.

Mitigation: Store only the Tavily API key needed by this skill in that file and avoid placing unrelated secrets there.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gyzx/skills/openclaw-tavily-search-0-1-0)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON or Markdown search results with titles, URLs, snippets, and optional short answer summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits max-results to 1-10, with 3-5 recommended by the skill documentation to reduce token and reading load.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
