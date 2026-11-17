## Description:

Use Lovable's MCP server to create, iterate on, inspect, and deploy full-stack web apps from natural-language prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[merlindegrote](https://clawhub.ai/user/merlindegrote)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate Lovable projects through MCP, including app creation, iteration, code review, deployment, database actions, analytics, connectors, and workspace governance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant broad project, workspace, deployment, database, token, and governance authority over a Lovable account.

Mitigation: Use it only when that authority is intended, avoid broad workspace/write/offline scopes unless needed, and require explicit confirmation before deployments, database changes, connector removal, project deletion, or governance updates.

Risk: Refresh tokens and access tokens are sensitive credentials.

Mitigation: Store tokens in a secure credential store or tightly permissioned file, never commit them to source control, and revoke exposed tokens through Lovable support.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/merlindegrote/skills/lovable-mcp)
- [Lovable](https://lovable.dev)
- [Lovable MCP server](https://mcp.lovable.dev)
- [Lovable OAuth authorization server metadata](https://lovable.dev/oauth/.well-known/oauth-authorization-server)
- [Lovable OAuth token endpoint](https://lovable.dev/oauth/token)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API calls]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Lovable project operations that require OAuth credentials and explicit user approval for high-impact changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
