## Description:

Provides synonyms, rhymes, related words, autocomplete, and advanced word search to enhance writing and word exploration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, songwriters, poets, and developers use this skill to find synonyms, rhymes, related terms, autocomplete suggestions, and constrained word-search results through a remote words MCP endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Words or phrases submitted to the skill may be sent to the remote gateway.pipeworx.io MCP gateway.

Mitigation: Avoid submitting secrets, private drafts, personal data, confidential internal terms, or other sensitive text unless the gateway's handling of query data is trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-words)
- [Pipeworx Words MCP Endpoint](https://gateway.pipeworx.io/words/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with example JSON-RPC curl commands and MCP server configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries are sent to a remote MCP gateway for Datamuse-powered word results; no local code execution or persistence is reported in the security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
