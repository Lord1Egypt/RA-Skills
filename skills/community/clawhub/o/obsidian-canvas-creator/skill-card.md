## Description: <br>
Create Obsidian Canvas files from text content, supporting both MindMap and freeform layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axtonliu](https://clawhub.ai/user/axtonliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and Obsidian users use this skill to convert articles, outlines, notes, and brainstorming material into Obsidian Canvas JSON with mind map or freeform layouts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate unintentionally for broad visualization or mind map requests. <br>
Mitigation: Use explicit prompts such as 'Obsidian Canvas' or '.canvas' when this output format is intended. <br>
Risk: Generated canvas text may not preserve exact quotes or source wording. <br>
Mitigation: Review generated node text against the source material before using the canvas as a factual record. <br>
Risk: Canvas layout quality can vary with input size, structure, and model behavior. <br>
Mitigation: Open the result in Obsidian and check node spacing, edge references, and readability before sharing or publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axtonliu/obsidian-canvas-creator) <br>
- [JSON Canvas Specification for Obsidian](references/canvas-spec.md) <br>
- [Canvas Layout Algorithms](references/layout-algorithms.md) <br>
- [Obsidian](https://obsidian.md/) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [JSON Canvas content with nodes and edges arrays] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed for direct import into Obsidian as a .canvas file; generated content should be reviewed for structure, spacing, and text fidelity.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
