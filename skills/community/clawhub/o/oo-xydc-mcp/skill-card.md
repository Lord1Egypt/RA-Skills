## Description:

Operate XYDC MCP through an OOMOL-connected account with the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the connected XYDC MCP service to retrieve Amazon product, keyword, advertising, and category market data, or to generate category insight resources when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run an unverified remote installer and add persistent agent skills without clearly explaining those changes.

Mitigation: Install a verified oo CLI release yourself, review setup before enabling the skill, and set OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization.

Risk: The integration uses connected-account access, and analysis calls can consume Credits; timed-out generation may have an unknown result.

Mitigation: Review the requested access and cost, confirm the marketplace and category before generation, reuse returned resource IDs, and do not automatically retry generation after a timeout.

## Reference(s):

- [XYDC MCP documentation](https://platform.xydc.com/docs/mcp-access)
- [XYDC MCP homepage](https://platform.xydc.com/mcp)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-xydc-mcp)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on XYDC data availability and connected-account access; category insight generation may consume Credits.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
