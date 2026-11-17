## Description:

Web search with LLM-ranked results and freshness control. Queries api.rhdxm.com across multiple engines. No API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c5huracan](https://clawhub.ai/user/c5huracan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Meyhem Search to retrieve ranked web search results with configurable freshness and optional page-content retrieval. It is useful when an agent needs current external information without configuring an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, agent identifiers, and selected result URLs are sent to api.rhdxm.com.

Mitigation: Do not include secrets, proprietary text, private documents, or sensitive personal data in queries or agent_id values.

## Reference(s):

- [Meyhem Search ClawHub listing](https://clawhub.ai/c5huracan/skills/meyhem-search)
- [Meyhem API documentation](https://api.rhdxm.com/docs)
- [Meyhem MCP endpoint](https://api.rhdxm.com/mcp/)

## Skill Output:

**Output Type(s):** [Text, URLs]

**Output Format:** [Plain text search results with titles, URLs, relevance scores, snippets, and optional selected page content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result count, agent identifier, freshness, and optional content retrieval are controlled by command-line arguments.]

## Skill Version(s):

0.2.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
