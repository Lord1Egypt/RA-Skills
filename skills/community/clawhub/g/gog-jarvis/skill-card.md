## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bingze00000](https://clawhub.ai/user/bingze00000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide an agent through Google Workspace tasks with the gog CLI, including OAuth setup and common Gmail, Calendar, Drive, Contacts, Sheets, and Docs commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gog CLI can receive OAuth access to sensitive Google services such as Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

Mitigation: Install only if the gog CLI is trusted, grant the least-privileged Google account and service set practical, and review requested OAuth access before use.

Risk: Commands can send email, create calendar events, or change and clear Sheets data.

Mitigation: Require explicit confirmation before outbound or mutating actions, especially email sends, calendar creation, Sheets updates, appends, and clears.

## Reference(s):

- [gog CLI homepage](https://gogcli.sh)
- [ClawHub Gog Jarvis skill page](https://clawhub.ai/bingze00000/skills/gog-jarvis)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OAuth setup, Google account selection, JSON-output scripting guidance, and confirmation guidance for mutating actions.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
