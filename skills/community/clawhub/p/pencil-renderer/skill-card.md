## Description: <br>
Renders DNA aesthetic codes into Pencil .pen frames through a Pencil MCP backend and returns the created frame ID with a screenshot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jcwen](https://clawhub.ai/user/Jcwen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and design orchestrators use this skill to convert aesthetic DNA codes into Pencil frames for common interface components. It is intended for rendering visual proposals when a trusted Pencil MCP backend is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit Pencil documents through the configured Pencil MCP backend. <br>
Mitigation: Install and run it only with a trusted Pencil MCP backend and use it on design files an agent is allowed to modify. <br>
Risk: Batch operations can affect the wrong frame or node if identifiers are incorrect. <br>
Mitigation: Check frame and node IDs before batch operations and review the screenshot after rendering. <br>
Risk: Optional AI or stock image generation may send prompts or assets outside the local design environment. <br>
Mitigation: Avoid sending confidential prompts or assets to AI or stock image providers unless approved for the project. <br>


## Reference(s): <br>
- [DNA to Pencil Property Mapping](references/dna-to-pencil.md) <br>
- [Batch Design Patterns](references/batch-design-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Image] <br>
**Output Format:** [Markdown summary with Pencil frame ID and screenshot] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Modifies or creates Pencil .pen frames through MCP operations; screenshot capture is used for visual verification.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
