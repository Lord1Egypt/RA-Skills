## Description:

FreeCAD MCP lets agents control FreeCAD through the Model Context Protocol to create and modify 3D models, automate CAD workflows, solve constraints, and use part libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mars720816](https://clawhub.ai/user/mars720816)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CAD automation users use this skill to let MCP-enabled agents create FreeCAD documents, add or edit CAD objects, inspect model state, capture views, and automate local FreeCAD tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected local agents can exercise broad control over FreeCAD, including arbitrary Python execution in the FreeCAD environment.

Mitigation: Use only trusted prompts and MCP clients, review generated actions before execution, and treat execute_code as equivalent to running local Python.

Risk: The local RPC server could expose CAD automation capabilities if reachable by untrusted clients.

Mitigation: Keep the RPC port bound to localhost, avoid exposing it to a network, and consider using an isolated user account or virtual machine for sensitive CAD work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mars720816/skills/openclaw-freecad-mcp)
- [FreeCAD parts library](https://github.com/FreeCAD/FreeCAD-library)
- [uv tool documentation](https://docs.astral.sh/uv/guides/tools/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON configuration snippets, shell commands, MCP tool responses, and optional image content from FreeCAD views]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local FreeCAD addon and localhost RPC connection; some tool responses may include screenshots encoded as image content.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
