## Description: <br>
Use Nexus through its hosted MCP server or direct API for authenticated read-first operations and explicitly confirmed writes across CRM, orders, inventory, messaging, shipping, internal chat, social publishing, invites, and conversation intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karimsherifyehia](https://clawhub.ai/user/karimsherifyehia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and business operators use this skill to let an AI assistant inspect Nexus workspace data and perform confirmed actions for ecommerce and retail operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Nexus workspace credentials can grant broad access to business data and operations. <br>
Mitigation: Use a dedicated, expiring, least-privilege NEXUS_API_KEY and prefer read-only scope unless write access is required. <br>
Risk: Write-capable actions can change records, send messages, publish posts, invite users, initiate calls, or trigger fulfillment. <br>
Mitigation: Require manual approval of the exact record, recipient, message, post, invite, call, or fulfillment action before any write. <br>
Risk: Credentials or payloads could be exposed if sent outside Nexus endpoints. <br>
Mitigation: Limit host calls to api.nexus.aiforstartups.io and nexus-docs.aiforstartups.io. <br>


## Reference(s): <br>
- [Nexus documentation](https://nexus-docs.aiforstartups.io) <br>
- [Hosted MCP docs](https://nexus-docs.aiforstartups.io/api/ai-agents-mcp) <br>
- [OpenAPI spec](https://nexus-docs.aiforstartups.io/openapi.yaml) <br>
- [Nexus Agent API Reference](artifact/api-reference.md) <br>
- [ClawHub skill listing](https://clawhub.ai/karimsherifyehia/nexus) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEXUS_API_KEY; write operations require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
