## Description:

Connects an agent to a user's Kia Access or Kia Owners account to read vehicle status, location, EV charge state, and run confirm-gated door, climate, and charging commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure an MCP server that lets an agent check and control their own Kia vehicle through Kia Access or Kia Owners credentials. It is intended for account setup, vehicle reads, and explicitly confirmed vehicle commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the setup asks users to run an unpinned remote package with account credentials.

Mitigation: Use a pinned and verified package version, avoid project-level .mcp.json for real credentials, and keep credentials in the narrowest appropriate secret scope.

Risk: The security summary reports exposure of a long-lived token that can bypass MFA.

Mitigation: Do not export the refresh token unless intentionally migrating a session, never echo it in conversation or logs, and delete the stored session when it is no longer needed.

Risk: The skill can issue commands that affect a real vehicle, including unlocking doors.

Mitigation: Keep KIA_WRITE_MODE at none or comfort unless door commands are required, list vehicles before command use, and require explicit user confirmation for every command.

Risk: Vehicle reads can be stale and command acceptance does not always prove the vehicle reached the requested state.

Mitigation: Report dry runs, accepted commands, and confirmed state changes distinctly; refresh and re-read status when freshness matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chrischall/skills/kiaaccess-mcp)
- [npm Package](https://www.npmjs.com/package/kiaaccess-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and MCP tool-use instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference sensitive account, session, vehicle, and location data; write actions require explicit confirmation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
