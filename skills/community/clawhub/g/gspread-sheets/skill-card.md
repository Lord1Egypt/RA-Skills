## Description:

Batch read/write Google Sheets using the gspread Python library with service account authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nuokunkeji](https://clawhub.ai/user/nuokunkeji)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to generate Python guidance for reading, writing, updating, clearing, and managing Google Sheets through gspread with service account authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Service account credentials can expose spreadsheets if stored or shared insecurely.

Mitigation: Store the service-account key securely, use a dedicated virtual environment, pin dependencies for production, and share only the specific spreadsheets the service account needs.

Risk: Clear, overwrite, or delete operations can remove or corrupt sheet data.

Mitigation: Require explicit confirmation before destructive sheet actions and prefer scoped ranges over whole-sheet operations.

Risk: Broad Google API scopes can grant more access than a workflow requires.

Mitigation: Prefer narrower OAuth scopes where they work for the intended read, write, or worksheet management task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nuokunkeji/skills/gspread-sheets)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes examples for service account authentication, spreadsheet access, batch reads and writes, worksheet management, formatting, and API error handling.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
