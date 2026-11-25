## Description:

Search, read, create, and update HubSpot CRM records and activities via HubSpot's hosted MCP server. Use when the user asks for HubSpot CRM, pipeline, owner, campaign, or customer context and changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to search HubSpot CRM records, retrieve customer and pipeline context, and make specifically authorized changes to records and activities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth credentials are stored in mcporter’s local vault, and setup can overwrite a newer refresh token if given stale credentials.

Mitigation: Install only in a trusted environment and rerun setup only with freshly issued OAuth credentials.

Risk: Authorized CRM writes can change live records or activities.

Mitigation: Confirm the requested changes, inspect current record state and relevant schemas before writing, and follow HubSpot’s confirmation requirements.

## Reference(s):

- [HubSpot hosted MCP server overview](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/integrate-with-the-remote-hubspot-mcp-server)
- [HubSpot MCP auth app setup](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/integrate-with-the-remote-hubspot-mcp-server#create-an-mcp-auth-app)
- [HubSpot OAuth token revocation](https://developers.hubspot.com/docs/api-reference/latest/authentication/oauth-tokens/revoke-token)
- [mcporter configuration reference](https://github.com/openclaw/mcporter/blob/v0.16.0/docs/config.md)
- [HubSpot skill on ClawHub](https://clawhub.ai/maverick/skills/maverick-hubspot-mcp)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Structured MCP tool calls and returned text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available tools, schemas, and permissions depend on the connected HubSpot account.]

## Skill Version(s):

1.0.13 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
