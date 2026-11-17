## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liang0591](https://clawhub.ai/user/liang0591)

### License/Terms of Use:


## Use Case:

Developers and operations users use this skill to configure and run the gog CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs tasks from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill helps an agent use an OAuth-authorized Google Workspace CLI that can access Gmail, Calendar, Drive, Contacts, Sheets, and Docs data.

Mitigation: Authorize only the Google services actually needed for the workflow and review the selected account before running commands.

Risk: Commands can send email, create calendar items, edit Sheets, or access Drive and Docs content.

Mitigation: Review actions that write, send, export, or disclose Workspace data before execution.

## Reference(s):

- [gog homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/liang0591/skills/gog-1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Google Workspace OAuth setup and command examples for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
