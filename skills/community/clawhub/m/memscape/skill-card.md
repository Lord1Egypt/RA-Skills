## Description:

Memscape gives AI agents persistent private memory, session handoffs, and shared community insights through MCP tools and REST API examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeasim](https://clawhub.ai/user/tobeasim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent users use Memscape to resume prior work, store decisions and preferences, create handoffs, and query or contribute reusable operational knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may send selected memories, handoff summaries, or project context to the external Memscape service.

Mitigation: Review every memory, handoff, contribution, promotion, and community result before acting on it or sharing it.

Risk: Secrets, personal data, customer data, proprietary source code, internal URLs, or confidential project details could be stored or contributed.

Mitigation: Do not store or contribute sensitive data; redact project-specific details before using private memory or community sharing workflows.

Risk: The Memscape API key could be exposed through repositories, logs, or weak local storage permissions.

Mitigation: Keep MEMSCAPE_API_KEY out of repositories and logs, and store credentials with restrictive file permissions or a secret store.

## Reference(s):

- [ClawHub Memscape Skill Page](https://clawhub.ai/tobeasim/skills/memscape)
- [Memscape Homepage](https://www.memscape.org)
- [Memscape REST API Reference](references/rest-api.md)
- [Memscape MCP Endpoint](https://www.memscape.org/api/mcp)
- [Memscape REST API Base URL](https://www.memscape.org/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, MCP tool names, and REST API examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MEMSCAPE_API_KEY for authenticated memory, handoff, contribution, validation, comment, and notification workflows.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
