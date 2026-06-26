## Description: <br>
Manage tasks in Obsidian via TaskNotes plugin API. Use when user wants to create tasks, list tasks, query by status or project, update task status, delete tasks, or check what they need to do. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benoitjadinon](https://clawhub.ai/user/benoitjadinon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage Obsidian TaskNotes through the local TaskNotes HTTP API, including listing, creating, updating, deleting, and filtering tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task update and delete commands can modify or remove Obsidian TaskNotes. <br>
Mitigation: Require explicit confirmation before delete or bulk-update operations and review the affected task paths before execution. <br>
Risk: An unauthenticated or externally reachable TaskNotes API could expose or alter vault task data. <br>
Mitigation: Enable a TaskNotes API token, keep the .env file private, and ensure the API is only reachable on localhost. <br>
Risk: The skill depends on a local Obsidian instance with the TaskNotes HTTP API enabled. <br>
Mitigation: Confirm Obsidian is running, the TaskNotes plugin is installed, and the configured API port matches TASKNOTES_API_PORT before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/benoitjadinon/obsidian-plugin-tasknotes) <br>
- [TaskNotes local API endpoint](http://localhost:8080/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI output is JSON by default or plain text tables with --table.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Obsidian vault with the TaskNotes HTTP API enabled; TASKNOTES_API_KEY is used when API authentication is configured.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
