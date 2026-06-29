## Description: <br>
Project Task Manager helps agents generate hierarchical task trees from objectives, decompose individual tasks, track progress, and review project status through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and project-focused agents use this skill to turn goals into structured work plans, break tasks into subtasks, and persist progress across sessions. It is intended for AgentPMT-enabled workflows that can call the remote Project Task Manager product. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project objectives, task descriptions, constraints, progress, and notes are sent to AgentPMT and generated task trees persist across sessions. <br>
Mitigation: Send only project-planning information appropriate for AgentPMT, and avoid secrets, credentials, wallet material, payment headers, and highly confidential project details. <br>
Risk: Each remote action may cost credits. <br>
Mitigation: Invoke the skill deliberately for project-planning work and confirm schema, authentication, or payment issues before retrying failed calls. <br>


## Reference(s): <br>
- [Project Task Manager on ClawHub](https://clawhub.ai/agentpmt/project-task-manager) <br>
- [Project Task Manager marketplace page](https://www.agentpmt.com/marketplace/project-task-manager) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>
- [Product schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request and response examples for remote AgentPMT tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated task trees, subtasks, status summaries, and progress updates may persist across sessions in AgentPMT.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
