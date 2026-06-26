## Description: <br>
Access and manage Asana workspaces, projects, and tasks through a Pipeworx-hosted Asana MCP gateway for listing, searching, retrieving details, and creating tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, project managers, and workspace administrators use this skill to let an agent inspect Asana workspaces, projects, and tasks, search task data, retrieve task details, and create tasks after OAuth authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses OAuth through a hosted Pipeworx gateway to access Asana data. <br>
Mitigation: Install only when Pipeworx is trusted to broker the Asana connection, review the OAuth consent screen, and use the least-privileged Asana account or workspace that supports the task. <br>
Risk: The skill can create tasks in shared Asana workspaces. <br>
Mitigation: Confirm workspace, project IDs, and task names before allowing task creation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration] <br>
**Output Format:** [Text responses with JSON MCP server configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create Asana tasks and relies on OAuth through a hosted Pipeworx gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
