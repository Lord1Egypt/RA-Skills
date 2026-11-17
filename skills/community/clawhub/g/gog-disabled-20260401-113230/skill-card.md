## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmundi3210](https://clawhub.ai/user/tmundi3210)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent provide gog CLI setup guidance and command examples for common Google Workspace tasks across Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned third-party CLI and Homebrew tap.

Mitigation: Review the gog project and Homebrew tap before installation and pin or otherwise control the installed CLI version where deployment policy requires it.

Risk: OAuth authorization can grant broad access across Google Workspace services.

Mitigation: Authorize only the Google services needed for the intended workflow and use accounts with the least necessary privileges.

Risk: Mail sending, calendar creation, and Sheets clear or update commands can change live Workspace content.

Mitigation: Test write commands on non-production data first and require human confirmation before applying changes to production mail, calendar, Sheets, Drive, Contacts, or Docs content.

## Reference(s):

- [gog CLI homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/tmundi3210/skills/gog-disabled-20260401-113230)
- [tmundi3210 publisher profile](https://clawhub.ai/user/tmundi3210)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples for Google Workspace services and safety notes for live actions.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
