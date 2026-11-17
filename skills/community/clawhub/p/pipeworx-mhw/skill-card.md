## Description:

MHW MCP - Monster Hunter World data (mhw-db.com, free, no auth).

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to Monster Hunter World data through the Pipeworx MHW MCP tools, including monsters, weapons, armor, and skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs a mutable npm package through the MCP bridge.

Mitigation: Pin mcp-remote to a reviewed exact version, use a lockfile or controlled install process, and review the package before installation.

Risk: The MCP client may receive more local access than the connector needs.

Mitigation: Run the MCP client with only the local access required for the Monster Hunter World data connector.

## Reference(s):

- [Pipeworx MHW Pack](https://pipeworx.io/packs/mhw)
- [Pipeworx](https://pipeworx.io)
- [ClawHub Skill Page](https://clawhub.ai/b-gutman/skills/pipeworx-mhw)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Markdown with JSON configuration block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key is required; setup uses an npm-based MCP bridge.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
