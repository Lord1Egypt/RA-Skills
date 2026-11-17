## Description:

Connects an agent to Google Workspace tools including Gmail, Calendar, Drive, Docs, Sheets, Slides, Chat, and People through OAuth sign-in without Google Cloud Console setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dru-ca](https://clawhub.ai/user/dru-ca)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let agents search, read, create, update, and send content across Google Workspace apps after OAuth sign-in. It provides setup and command examples for mcporter and the Google Workspace MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Google Workspace account access can expose sensitive email, files, calendars, chats, and contacts.

Mitigation: Review account contents before installing and prefer a dedicated or limited Google account for agent access.

Risk: The setup auto-executes an unpinned npm package with `npx -y`.

Mitigation: Verify the npm package and publisher, and pin a reviewed package version before use.

Risk: OAuth credentials are stored locally for later reuse.

Mitigation: Revoke or delete stored OAuth credentials when the integration is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dru-ca/skills/google-workspace-mcp)
- [Publisher profile](https://clawhub.ai/user/dru-ca)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and mcporter tool examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides command-oriented guidance for configuring and calling Google Workspace tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
