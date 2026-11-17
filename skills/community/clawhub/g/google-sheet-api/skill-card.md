## Description:

Installs and documents a Google Sheets CLI for service-account based read/write, batch, formatting, and sheet-management workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to configure service-account access and operate Google Sheets through repeatable CLI commands for reads, writes, formatting, batch updates, and sheet management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can modify or delete spreadsheet data through clear, deleteSheet, and batch operations.

Mitigation: Review commands before execution, especially destructive and raw batch operations, and restrict write access to intended spreadsheets.

Risk: Service-account credentials may grant access beyond the immediate task if broadly shared or automatically discovered.

Mitigation: Use a least-privilege service account, share only target spreadsheets with that account, and prefer explicit credential environment variables over automatic credential-file discovery.

Risk: The release has supply-chain risk because dependencies are not pinned by a reviewed lockfile in the provided artifact.

Mitigation: Pin dependencies or add and review a lockfile before production deployment.

## Reference(s):

- [Google Sheet API skill page](https://clawhub.ai/codedao12/skills/google-sheet-api)
- [Google Sheets API usage limits](https://developers.google.com/workspace/sheets/api/limits)
- [Google Sheets API append reference](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/append)
- [Google Sheets API ValueInputOption reference](https://developers.google.com/workspace/sheets/api/reference/rest/v4/ValueInputOption)
- [Google Sheets API batchUpdate reference](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/batchUpdate)
- [Google Sheets API batch requests guide](https://developers.google.com/workspace/sheets/api/guides/batch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI writes JSON to stdout and uses non-zero exit codes on errors.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
