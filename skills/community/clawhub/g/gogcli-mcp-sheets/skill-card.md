## Description:

Use when the user asks to read, write, format, or manage Google Sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect an agent to Google Sheets for reading spreadsheet data, editing cells, managing tabs, formatting ranges, exporting files, and handling named ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP server with an authenticated Google account.

Mitigation: Pin or locally verify the MCP package before use and run it with a dedicated Google account or a limited-access workspace.

Risk: The skill exposes write, delete, copy, export, merge, and structural spreadsheet actions.

Mitigation: Require explicit confirmation and a backup before delete, overwrite, export, copy, merge, or structural edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/gogcli-mcp-sheets)
- [gogcli project](https://github.com/openclaw/gogcli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute Google Sheets operations through an authenticated MCP server when installed and approved.]

## Skill Version(s):

2.8.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
