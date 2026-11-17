## Description:

Outline is presented as a document-outline skill, but the inspected artifact implements a local plaintext productivity and activity logger for notes, plans, reviews, reminders, tags, timelines, search, statistics, and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the artifact as a local command-line activity logger for capturing tasks, plans, reminders, reviews, and simple exports. Review the package before use because server security evidence says the artifact behavior does not match the advertised document-outline summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package description does not match the inspected artifact behavior.

Mitigation: Install only when a local productivity and activity logger is desired, and review the artifact before deployment.

Risk: User-entered text is stored persistently in local plaintext log files.

Mitigation: Avoid entering secrets or sensitive plans, and review filesystem permissions on ~/.local/share/outline.

Risk: CSV exports may carry user-entered content into spreadsheet applications.

Mitigation: Inspect exported CSV files before opening them in spreadsheet tools.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ckchzh/skills/outline)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration, guidance]

**Output Format:** [Plain text command output with local log and export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores user-entered text under ~/.local/share/outline and can export JSON, CSV, or text files.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
