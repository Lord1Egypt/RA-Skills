## Description:

Connects Google Drive and Sheets through a user's OAuth authorization and provides workflows for creating, reading, editing, formatting, and managing files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinhbuiii](https://clawhub.ai/user/thinhbuiii)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to their Google Drive and Sheets account, then create and manage files and spreadsheet data through the user's own OAuth authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that a formatting command may bypass deletion safeguards and make destructive spreadsheet changes beyond the requested formatting task.

Mitigation: Review the exact operation, spreadsheet, and affected range before execution; retain a recoverable copy before changes and require explicit user confirmation for destructive edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thinhbuiii/skills/gsc-clean)
- [Publisher profile](https://clawhub.ai/user/thinhbuiii)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operations use the connected user's Google Drive and Sheets permissions and require the user to authorize access.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
