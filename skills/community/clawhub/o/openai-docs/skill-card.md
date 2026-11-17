## Description:

Query the OpenAI developer documentation via the OpenAI Docs MCP server using CLI (curl/jq) for current OpenAI API, SDK, ChatGPT Apps SDK, Codex, MCP, endpoint, parameter, limit, and migration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[am-will](https://clawhub.ai/user/am-will)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill when OpenAI platform work requires current official documentation instead of memory or non-official sources. It supports searching and fetching OpenAI docs, browsing docs indexes, listing API endpoints, and retrieving OpenAPI schemas or code samples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation search terms and fetched URLs are sent to the configured MCP endpoint.

Mitigation: Avoid including secrets, private customer data, or confidential implementation details in documentation queries.

Risk: Returned guidance can become misleading if the configured MCP endpoint is changed to an untrusted or stale source.

Mitigation: Use the default OpenAI Docs MCP endpoint or verify any MCP_URL override before relying on retrieved documentation.

## Reference(s):

- [OpenAI Docs MCP Server](https://developers.openai.com/mcp)
- [Migrate to Responses API](https://platform.openai.com/docs/guides/migrate-to-responses)
- [OpenAI Developer Docs Skill on ClawHub](https://clawhub.ai/am-will/skills/openai-docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and shell command output from OpenAI documentation queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fetched documentation URLs, excerpts, OpenAPI schema details, and code samples from the configured MCP endpoint.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
