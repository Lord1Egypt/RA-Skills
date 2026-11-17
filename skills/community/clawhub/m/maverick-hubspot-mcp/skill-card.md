## Description:

Search, read, and update HubSpot CRM contacts, companies, deals, tickets, associations, owners, and pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

CRM teams and other HubSpot users can find customer and pipeline information, review records, and—with clear user intent—update properties or log activities in the connected HubSpot account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected account can make changes to HubSpot business records.

Mitigation: Review the account's permissions, confirm clear user intent, and inspect the current record before editing.

Risk: Credentials persist locally, and CRM requests pass through HubSpot.

Mitigation: Keep unrelated sensitive information out of requests, revoke the integration when it is no longer needed, and rerun setup only with fresh credentials.

## Reference(s):

- [HubSpot remote MCP server documentation](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/integrate-with-the-remote-hubspot-mcp-server)
- [HubSpot MCP authentication app documentation](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/integrate-with-the-remote-hubspot-mcp-server#create-an-mcp-auth-app)

## Skill Output:

**Output Type(s):** [Text, Structured data]

**Output Format:** [Plain-text summaries, CRM records, and update confirmations; structured responses may be JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results and available operations depend on the user's request and connected HubSpot account permissions.]

## Skill Version(s):

1.0.11 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
