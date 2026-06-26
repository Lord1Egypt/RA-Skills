## Description: <br>
Access and manage ClickUp tasks, spaces, folders, and create new tasks through a Pipeworx ClickUp MCP gateway using a user-provided ClickUp API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to let an agent list ClickUp workspace structure, inspect tasks, and create ClickUp tasks from agent workflows. It is useful when ClickUp actions should be available through an MCP server with a user-managed API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClickUp API-key-backed workspace data is routed through a third-party gateway. <br>
Mitigation: Install only if you trust the Pipeworx gateway, use the least-privileged revocable ClickUp credential available, and rotate or revoke the key if access is no longer needed. <br>
Risk: The skill can create ClickUp tasks in a real workspace. <br>
Mitigation: Review task-creation requests before approval and test in a low-impact list or workspace before using it for production task creation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-clickup) <br>
- [Publisher profile](https://clawhub.ai/user/b-gutman) <br>
- [ClickUp REST API v2](https://clickup.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, API calls, guidance] <br>
**Output Format:** [Markdown and MCP configuration JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided ClickUp API key and routes ClickUp requests through the Pipeworx gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
