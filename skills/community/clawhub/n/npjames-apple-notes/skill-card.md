## Description: <br>
Manage Apple Notes via the `memo` CLI on macOS to create, view, edit, delete, search, move, and export notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npjameszheng1125-netizen](https://clawhub.ai/user/npjameszheng1125-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to manage Apple Notes through the `memo` command-line tool on macOS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, change, export, move, or delete personal Apple Notes through the external `memo` CLI. <br>
Mitigation: Install only if the user trusts the `memo` CLI, and review selected notes before edit, export, move, or delete actions. <br>
Risk: Note deletion may be difficult or impossible to recover from depending on Apple Notes or iCloud settings. <br>
Mitigation: Confirm recovery options or backups before deleting notes. <br>
Risk: Interactive prompts require terminal access and may block unattended agent workflows. <br>
Mitigation: Use the skill in sessions where the user or agent can respond to terminal prompts. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/npjameszheng1125-netizen/npjames-apple-notes) <br>
- [memo CLI project](https://github.com/antoniorodr/memo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include interactive terminal prompts for selecting, editing, deleting, moving, or exporting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
