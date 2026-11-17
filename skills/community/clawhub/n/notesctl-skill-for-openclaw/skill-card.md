## Description:

Manage Apple Notes via deterministic local scripts to create, append, list, search, export, and edit notes when a user asks OpenClaw to manage note content or folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clinchcc](https://clawhub.ai/user/clinchcc)

### License/Terms of Use:


## Use Case:

External users and developers use Notesctl to let an OpenClaw agent create, list, search, export, and manage Apple Notes on macOS through local helper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted folder name can turn note creation into local command execution.

Mitigation: Review before installing, use only trusted note titles, bodies, and folder names, and prefer installing after folder handling is fixed by passing values to osascript as arguments or by strictly validating folder names.

Risk: The skill creates, lists, searches, and exports Apple Notes using the current macOS user's permissions.

Mitigation: Review requested note operations before execution and limit use to intended Notes folders and trusted inputs.

## Reference(s):

- [Notesctl ClawHub skill page](https://clawhub.ai/clinchcc/skills/notesctl-skill-for-openclaw)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and short text receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS with memo, python3, and osascript; export flows can prompt interactively.]

## Skill Version(s):

0.1.0 (source: server release evidence, released 2026-02-07T07:31:18Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
