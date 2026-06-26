## Description: <br>
Manage Apple Notes from the terminal using the inotes CLI. Use when asked to list, read, create, edit, delete, or search notes in Notes.app on macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangwalk](https://clawhub.ai/user/wangwalk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external users, and developers use this skill to have an agent operate Apple Notes through the local inotes CLI on macOS, including listing, reading, creating, editing, deleting, searching, and exporting notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, export, edit, and delete sensitive Apple Notes after Automation permission is granted. <br>
Mitigation: Ask the agent to show the exact notes, folder or account scope, and intended operation before allowing edits, deletes, exports, or bulk archive actions. <br>
Risk: Forced or non-interactive operations can bypass confirmations for destructive changes. <br>
Mitigation: Avoid --force and --no-input unless the specific action and target scope have been clearly authorized. <br>
Risk: Installing an untrusted inotes binary could expose local note contents or modify notes unexpectedly. <br>
Mitigation: Install only from the official inotes source and verify checksums when using manual downloads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangwalk/managing-apple-notes) <br>
- [inotes GitHub repository](https://github.com/wangwalk/inotes) <br>
- [inotes releases](https://github.com/wangwalk/inotes/releases) <br>
- [inotes issues](https://github.com/wangwalk/inotes/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Notes.app, the inotes binary, and user-granted Notes Automation permission.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
