## Description: <br>
Manage Google Tasks from the command line: view, create, update, and delete tasks and task lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BRO3886](https://clawhub.ai/user/BRO3886) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate Google Tasks through the gtasks CLI, including listing, creating, completing, updating, deleting, and exporting tasks and task lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authenticated authority to delete or bulk-change Google Tasks data. <br>
Mitigation: Require explicit user confirmation before delete operations or bulk changes, and review the target task list and task numbers immediately before execution. <br>
Risk: OAuth client secrets and token files can expose Google Tasks access if logged, echoed, or stored with loose permissions. <br>
Mitigation: Avoid echoing secrets, store credentials in a private secrets file or manager, keep ~/.gtasks/token.json private, and remove access with gtasks logout when no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/BRO3886/gtasks-cli) <br>
- [gtasks Homepage](https://github.com/BRO3886/gtasks) <br>
- [Quick Reference Card](references/QUICK-REFERENCE.md) <br>
- [Advanced Usage and Integration](references/ADVANCED.md) <br>
- [gtasks Releases](https://github.com/BRO3886/gtasks/releases) <br>
- [dateparse examples](https://github.com/araddon/dateparse#extended-example) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON or CSV command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce gtasks commands that read or modify authenticated Google Tasks data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
