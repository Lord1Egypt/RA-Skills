## Description:

Create, view, edit, delete, search, move, or export Apple Notes via the memo CLI on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patrick-erichsen-2](https://clawhub.ai/user/patrick-erichsen-2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS users use this skill to manage Apple Notes from an agent-guided terminal workflow, including note creation, search, editing, moving, deletion, and export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can delete notes or export note contents that may include private information.

Mitigation: Confirm the selected note before delete operations and export notes only to secure destinations.

Risk: The workflow requires trusting the memo CLI and granting Automation access to Notes.app.

Mitigation: Install the memo CLI only from a trusted source and grant macOS Automation access only after reviewing the requested permission.

Risk: Notes containing images or attachments cannot be edited through this workflow.

Mitigation: Use Notes.app directly for notes with images or attachments, or verify note contents before attempting edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patrick-erichsen-2/skills/my-apple-notes-skill)
- [memo CLI homepage](https://github.com/antoniorodr/memo)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target macOS with Notes.app and the memo CLI available.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
