## Description:

Command-line helper for managing Google Workspace services including Gmail, Calendar, Drive, Sheets, Docs, Slides, Contacts, Tasks, People, Groups, and Keep.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luccast](https://clawhub.ai/user/luccast)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install, configure, authenticate, and run gogcli commands for Google Workspace services from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable third-party code before interacting with Google Workspace services.

Mitigation: Inspect the upstream project before installation and avoid privileged install steps such as sudo make install unless they have been reviewed.

Risk: The skill can grant persistent access to sensitive Google account data through OAuth credentials stored under ~/.config/gog/.

Mitigation: Use a dedicated or least-privilege Google account where possible, enable only required APIs, and revoke stored OAuth credentials when access is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luccast/skills/gogcli)
- [Publisher profile](https://clawhub.ai/user/luccast)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that authenticate a Google account and access Google Workspace data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
