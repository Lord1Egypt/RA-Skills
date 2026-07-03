## Description: <br>
Pipedrive helps agents manage sales workflows through AgentPMT-hosted remote tool calls for CRM discovery, search, lead conversion, record updates, activities, files, notes, webhooks, pipelines, and stages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to connect Pipedrive CRM workflows to AgentPMT, capture and convert inbound leads, manage contacts and organizations, move deals through pipeline stages, schedule follow-ups, log notes, attach files, and trigger webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags broader CRM capabilities than the workflow description, including persistent webhooks, file transfer, and delete actions. <br>
Mitigation: Review the skill before installing, use least-privilege CRM credentials, and require explicit confirmation before creating webhooks, moving files, or deleting records. <br>
Risk: Persistent webhook subscriptions can continue sending CRM change events after setup. <br>
Mitigation: Check existing webhooks regularly and remove subscriptions that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Pipedrive skill page](https://clawhub.ai/agentpmt/skills/pipedrive) <br>
- [AgentPMT Pipedrive marketplace page](https://www.agentpmt.com/marketplace/pipedrive) <br>
- [AgentPMT File Management skill](https://clawhub.ai/agentpmt/file-management) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, API calls, Configuration] <br>
**Output Format:** [Markdown instructions with JSON action examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool calls return JSON-wrapped raw Pipedrive responses; file actions may use AgentPMT File Manager IDs and signed URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
