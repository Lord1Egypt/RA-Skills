## Description:

Web search using Tavily's LLM-optimized API. Returns relevant results with content snippets, scores, and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohmaxy](https://clawhub.ai/user/ohmaxy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve current web or news search results through Tavily, including source URLs, content snippets, relevance scores, and optional raw JSON metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, domain filters, and raw-content options are sent to Tavily through a third-party API.

Mitigation: Use the skill only for data categories approved for Tavily, and avoid secrets, private customer data, or confidential internal research terms unless Tavily is approved for that use.

Risk: The skill requires a Tavily API key and fails if TAVILY_API_KEY is unavailable.

Mitigation: Provide the API key through approved secret or environment-variable handling, and avoid placing credentials directly in shared logs or prompts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ohmaxy/skills/my-liang-tavily-search)
- [Tavily](https://tavily.com)
- [Tavily Search API Endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Markdown-formatted search results by default, or raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source titles, URLs, snippets, relevance scores, optional answer text, and response time when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
