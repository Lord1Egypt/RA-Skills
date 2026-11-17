## Description:

Manage Apple Notes from the terminal using the inotes CLI. Use when asked to list, read, create, edit, delete, or search notes in Notes.app on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangwalk](https://clawhub.ai/user/wangwalk)

### License/Terms of Use:

MIT

## Use Case:

Developers and macOS users use this skill to manage Apple Notes from an agent session through the inotes command-line tool, including listing, reading, creating, editing, deleting, and searching notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing a third-party binary that can control Apple Notes.

Mitigation: Install only from trusted sources and verify the Homebrew formula or release checksum before use.

Risk: Granting macOS Automation permission allows the CLI to read, edit, and delete notes.

Mitigation: Grant Automation access only after reviewing the tool and run `inotes status` before attempting note operations.

Risk: Delete, force, no-input, all-account, and bulk edit workflows can change or remove more notes than intended.

Mitigation: Review target notes first, prefer JSON output for programmatic selection, and avoid destructive or bulk flags unless the exact targets are confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangwalk/skills/managing-apple-notes)
- [inotes GitHub repository](https://github.com/wangwalk/inotes)
- [inotes releases](https://github.com/wangwalk/inotes/releases)
- [inotes issues](https://github.com/wangwalk/inotes/issues)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON]

**Output Format:** [Markdown guidance with shell command examples and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are intended for macOS with Notes.app, the inotes binary, and user-granted Automation permission.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
