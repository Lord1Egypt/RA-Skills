## Description: <br>
Manage Plutio projects and tasks by listing projects and people, querying tasks, creating tasks, updating task details, and closing tasks through the Plutio REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GrewingM](https://clawhub.ai/user/GrewingM) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and project teams use this skill to connect an agent to a Plutio workspace, inspect projects and tasks, create tasks with required board and group IDs, and update or close existing tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Plutio API credentials and caches temporary access tokens locally. <br>
Mitigation: Use dedicated low-privilege credentials, avoid sharing secrets in chat or command history, and clear the token cache when access is no longer needed. <br>
Risk: Task-changing commands and bulk workflow examples can create, update, or close live Plutio tasks. <br>
Mitigation: Review commands and bulk filters before execution, test on a limited workspace or project first, and confirm board and group IDs before creating tasks. <br>
Risk: The Matrix notification example may disclose task details outside Plutio. <br>
Mitigation: Remove or edit the notification workflow unless the destination and content handling are approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GrewingM/plutio) <br>
- [Plutio product site](https://plutio.com/) <br>
- [Plutio API v1.11](https://api.plutio.com/v1.11) <br>
- [API endpoints reference](references/api-endpoints.md) <br>
- [Setup guide](references/setup-guide.md) <br>
- [PowerShell workflows](references/powershell-workflows.md) <br>
- [Integration examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Bash, PowerShell, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled CLI can emit JSON responses for Plutio projects, tasks, and people.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
