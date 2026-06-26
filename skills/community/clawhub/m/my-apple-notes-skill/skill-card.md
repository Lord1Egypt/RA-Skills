## Description: <br>
Create, view, edit, delete, search, move, or export Apple Notes via the memo CLI on macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patrick-erichsen-2](https://clawhub.ai/user/patrick-erichsen-2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and macOS users use this skill to manage Apple Notes from an agent-assisted terminal workflow through the memo CLI. It supports creating, viewing, editing, deleting, searching, moving, and exporting notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, edit, export, move, and delete Apple Notes through the memo CLI. <br>
Mitigation: Install and use it only when agent access to Apple Notes is intended, and review note-changing or note-exporting commands before execution. <br>
Risk: macOS Automation permissions may grant access to Notes.app. <br>
Mitigation: Review macOS Automation prompts carefully and grant access only for the expected terminal or agent environment. <br>
Risk: Notes containing images or attachments cannot be edited by the underlying workflow. <br>
Mitigation: Use the skill for supported text-note workflows and handle attachment-heavy notes directly in Notes.app. <br>


## Reference(s): <br>
- [memo GitHub repository](https://github.com/antoniorodr/memo) <br>
- [ClawHub skill page](https://clawhub.ai/patrick-erichsen-2/my-apple-notes-skill) <br>
- [Homebrew formula: antoniorodr/memo/memo](https://github.com/antoniorodr/memo) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent output may direct the memo CLI to read, edit, export, move, or delete Apple Notes on macOS.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
