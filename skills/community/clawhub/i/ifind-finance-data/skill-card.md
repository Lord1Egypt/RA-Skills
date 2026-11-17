## Description:

iFinD Finance Data queries iFinD stock, fund, macroeconomic, industry, news, and announcement data through Python or Node.js MCP clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kooui](https://clawhub.ai/user/kooui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve iFinD financial market, fund, macroeconomic, industry, news, and announcement data from natural-language-style query parameters. It is suited for agents that need to search first, then call stock, fund, EDB, or news tools and return structured results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an iFinD authentication token locally in mcp_config.json.

Mitigation: Keep mcp_config.json out of version control, restrict file access, and rotate the token if exposure is possible.

Risk: The bundled clients disable TLS certificate verification while sending the token and finance queries over the network.

Mitigation: Enable TLS verification before use on untrusted networks, or restrict use to environments where this transport risk is acceptable.

Risk: Finance queries and requested entities are sent to iFinD services.

Mitigation: Use the skill only when sharing those query details with iFinD is acceptable for the user and organization.

## Reference(s):

- [iFinD homepage](https://www.51ifind.com)
- [ClawHub skill page](https://clawhub.ai/kooui/skills/ifind-finance-data)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python or JavaScript examples and JSON-like API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an iFinD MCP auth token in mcp_config.json; query arguments vary by stock, fund, EDB, and news service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
