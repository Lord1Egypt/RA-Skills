## Description:

Translates Figma designs into production-ready code with 1:1 visual fidelity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[springer63](https://clawhub.ai/user/springer63)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement UI from Figma links by fetching design context, screenshots, and assets through the Figma MCP server, then translating the result into the target project's conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a connected Figma MCP server and may query Figma project data.

Mitigation: Use it only with explicit Figma URLs the user intends to share, and confirm the Figma MCP server is connected before running design-context or screenshot tools.

Risk: Assets may be loaded from localhost URLs returned by the Figma MCP server.

Mitigation: Use only asset URLs returned by the Figma MCP server and verify that assets render correctly during UI validation.

## Reference(s):

- [Figma MCP Server Documentation](https://developers.figma.com/docs/figma-mcp-server/)
- [Figma MCP Server Tools and Prompts](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/)
- [Figma Variables and Design Tokens](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected Figma MCP server and an explicit Figma URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
