## Description: <br>
Manage Apple Reminders via the `remindctl` CLI on macOS (list, add, edit, complete, delete). Supports lists, date filters, and JSON/plain output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[landercortazarromero](https://clawhub.ai/user/landercortazarromero) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and macOS users use this skill to view, create, edit, complete, and delete Apple Reminders from an agent-assisted terminal workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required Reminders permission allows the CLI to read, modify, complete, or delete reminders and lists. <br>
Mitigation: Grant Reminders access only on trusted Macs and review destructive commands, especially delete and list-delete operations, before running them. <br>
Risk: The skill depends on installing `remindctl` from the Homebrew tap `steipete/tap` or another upstream source. <br>
Mitigation: Install only if the Homebrew tap or upstream project is trusted in the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/landercortazarromero/korta-apple-reminders) <br>
- [remindctl GitHub repository](https://github.com/steipete/remindctl) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output options including JSON, plain text, and counts-only formats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only; requires the `remindctl` binary and Apple Reminders permission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
