## Description:

Retrieve current, source-backed official Google developer documentation for Google Cloud, Firebase, Android, Google AI, Gemini CLI, Flutter, Go, Maps, Web, TensorFlow, and related products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wei840222](https://clawhub.ai/user/wei840222)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to retrieve official Google developer documentation for setup, migrations, troubleshooting, architecture decisions, and code examples when current source-backed guidance matters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MCP routing and REST examples can send documentation queries or credentials to a configured service the user has not reviewed.

Mitigation: Install only when the configured MCP server is controlled and trusted, or set a known preferred server or config before use.

Risk: Sensitive, proprietary, incident, customer, credential, or private URL content could be exposed if included in documentation queries.

Mitigation: Use product names, public error text, and minimal non-sensitive context; do not include secrets, proprietary code, customer data, incident details, or private URLs.

Risk: Raw curl examples can encourage unsafe credential handling when used as-is.

Mitigation: Prefer safer local credential handling for REST use and only attempt REST after confirming an API key or OAuth token plus quota project is available.

## Reference(s):

- [Google Developer Knowledge API](https://developers.google.com/knowledge/api)
- [Google Developer Knowledge Quickstart](https://developers.google.com/knowledge/quickstart)
- [Google Developer Knowledge How-to](https://developers.google.com/knowledge/howto)
- [AnswerQuery](https://developers.google.com/knowledge/answer-query)
- [Google Developer Knowledge MCP](https://developers.google.com/knowledge/mcp)
- [MCP Reference](https://developers.google.com/knowledge/reference/mcp)
- [search_documents Tool Reference](https://developers.google.com/knowledge/reference/mcp/tools_list/search_documents)
- [answer_query Tool Reference](https://developers.google.com/knowledge/reference/mcp/tools_list/answer_query)
- [get_documents Tool Reference](https://developers.google.com/knowledge/reference/mcp/tools_list/get_documents)
- [Corpus Reference](https://developers.google.com/knowledge/reference/corpus-reference)
- [mcporter workflow reference](references/mcporter-workflow.md)
- [REST API fallback reference](references/api-fallback.md)
- [ClawHub skill page](https://clawhub.ai/wei840222/skills/google-developer-knowledge)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with official source URLs, document URIs, and inline shell command examples when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a concise retrieval record for current Google behavior, covering method, selected server or fallback, sources, and verification level.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
