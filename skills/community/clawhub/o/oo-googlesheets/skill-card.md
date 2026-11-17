## Description:

Google Sheets (workspace.google.com). Use this skill for ANY Google Sheets request — reading, creating, updating, and deleting data. Whenever a task involves Google Sheets, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Google Sheets can use this skill to search for spreadsheets, inspect spreadsheet structure and values, and create or update sheets through their connected OOMOL account. It guides the agent to check action schemas and seek approval before spreadsheet writes or destructive changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing-software setup directs the agent to execute downloaded code without separate approval or integrity verification.

Mitigation: Review setup behavior and approve and verify CLI installation separately before use.

Risk: The connected account can make spreadsheet writes and deletions.

Mitigation: Review connected account permissions and retain the skill's approval steps for writes and destructive changes.

## Reference(s):

- [Google Sheets](https://workspace.google.com/products/sheets/)
- [Google Sheets API Reference](https://developers.google.com/workspace/sheets/api/reference/rest)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers spreadsheet reads and changes, with approval guidance for writes and destructive actions.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
