## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottol](https://clawhub.ai/user/yottol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Google Workspace users use this skill to set up and run the gog CLI for Gmail, Calendar, Drive, Contacts, Sheets, Docs, and scripting workflows that prefer JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a Google OAuth client credential file that the security evidence says is not needed for the documented setup.

Mitigation: Use a release that removes credentials.json and requires each user to supply their own Google OAuth client configuration.

Risk: Authorizing the CLI can grant broad access to Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

Mitigation: Review requested OAuth scopes and confirm before sending mail, creating calendar events, or modifying Workspace data.

## Reference(s):

- [gog homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/yottol/skills/gog-jasmine-yottol)
- [Publisher profile](https://clawhub.ai/user/yottol)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command examples include optional JSON output modes for scripting.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
