## Description:

Provides workflows and scripts for reading, searching, creating, updating, deleting, backing up, restoring, deduplicating, and merging macOS Contacts records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leocdchina](https://clawhub.ai/user/leocdchina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators on macOS use this skill to inspect, search, and manage local Contacts records. It is most appropriate where the user can review proposed changes and confirm destructive operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and change local macOS Contacts, including update, delete, merge, and restore workflows.

Mitigation: Use a Review posture and require explicit human confirmation before any operation that changes contacts.

Risk: Destructive or bulk workflows can remove or merge contact records incorrectly.

Mitigation: Keep an independent Contacts backup and prefer read/search or single-contact create operations unless the user has reviewed the exact target identifiers.

Risk: The security guidance flags transaction, dedupe, and merge helpers as unsuitable until scoping and input-safety issues are fixed.

Mitigation: Avoid those helpers in normal use and limit execution to lower-risk read/search workflows or carefully reviewed single-contact changes.

## Reference(s):

- [Production notes](references/production-notes.md)
- [Schema notes](references/schema-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-producing helper usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that read or mutate local macOS Contacts data and should be reviewed before execution.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
