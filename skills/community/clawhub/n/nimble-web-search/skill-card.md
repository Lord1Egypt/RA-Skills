## Description:

Real-time web intelligence powered by Nimble Search API for current web search, URL discovery, AI-generated summaries, domain and time filtering, and focused research across general, coding, news, academic, shopping, social, geo, and location modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilchemla](https://clawhub.ai/user/ilchemla)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, analysts, and other external users use this skill to gather current web information, discover relevant URLs, synthesize search results, and run focused research workflows through Nimble Search API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, request parameters, request metadata, and optional deep-search page content are sent to Nimble's external API.

Mitigation: Do not submit secrets, private code, internal URLs, regulated data, or personal information unless approved for external processing.

Risk: The skill requires a Nimble API key for API access.

Mitigation: Store NIMBLE_API_KEY in a secure secret store or tightly permissioned environment configuration rather than in source files or shared logs.

Risk: Deep search can extract full page content and may increase exposure of sensitive query context.

Mitigation: Keep deep_search false for normal searches and enable it only when full page content is needed and the data is appropriate to send externally.

## Reference(s):

- [Nimble Web Search Skill Page](https://clawhub.ai/ilchemla/skills/nimble-web-search)
- [Repository Metadata](https://github.com/Nimbleway/agent-skills)
- [Nimble Search API Reference](references/api-reference.md)
- [Focus Modes - Complete Guide](references/focus-modes.md)
- [Search Strategies - Best Practices](references/search-strategies.md)
- [Nimble](https://www.nimbleway.com/)
- [Nimble Search API Endpoint](https://nimble-retriever.webit.live/search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, code examples, and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search responses may include result URLs, titles, descriptions, optional extracted page content, and optional AI-generated summaries with source citations.]

## Skill Version(s):

0.1.0 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
