## Description:

Creates Obsidian Canvas files from text content with MindMap and freeform layouts for interactive mind maps and spatial organization.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[axtonliu](https://clawhub.ai/user/axtonliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Obsidian users use this skill to transform notes, outlines, articles, and other structured text into Obsidian Canvas JSON for mind maps or freeform visual organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad visualization requests may activate the skill when the user did not intend to create an Obsidian Canvas.

Mitigation: Ask explicitly for Obsidian Canvas or .canvas output and confirm the layout mode before generating the final JSON.

Risk: Generated Canvas JSON can be hard to use if nodes overlap, edge references are invalid, or quotes are not escaped correctly.

Mitigation: Validate the JSON structure, unique IDs, edge endpoints, quote escaping, and spacing before importing or sharing the canvas.

## Reference(s):

- [JSON Canvas Specification for Obsidian](references/canvas-spec.md)
- [Layout Algorithms for Obsidian Canvas](references/layout-algorithms.md)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [JSON Canvas (.canvas) content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directly importable into Obsidian when saved as a .canvas file; generated node IDs, edge references, quote escaping, and node spacing should be validated.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
