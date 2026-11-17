## Description:

Web search via Tavily API as an alternative to Brave search, returning relevant titles, URLs, snippets, and optional short answer summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[popxool868-abcd](https://clawhub.ai/user/popxool868-abcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform Tavily-backed web searches when they need source links, snippets, compact result summaries, or a Brave-like search result shape.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and the Tavily API key are sent to Tavily as expected for the skill's purpose.

Mitigation: Do not send confidential, personal, or secret material as search queries unless sharing it with Tavily is acceptable, and store only the Tavily API key in the documented location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/popxool868-abcd/skills/openclaw-tavily-search-pb)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON or compact Markdown search results with titles, URLs, snippets, and optional short answer summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY and limits max-results to 1-10.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
