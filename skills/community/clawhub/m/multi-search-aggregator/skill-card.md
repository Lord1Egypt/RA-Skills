## Description:

Aggregates searches across Tavily, Brave, and Perplexity and returns normalized results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lirun26](https://clawhub.ai/user/lirun26)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to issue one search request across multiple configured providers and receive consolidated search results for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Tavily, Brave, and/or Perplexity.

Mitigation: Use only providers approved for the data involved, and avoid sensitive internal, personal, or secret data in search queries.

Risk: Provider API keys are read from environment variables or ~/.openclaw/.env.

Mitigation: Store keys with normal secret-management controls and avoid committing local environment files or exposing captured command output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lirun26/skills/multi-search-aggregator)
- [Tavily Search API endpoint](https://api.tavily.com/search)
- [Brave Search API endpoint](https://api.search.brave.com/res/v1/web_search)
- [Perplexity API endpoint](https://api.perplexity.ai/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, code, configuration guidance]

**Output Format:** [Markdown or JSON search result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires at least one configured provider API key; default sources are Tavily and Brave.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
