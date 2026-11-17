## Description:

Use the fpx CLI and a signed-in browser session to query OneHome saved searches, shared listings, and property details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and real-estate agents use this skill to search OneHome shared listings and inspect property details from shell workflows when they need CLI access instead of the OneHome MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OneHome session tokens may be written to predictable temporary files without protection or cleanup.

Mitigation: Keep tokens in memory or use a private temporary directory with restrictive permissions and cleanup; avoid printing tokens into logs.

Risk: The external CLI and browser extension behavior remains unverified.

Mitigation: Review the tools before use and approve browser access only for OneHome.

## Reference(s):

- [GraphQL and REST operation examples](references/graphql-operations.md)
- [OneHome portal](https://portal.onehome.com)
- [ContextMint Bridge source](https://github.com/nullnet-app/contextmint-bridge)
- [Fetchproxy extension information](https://github.com/chrischall/fetchproxy#extension)

## Skill Output:

**Output Type(s):** [Shell commands, GraphQL queries, JSON request bodies, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands, GraphQL queries, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls use a user-provided OneHome magic link or an active signed-in browser session, plus relevant search or listing identifiers.]

## Skill Version(s):

1.2.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
