## Description:

Guides an agent using an existing ListingsAPI MCP connection to inspect business locations, listings, reviews, posts, and local analytics, or help a user try the Day Pass sandbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[listingsapi](https://clawhub.ai/user/listingsapi)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners, marketers, and their agents use this skill to inspect ListingsAPI account data and local listing performance through an existing MCP connection. With explicit approval and write access, they can also prepare and perform requested updates, review replies, or posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A connected account with write access can change business-facing listings, posts, or review replies.

Mitigation: Prefer read-only access; show the exact target and proposed change, and obtain explicit approval before each write.

Risk: Exposing a ListingsAPI key or OAuth token can compromise account access.

Mitigation: Keep credentials user-managed and out of generated content, logs, and chat.

Risk: Day Pass sandbox access could be mistaken for production authorization.

Mitigation: Confirm the active Day Pass account and restrict sandbox writes to requested sample locations; do not use it for production writes.

## Reference(s):

- [ListingsAPI MCP service](https://listingsapi.com/mcp)
- [Connect an AI agent with MCP](https://listingsapi.com/guides/connect-an-ai-agent-with-mcp)
- [Day Pass guide](https://listingsapi.com/docs/day-pass.md)
- [Day Pass live availability](https://listingsapi.com/api/day-pass)
- [ClawHub skill release](https://clawhub.ai/listingsapi/skills/listingsapi)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account findings, drafts, and user-approved action results depend on the connected account and its access level.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
