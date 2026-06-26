## Description: <br>
Manage Microsoft To Do tasks via the `todo` CLI for adding, listing, completing, removing, and organizing tasks, subtasks, notes, and lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[underwear](https://clawhub.ai/user/underwear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to manage Microsoft To Do tasks, lists, subtasks, notes, reminders, due dates, and recurrence patterns through the `todo` CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete tasks, subtasks, and lists, and its artifact examples include `-y` flags that bypass CLI confirmation prompts. <br>
Mitigation: Require the agent to show the exact target task, subtask, or list and receive explicit confirmation before deletion; prefer stable IDs over names or indices. <br>
Risk: The setup flow stores Microsoft OAuth client credentials and tokens in local configuration files. <br>
Mitigation: Treat `~/.config/microsoft-todo-cli/keys.yml` and OAuth token files as secrets, restrict file permissions, avoid printing them, and rotate the Azure app secret if exposed. <br>
Risk: The skill depends on the upstream `microsoft-todo-cli` package and grants access to Microsoft To Do data. <br>
Mitigation: Install only from trusted package sources and use the skill only when the user accepts the access granted to the CLI. <br>


## Reference(s): <br>
- [Microsoft API setup guide](references/setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/underwear/microsoft-todo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses `--json` for structured command output and recommends stable task IDs for multi-step operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
