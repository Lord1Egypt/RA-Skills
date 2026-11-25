## Description:

Pipedrive: Manage Pipedrive sales workflows: discover fields and users, search CRM records, create and update deals, persons, organizations, activities, products, leads, and notes, move records through pipelines and stages. Use when an agent needs pipedrive, capture and convert inbound leads, create and update deals contacts and organizations, move deals through pipeline stages, schedule follow up calls and log notes, convert lead, lead id, data through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External sales teams and agents use this skill to manage Pipedrive records, leads, deals, pipelines, and follow-up activities through AgentPMT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent webhooks and delete CRM records.

Mitigation: Use these actions only when needed; verify the webhook destination and event scope, and confirm the target record before deletion.

Risk: Installation guidance is unpinned, and the scan could not review some referenced material.

Mitigation: Review the installer and skill source, pin them to reviewed versions, and check referenced material before relying on the skill.

## Reference(s):

- [AgentPMT Pipedrive marketplace page](https://www.agentpmt.com/marketplace/pipedrive)
- [Pipedrive skill on ClawHub](https://clawhub.ai/agentpmt/skills/pipedrive)
- [AgentPMT account MCP and REST API setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [API calls, JSON, Guidance]

**Output Format:** [AgentPMT tool-call JSON with concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
