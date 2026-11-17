## Description:

Web search using Tavily's LLM-optimized API. Returns relevant results with content snippets, scores, and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthew77](https://clawhub.ai/user/matthew77)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run web searches through Tavily and retrieve LLM-oriented snippets, relevance scores, metadata, optional raw content, and filtered result sets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and selected search options are sent to Tavily.

Mitigation: Avoid confidential prompts, secrets, personal data, and proprietary internal identifiers unless Tavily's data handling terms satisfy the deployment requirements.

Risk: The skill requires a Tavily API key in configuration or the TAVILY_API_KEY environment variable.

Mitigation: Store the API key in the agent's approved secret management path and avoid printing or committing it.

## Reference(s):

- [Tavily](https://tavily.com)
- [Tavily Search API endpoint](https://api.tavily.com/search)
- [ClawHub skill page](https://clawhub.ai/matthew77/skills/liang-tavily-search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands]

**Output Format:** [Markdown search results with titles, URLs, snippets, relevance scores, optional answer text, and optional raw JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; result count is clamped to 1-20.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
