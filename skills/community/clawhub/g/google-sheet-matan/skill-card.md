## Description:

Interact with Google Sheets through Maton Gateway to read, write, append, clear, format, manage sheets, insert formulas, and configure protected ranges using curl-based API requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otman-ai](https://clawhub.ai/user/otman-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to compose Google Sheets API requests through Maton Gateway for spreadsheet data access, updates, formatting, formulas, and sheet administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, change, clear, and delete spreadsheet content through Maton Gateway.

Mitigation: Use least-privilege credentials and install only for spreadsheets where Maton Gateway is trusted and approved.

Risk: Clear, delete, batch update, and formula-writing requests can cause high-impact spreadsheet changes.

Mitigation: Require explicit review before running destructive, broad, or formula-writing commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/otman-ai/skills/google-sheet-matan)
- [Maton Google Sheets Gateway Base URL](https://gateway.maton.ai/google-sheets/v4/spreadsheets/{SPREADSHEET_ID}/{native-api-path})

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with curl command examples and request JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Maton API key and spreadsheet-specific identifiers supplied by the user.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
