## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ifocus1776](https://clawhub.ai/user/ifocus1776)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to have an agent prepare Google Workspace workflows through the gog CLI, including Gmail, Calendar, Drive, Contacts, Sheets, and Docs tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and depends on an unpinned third-party gog executable.

Mitigation: Review the gog CLI and the steipete/tap/gogcli Homebrew tap before installation, and install only from trusted environments.

Risk: The OAuth setup can grant broad access to Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

Mitigation: Grant only the Google services needed for the task and revoke the OAuth grant when the skill is no longer used.

Risk: Mutating commands can send email, update calendars, or change Sheets and Docs data.

Mitigation: Check the target account, recipients, document IDs, and ranges before execution, and avoid unattended mutating commands.

## Reference(s):

- [GoG CLI homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/ifocus1776/skills/gogifocus)
- [Publisher profile](https://clawhub.ai/user/ifocus1776)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented command options when scripting gog CLI workflows.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
