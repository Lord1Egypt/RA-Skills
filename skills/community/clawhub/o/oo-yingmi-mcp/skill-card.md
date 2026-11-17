## Description:

Use an OOMOL-connected account to read and manage Yingmi MCP data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover Yingmi MCP tools and read or update financial data through an OOMOL-connected account. Check each live action schema before use, and confirm state-changing actions with the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI may synchronize additional agent skills at startup, extending capabilities beyond the Yingmi connector.

Mitigation: Review the CLI installer separately. Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if only the Yingmi connector is needed, connect only the intended account, and retain the skill's confirmation requirement for writes.

## Reference(s):

- [Yingmi MCP homepage](https://qieman.com/mcp/mcp-market)
- [Yingmi MCP API documentation](https://qieman.com/mcp/how-to-use)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Financial data, Guidance]

**Output Format:** [JSON connector responses and explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
