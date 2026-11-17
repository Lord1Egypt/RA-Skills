## Description:

WPS Office AI Control helps agents operate open WPS Office spreadsheets, documents, and presentations through Excel, Word, PPT, common, and conversion tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and agents use this skill to inspect, edit, format, analyze, and convert WPS Office Excel, Word, and PPT files through natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform destructive document changes such as deleting sheets, rows, slides, images, or replacing text globally.

Mitigation: Review tool calls before destructive actions and keep backups for important documents.

Risk: The skill operates on open WPS Office documents and may affect the wrong file if context is stale or ambiguous.

Mitigation: Verify WPS is running, gather document context before modifying, and confirm batch or high-impact operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-wps-mod)
- [ClawHub scan report README](artifact/scan-report/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance, files]

**Output Format:** [Markdown or plain text with WPS Office operation plans, generated formulas or content, and change summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify open WPS Office documents or produce converted files when the user approves the requested operation.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
