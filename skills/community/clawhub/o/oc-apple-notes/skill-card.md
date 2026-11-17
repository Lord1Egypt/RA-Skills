## Description:

Create, view, edit, delete, search, move, or export Apple Notes via the memo CLI on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent on macOS can manage Apple Notes from the terminal, including searching, organizing, editing, deleting, and exporting notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deleting a selected note removes user content.

Mitigation: Confirm the target note with the user before running the delete command.

Risk: Apple Notes automation requires macOS permission for Notes.app access.

Mitigation: Explain why access is needed and proceed only after the user grants the required Automation permission.

## Reference(s):

- [memo CLI project](https://github.com/antoniorodr/memo)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands manage Apple Notes; exports can be HTML or Markdown.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
