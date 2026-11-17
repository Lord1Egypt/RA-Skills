## Description:

This skill uses OOMOL's draw.io MCP connector to search the shape library and create diagrams from Mermaid or draw.io XML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and diagram authors use this skill to find draw.io shapes and create diagrams that open in the draw.io editor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote CLI installer contents are unverified, and setup may install or synchronize bundled agent skills.

Mitigation: Install and verify the CLI separately, review installation and synchronization behavior, and require approval before setup changes.

Risk: Diagram content is sent through the connected OOMOL service.

Mitigation: Review the diagram content before sending it through the connected service.

## Reference(s):

- [draw.io MCP homepage](https://www.drawio.com)
- [draw.io MCP API documentation](https://github.com/jgraph/drawio-mcp)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-drawio-mcp)

## Skill Output:

**Output Type(s):** [Text, Diagram links, Code, API results]

**Output Format:** [Text and JSON responses, including editor links, shape style strings, and diagram markup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the selected draw.io MCP action.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
