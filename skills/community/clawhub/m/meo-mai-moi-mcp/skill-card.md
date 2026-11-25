## Description:

Connect to Meo Mai Moi through its OAuth MCP gateway using scopes suited to the requested task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[troioi-vn](https://clawhub.ai/user/troioi-vn)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and agents use this skill to connect with Meo Mai Moi and carry out pet care, account, placement, or other supported tasks through OAuth-authorized MCP tools. It guides scope selection and safe handling of consequential actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad OAuth scopes can expose or change sensitive pet, health, finance, messaging, sharing, and account data.

Mitigation: Request only scopes needed for the task; use Full management only when explicitly selected and explain its sensitive access.

Risk: Consequential writes can affect records, access, finances, or real-world placement.

Mitigation: Read the exact target and its current version before acting, then verify the resulting state.

Risk: OAuth credentials and personal records could be exposed in chat or logs.

Mitigation: Do not request or disclose access tokens, refresh tokens, or client secrets; keep personal records out of chat unless needed for a decision.

## Reference(s):

- [Meo Mai Moi MCP clients guide](https://github.com/troioi-vn/meo-mcp/blob/main/docs/clients.md)
- [Meo Mai Moi MCP tools guide](https://github.com/troioi-vn/meo-mcp/blob/main/docs/tools.md)
- [Meo Mai Moi MCP OAuth guide](https://github.com/troioi-vn/meo-mcp/blob/main/docs/oauth.md)
- [Meo Mai Moi MCP errors guide](https://github.com/troioi-vn/meo-mcp/blob/main/docs/errors.md)
- [Meo Mai Moi MCP gateway](https://mcp.meo-mai-moi.com/mcp)
- [ClawHub skill page](https://clawhub.ai/troioi-vn/skills/meo-mai-moi-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, API calls]

**Output Format:** [Natural language guidance, OAuth and MCP configuration steps, and structured tool requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool actions depend on the user's authorization and selected scopes; sensitive operations require current-state checks and post-action verification.]

## Skill Version(s):

0.5.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
