## Description:

Gitbuddy is a local command-line activity logger for recording development checks, validation outcomes, lint results, diffs, fixes, reports, searches, status summaries, and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to keep a local history of code-quality checks, validation results, lint findings, diffs, fixes, reports, and related development notes. It is useful when an agent needs to suggest or run local logging, search, summary, and export workflows around development activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect Git automation features such as changelog generation, branch cleanup, or repo statistics even though the artifact behaves as a local activity logger.

Mitigation: Present and review it as a logging and export utility, and verify any Git automation claims before relying on them.

Risk: Sensitive development notes can be stored persistently in plain local files under ~/.local/share/gitbuddy.

Mitigation: Avoid logging secrets, credentials, private incident details, proprietary code notes, or other data that should not be stored or exported in plain files.

Risk: CSV and JSON exports may be unsafe to consume if values are not properly escaped.

Mitigation: Treat exported files as untrusted, validate or sanitize them before sharing or importing, and review CSV content before opening it in spreadsheet tools.

## Reference(s):

- [Gitbuddy ClawHub skill page](https://clawhub.ai/bytesagain3/skills/gitbuddy)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown with inline bash commands and terminal-output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local log files and exports under ~/.local/share/gitbuddy in JSON, CSV, or text format.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
