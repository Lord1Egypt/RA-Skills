## Description:

Manage Apple Notes via AppleScript CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rainbat](https://clawhub.ai/user/rainbat)

### License/Terms of Use:


## Use Case:

Developers and Apple Notes users use this skill to have an agent propose notectl commands for listing, searching, showing, creating, and appending notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search and show commands may expose private Apple Notes content.

Mitigation: Review proposed read commands and queries before running them, and avoid broad searches when private notes may be in scope.

Risk: Add and append commands persist changes in Apple Notes.

Mitigation: Confirm the target note, folder, and text before executing any write command.

## Reference(s):

- [Notectl ClawHub skill page](https://clawhub.ai/rainbat/skills/notectl)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read from or write to Apple Notes and should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
