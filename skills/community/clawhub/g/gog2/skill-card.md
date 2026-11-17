## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fionn1989](https://clawhub.ai/user/fionn1989)

### License/Terms of Use:


## Use Case:

Developers, operators, and agents use this skill to work with Google Workspace through the gog CLI, including Gmail, Calendar, Drive, Contacts, Sheets, and Docs workflows after OAuth setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad Google Workspace account access through OAuth.

Mitigation: Use a dedicated or least-privilege Google account and grant only the services needed for the task.

Risk: The skill can propose write, export, send-mail, calendar, and Sheets range-clearing actions.

Mitigation: Require explicit confirmation before sending email, modifying Sheets, clearing ranges, exporting or copying Docs, or writing calendar data.

Risk: The installation flow depends on an external gog CLI package.

Mitigation: Verify the Homebrew package provenance and trust the gog CLI source before authenticating.

Risk: OAuth client secrets may expose Google Workspace access if stored insecurely.

Mitigation: Keep the OAuth client secret in a secure local path and avoid sharing it in prompts, logs, or generated files.

## Reference(s):

- [gog CLI homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/fionn1989/skills/gog2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented CLI usage guidance when scripting with gog.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
