## Description:

Add OAuth 2.0 PKCE authentication to a remote MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucaperret](https://clawhub.ai/user/lucaperret)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add OAuth 2.0 PKCE authentication, client registration, token exchange, refresh handling, and MCP tool access checks to remote MCP servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth examples could lead to weak login protection if used as production security code without review.

Mitigation: Treat the output as a starting reference and require security review before deployment.

Risk: Loose client or redirect URI registration can allow unsafe OAuth redirects or unintended clients.

Mitigation: Require exact client and redirect URI registration before enabling the flow.

Risk: Incorrect PKCE, token storage, revocation, or authorization tests can leave protected MCP tools accessible without valid authentication.

Mitigation: Enforce PKCE verifier checks, use secure token storage with revocation and rotation, and add centralized tests proving protected tools cannot run without valid auth.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucaperret/skills/mcp-oauth)
- [Publisher profile](https://clawhub.ai/user/lucaperret)
- [Project homepage](https://github.com/lucaperret/agent-skills)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint examples, Redis token storage guidance, redirect URI allowlist guidance, and MCP handler wrapping guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
