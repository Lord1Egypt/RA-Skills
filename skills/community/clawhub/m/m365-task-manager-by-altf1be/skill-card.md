## Description: <br>
Manage lightweight Microsoft 365 task workflows by using Microsoft Graph to create, list, update, and delete Microsoft To Do tasks with structured naming, due dates, and status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abdelkrim](https://clawhub.ai/user/Abdelkrim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operations teams use this skill to capture, track, update, and close Microsoft To Do tasks from an agent workflow. It is suited to operational follow-up where tasks need clear names, due dates, and status values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, and delete real Microsoft To Do tasks through delegated Microsoft Graph access. <br>
Mitigation: Grant Tasks.ReadWrite only when that behavior is intended, and verify list names and task IDs before update or delete commands. <br>
Risk: The optional local token cache may hold reusable authentication material after device-code sign-in. <br>
Mitigation: Store the cache in a user-private directory, avoid shared or CI workstations, and set M365_TOKEN_CACHE_PATH when a controlled location is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Abdelkrim/m365-task-manager-by-altf1be) <br>
- [Publisher profile](https://clawhub.ai/user/Abdelkrim) <br>
- [M365 Task Manager Playbook](references/playbook.md) <br>
- [Skill homepage](https://github.com/ALT-F1-OpenClaw/openclaw-skill-m365-task-manager) <br>
- [Microsoft Graph API endpoint](https://graph.microsoft.com/v1.0) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI commands return JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires M365_TENANT_ID and M365_CLIENT_ID; M365_TOKEN_CACHE_PATH is optional.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
