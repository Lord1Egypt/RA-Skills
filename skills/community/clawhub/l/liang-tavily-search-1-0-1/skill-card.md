## Description:

Web search using Tavily's LLM-optimized API. Returns relevant results with content snippets, scores, and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryren2024](https://clawhub.ai/user/terryren2024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to run Tavily web searches from an agent workflow, returning concise source lists, snippets, relevance scores, optional answers, and optional raw JSON for downstream reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, filters, and raw-content requests are sent to Tavily.

Mitigation: Avoid submitting secrets, private internal identifiers, or sensitive personal data unless Tavily account terms and organizational policy permit that use.

Risk: The skill requires a Tavily API key.

Mitigation: Provide TAVILY_API_KEY through the agent environment or approved configuration storage and rotate it according to local credential policy.

Risk: Using --raw-content can request and return larger page-content payloads.

Mitigation: Enable raw-content output only when the task requires full page text and review returned content before using it in sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terryren2024/skills/liang-tavily-search-1-0-1)
- [Publisher profile](https://clawhub.ai/user/terryren2024)
- [Tavily homepage](https://tavily.com)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration]

**Output Format:** [Markdown source summaries by default, or formatted JSON when the --json option is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result count is clamped to 1-20; options include search depth, topic, time range, domain filters, and raw-content inclusion.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
