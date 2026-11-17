## Description:

Pipedrive helps agents manage Pipedrive CRM workflows, including record discovery, search, lead conversion, deal and contact updates, activities, notes, files, and webhooks through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CRM operators use this skill to let an agent search and manage Pipedrive records, capture and convert leads, update deals and contacts, schedule follow-up activities, attach files, and configure webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad CRM write and delete authority can create, update, convert, or remove business records.

Mitigation: Use least-privilege Pipedrive scopes and require explicit user confirmation before delete operations, lead conversion, stage movement, or other material CRM changes.

Risk: File transfer actions can move Pipedrive-hosted files or File Manager files between systems.

Mitigation: Confirm the file id, record association, destination, and retention settings before upload or download actions, and avoid transferring sensitive files unless the user has approved it.

Risk: Webhook creation can send CRM change events to external URLs and wildcard subscriptions can over-collect events.

Mitigation: Use verified HTTPS destinations, avoid wildcard event_action or event_object values when possible, and prefer narrow webhook subscriptions tied to the minimum required event.

Risk: Unpinned setup commands can install changing dependencies over time.

Mitigation: Prefer pinned setup dependencies over unpinned npx commands when installing related setup skills.

Risk: Pass-through data and options fields can carry unintended CRM body or query values.

Mitigation: Review JSON payloads before write operations, keep inputs scoped to the requested task, and verify the resulting Pipedrive record after each write.

## Reference(s):

- [AgentPMT Pipedrive marketplace](https://www.agentpmt.com/marketplace/pipedrive)
- [ClawHub Pipedrive skill page](https://clawhub.ai/agentpmt/skills/pipedrive)
- [Generated Pipedrive action schema](artifact/schema.md)
- [Related File Management skill](https://clawhub.ai/agentpmt/file-management)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API Calls, Shell commands]

**Output Format:** [Markdown with JSON examples and bash setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Pipedrive action names, JSON argument schemas, permission notes, pagination guidance, response handling guidance, and AgentPMT setup routes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
