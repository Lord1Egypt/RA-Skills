## Description:

OpenClaw skill that installs a Google Sheets CLI with setup steps and commands for read/write, batch, formatting, and sheet management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to set up and run a Google Sheets command-line workflow for reading, writing, batch updates, formatting, layout changes, and sheet management with service account authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can modify or delete spreadsheet data through write, clear, deleteSheet, and raw batch commands.

Mitigation: Test write and batch commands on non-production spreadsheets first, and review destructive commands before execution.

Risk: Overbroad service account access could expose or alter spreadsheets beyond the intended workflow.

Mitigation: Use a tightly scoped service account, share only the specific spreadsheets needed, and prefer read-only credentials for read workflows.

Risk: Service account keys can be exposed if logged or committed.

Mitigation: Keep credentials in environment variables or local key files outside version control, and do not print key material in logs.

## Reference(s):

- [Google Sheets API Field Guide](assets/sheets-api-guide.md)
- [Google Sheets API usage limits](https://developers.google.com/workspace/sheets/api/limits)
- [spreadsheets.values.append reference](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/append)
- [ValueInputOption reference](https://developers.google.com/workspace/sheets/api/reference/rest/v4/ValueInputOption)
- [spreadsheets.batchUpdate reference](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/batchUpdate)
- [Google Sheets API batch requests guide](https://developers.google.com/workspace/sheets/api/guides/batch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples; the CLI itself returns JSON to stdout and non-zero exit codes on errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports inline JSON or @file inputs for write, append, batch, formatting, and raw batchUpdate operations.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
