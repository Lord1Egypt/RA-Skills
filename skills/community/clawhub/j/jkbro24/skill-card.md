## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thayyilshihab24](https://clawhub.ai/user/thayyilshihab24)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent prepare Google Workspace CLI commands for Gmail, Calendar, Drive, Contacts, Sheets, and Docs workflows, including OAuth setup and scripting-friendly read/write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party executable for a live Google Workspace CLI.

Mitigation: Verify the gogcli Homebrew tap and release provenance before installation or execution.

Risk: Workspace write actions can send email or create, update, append, clear, or copy user data.

Mitigation: Use the narrowest OAuth services needed for the task and require explicit confirmation before any write operation.

Risk: OAuth credentials and account selection determine which live Google Workspace data the CLI can access.

Mitigation: Configure only the required services for the active account and review GOG_ACCOUNT before scripted runs.

## Reference(s):

- [gog homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/thayyilshihab24/skills/jkbro24)
- [ClawHub publisher profile](https://clawhub.ai/user/thayyilshihab24)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented command options when the underlying gog CLI supports --json.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
