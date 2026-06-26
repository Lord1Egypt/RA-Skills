## Description: <br>
Manage Apple Reminders via the `remindctl` CLI on macOS (list, add, edit, complete, delete). Supports lists, date filters, and JSON/plain output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npjameszheng1125-netizen](https://clawhub.ai/user/npjameszheng1125-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for Apple Reminders operations on macOS through `remindctl`, including viewing, creating, editing, completing, and deleting reminders and lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to change, complete, or delete Apple Reminders data. <br>
Mitigation: Before edit, complete, delete, or force-delete commands, require the agent to show the matching reminder or list and obtain explicit confirmation. <br>
Risk: The skill depends on the third-party `remindctl` Homebrew package and local Reminders authorization. <br>
Mitigation: Install only if the user trusts the package source and wants an agent to access Apple Reminders on the Mac where commands run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/npjameszheng1125-netizen/npjames-apple-reminders) <br>
- [remindctl project](https://github.com/steipete/remindctl) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON or plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Apple Reminders permission, and the `remindctl` CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
