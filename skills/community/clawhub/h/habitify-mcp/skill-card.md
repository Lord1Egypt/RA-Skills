## Description:

Connect Habitify to OpenClaw with OAuth; read habits and update progress through Habitify's hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenyonglim](https://clawhub.ai/user/wenyonglim)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to connect a Habitify account, verify live access, read habit data, and update habit progress through Habitify's hosted MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects OpenClaw to a user's Habitify account with OAuth and managed persistent tokens.

Mitigation: Review the Habitify authorization screen, approve only expected habit read or progress update access, and keep sign-in links, callback codes, and tokens out of shared artifacts.

Risk: Progress updates can change user habit records if applied to the wrong live habit ID or scope.

Mitigation: Verify live schemas, resolve habits by live IDs, deduplicate by ID, and apply bulk updates only when every affected habit is in the user's requested scope.

Risk: Authorization or connectivity success can be mistaken for availability of every Habitify operation.

Mitigation: Use read-only verification first, report subscription, authentication, and transport errors as returned, and describe only capabilities exposed by the live server.

## Reference(s):

- [OpenClaw MCP Registry Documentation](https://docs.openclaw.ai/cli/mcp/registry)
- [Habitify MCP API Documentation](https://api-docs.habitify.me/mcp/)
- [ClawHub Skill Page](https://clawhub.ai/wenyonglim/skills/habitify-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OAuth setup guidance, live read verification steps, and scoped habit progress operation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
