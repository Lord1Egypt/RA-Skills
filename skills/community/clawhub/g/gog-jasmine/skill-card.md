## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasminehuang98613](https://clawhub.ai/user/jasminehuang98613)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to work with Gmail, Calendar, Drive, Contacts, Sheets, and Docs from an agent-assisted CLI workflow after OAuth setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Google Workspace OAuth permissions may expose mail, calendar, drive, contacts, sheets, and docs data.

Mitigation: Use a dedicated or least-privilege Google account and authorize only the Google services needed for the task.

Risk: The Homebrew install references an unpinned third-party CLI dependency.

Mitigation: Review the gog Homebrew tap before installing and pin or otherwise control the CLI version in managed environments.

Risk: OAuth client secrets and tokens can be exposed through repositories, logs, or shared shells.

Mitigation: Keep credentials and tokens out of repos, logs, and shared shell history, and store them using local secret-handling practices.

Risk: Generated CLI actions could send mail or create calendar events.

Mitigation: Require confirmation before executing commands that send messages, create events, or modify Google Workspace data.

## Reference(s):

- [gog CLI homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/jasminehuang98613/skills/gog-jasmine)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented command examples when the underlying gog command supports --json.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
