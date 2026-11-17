## Description:

Connects agents to 100+ external APIs, including Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, and HubSpot, through Maton's managed OAuth gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjcloud](https://clawhub.ai/user/hjcloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route agent requests through Maton's API gateway to user-authorized third-party service connections. It is intended for workflows that need listing, creating, retrieving, updating, deleting, or messaging through connected external services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route read, write, delete, and message-sending requests across connected services.

Mitigation: Keep OAuth scopes minimal, verify the exact app and connection before each call, and require explicit user approval before POST, PUT, PATCH, DELETE, or message-sending actions.

Risk: A leaked MATON_API_KEY could allow unauthorized use of the Maton gateway for available connections.

Mitigation: Store MATON_API_KEY only in the environment or a secrets manager, avoid printing it in logs or screenshots, and rotate it if exposure is suspected.

Risk: The security review flags broad connected-service access as suspicious without enough built-in scoping or safety warnings.

Mitigation: Install only when the user trusts Maton with gateway access to connected services, and review authorized connections and scopes before use.

## Reference(s):

- [Maton](https://maton.ai)
- [Maton API Reference](https://www.maton.ai/docs/api-reference)
- [ClawHub Skill Page](https://clawhub.ai/hjcloud/skills/jef1test)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and user-authorized Maton service connections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
