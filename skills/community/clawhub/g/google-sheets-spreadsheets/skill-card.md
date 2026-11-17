## Description:

Google Sheets API integration with managed OAuth. Create spreadsheets, read and write cell values, manage sheets, append rows, create charts, and automate data operations. Use this skill when users want spreadsheet work done in Google Sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect an OpenClaw agent to Google Sheets through ClawLink, then search spreadsheets, read ranges, update cells, append rows, manage sheets, and create charts with user-confirmed writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and allowlist an unpinned third-party plugin that handles Google OAuth and spreadsheet access.

Mitigation: Install only if the ClawLink plugin source is trusted, verify the Google consent screen and requested scopes, and remove the plugin if it is no longer needed.

Risk: A connected Google account can allow spreadsheet reads plus confirmed writes or destructive changes.

Mitigation: Preview write, clear, delete, and batch operations before execution, confirm the target spreadsheet and range, and revoke the Google connection when access is no longer required.

## Reference(s):

- [Google Sheets API Overview](https://developers.google.com/sheets/api)
- [Google Sheets Values Resource](https://developers.google.com/sheets/api/reference/spreadsheets.values)
- [Google Sheets Spreadsheets Resource](https://developers.google.com/sheets/api/reference/spreadsheets)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/google-sheets-spreadsheets)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Google Sheets writes and destructive changes require explicit user confirmation before execution.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
