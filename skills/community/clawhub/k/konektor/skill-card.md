## Description:

Access and manage marketing leads, update lead details, and retrieve analytics for lead performance and conversion tracking via the Konektor API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramaaditya49](https://clawhub.ai/user/ramaaditya49)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to work with Konektor CRM workflows, including reading and updating leads, retrieving analytics, checking conversion sync status, reading workspace details, and creating support tickets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide creation or update of CRM leads and support tickets through remote Konektor API calls.

Mitigation: Use only Konektor workspaces you control, require explicit user approval before write actions, and grant API keys the narrowest scopes needed.

Risk: Lead, analytics, conversion, and workspace operations may involve personal or business data.

Mitigation: Avoid sending unnecessary personal or business data and verify request details before calling Konektor endpoints.

Risk: Support ticket priority and status values contain unresolved placeholders in the artifact.

Mitigation: Check Konektor's current API documentation before creating support tickets or relying on ticket status or priority values.

## Reference(s):

- [Konektor Agent API documentation](https://konektor.id/docs/api/agent-api)
- [ClawHub skill page](https://clawhub.ai/ramaaditya49/skills/konektor)
- [ClawHub publisher profile](https://clawhub.ai/user/ramaaditya49)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown API reference with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a KONEKTOR_API_KEY bearer token and endpoint-specific API scopes.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
