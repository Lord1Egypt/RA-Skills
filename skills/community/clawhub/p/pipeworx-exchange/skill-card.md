## Description:

Currency exchange rates and conversion — current, historical, and all supported pairs via the Frankfurter API

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current and historical currency exchange rates, convert amounts between supported currencies, and list available currency pairs for travel planning, analysis, or commerce workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup can run a mutable npm package automatically.

Mitigation: Review the MCP setup before installing and prefer a pinned version of mcp-remote.

Risk: Exchange queries are sent to the Pipeworx gateway.

Mitigation: Avoid sending sensitive transaction context, and run the MCP client with minimal environment variables and filesystem access.

## Reference(s):

- [Pipeworx exchange homepage](https://pipeworx.io/packs/exchange)
- [Pipeworx exchange MCP endpoint](https://gateway.pipeworx.io/exchange/mcp)
- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-exchange)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Configuration, Shell commands]

**Output Format:** [JSON responses with Markdown setup guidance and shell/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exchange queries are sent to the Pipeworx gateway; setup requires curl and may use mcp-remote.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
