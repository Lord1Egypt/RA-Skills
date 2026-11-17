## Description:

Web search using Tavily's LLM-optimized API. Returns relevant results with content snippets, scores, and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[15914355527](https://clawhub.ai/user/15914355527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tavily web searches and return source results, snippets, relevance scores, optional answers, and metadata. It supports configurable result count, search depth, topic, time range, domain filters, raw content, and JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and selected filters are sent to Tavily.

Mitigation: Install and use the skill only when sending those queries and filters to Tavily is acceptable.

Risk: The skill requires a Tavily API key.

Mitigation: Keep the key scoped and rotated according to Tavily account practices.

## Reference(s):

- [Tavily homepage](https://tavily.com)
- [Tavily Search API endpoint](https://api.tavily.com/search)
- [ClawHub skill page](https://clawhub.ai/15914355527/skills/liang-tavily-search-v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown search results by default, or formatted JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output may include source URLs, snippets, relevance scores, optional Tavily answers, and response time.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
