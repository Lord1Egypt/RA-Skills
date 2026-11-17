## Description:

Google Power Tools helps agents use the Google Workspace CLI to manage Gmail, Drive, Calendar, Sheets, Docs, Slides, Forms, Tasks, People, Meet, and Classroom workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyrushuang1995-cmyk](https://clawhub.ai/user/cyrushuang1995-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and workspace administrators use this skill to have an agent draft Google Workspace CLI commands and workflows for email triage, file management, calendar scheduling, spreadsheet and document editing, forms, tasks, contacts, Meet, and Classroom operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can request broad Google Workspace OAuth access across mail, files, calendars, documents, sheets, presentations, forms, tasks, meetings, classroom data, and profile information.

Mitigation: Use service-specific OAuth scopes where possible, avoid full authorization unless comprehensive Workspace management is required, and periodically review authorized scopes and tokens.

Risk: The documented workflows include live send, edit, create, share, and delete actions that can affect user or organization data.

Mitigation: Verify every recipient, file ID, calendar ID, sheet range, and destructive operation before execution; prefer dry-run or read-only checks before mutating commands.

Risk: The setup uses local credential files and a global npm-installed CLI.

Mitigation: Protect OAuth credential files, use a dedicated Google Cloud project when practical, and review the installed CLI package and credential storage before use with sensitive personal or business data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyrushuang1995-cmyk/skills/gws-google-workspace)
- [Google Workspace CLI](https://github.com/googleworkspace/cli)
- [Google Cloud Console](https://console.cloud.google.com)
- [Setup guide](references/setup.md)
- [Gmail reference](references/gmail.md)
- [Drive reference](references/drive.md)
- [Calendar reference](references/calendar.md)
- [Sheets reference](references/sheets.md)
- [Docs, Slides, and Forms reference](references/docs-slides-forms.md)
- [Tasks, People, Meet, and Classroom reference](references/tasks-people-other.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires gws, jq, base64, python3, Google Workspace OAuth credentials, and configured project and keyring environment variables.]

## Skill Version(s):

2.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
