## Description: <br>
Create, read, search, and manage Apple Notes on macOS through AppleScript-backed shell commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucaperret](https://clawhub.ai/user/lucaperret) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External macOS users and their agents use this skill to create notes, list folders and notes, search note titles, and read Apple Notes content when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent access Apple Notes on the user's Mac when the user asks it to read, search, or manage notes. <br>
Mitigation: Use it only for intended Notes workflows and avoid asking it to read or search notes that contain secrets. <br>
Risk: Local activity logs may include note titles, commands, or search terms that are sensitive. <br>
Mitigation: Review or delete logs/notes.log periodically when note titles or search terms are sensitive. <br>
Risk: Notes may be created or searched in an unintended account or folder when names are ambiguous. <br>
Mitigation: List folders first and specify both account and folder when location matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucaperret/macos-notes) <br>
- [Project homepage](https://github.com/lucaperret/agent-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with JSON-over-stdin shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS with Notes.app, osascript, and python3; password-protected notes are skipped.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
