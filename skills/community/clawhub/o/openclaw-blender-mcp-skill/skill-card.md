## Description:

Integrate Blender MCP (Model Context Protocol) allowing OpenClaw to control Blender for 3D modeling, scene creation, and manipulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars720816](https://clawhub.ai/user/mars720816)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and artists use this skill to let OpenClaw operate Blender through BlenderMCP for scene inspection, 3D object creation, material changes, rendering workflows, and Blender connection testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause powerful local Blender actions, including arbitrary Blender Python execution and scene modification.

Mitigation: Require explicit approval before running arbitrary Blender Python or deleting or modifying important scene content.

Risk: The workflow depends on external Blender MCP package and add-on code.

Mitigation: Install only trusted, reviewed, pinned versions of the Blender MCP package and add-on.

Risk: Agent-driven scene changes can damage or overwrite important Blender work.

Mitigation: Use project copies or backups before allowing the skill to modify Blender scenes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mars720816/skills/openclaw-blender-mcp-skill)
- [Blender MCP](https://github.com/ahujasid/blender-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands, configuration values, and BlenderMCP tool names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to start a local MCP server, test a Blender socket connection, and request Blender scene changes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
