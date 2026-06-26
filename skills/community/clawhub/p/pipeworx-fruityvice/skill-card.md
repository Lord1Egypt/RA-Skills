## Description: <br>
Nutritional data for fruits — calories, sugar, fat, protein, and carbs per 100g from Fruityvice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to query fruit nutrition data through Pipeworx Fruityvice tools, including single-fruit lookup, full fruit listing, and nutrient-range filtering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fruit nutrition queries are sent to the Pipeworx gateway. <br>
Mitigation: Avoid sending sensitive or private data in tool arguments and review gateway use against local data handling requirements. <br>
Risk: The setup command runs mcp-remote through npx. <br>
Mitigation: Review the package and command before installation, pin versions where appropriate, and install only in environments that permit remote MCP execution. <br>


## Reference(s): <br>
- [Pipeworx Fruityvice](https://pipeworx.io/packs/fruityvice) <br>
- [Pipeworx Fruityvice MCP endpoint](https://gateway.pipeworx.io/fruityvice/mcp) <br>
- [ClawHub listing](https://clawhub.ai/b-gutman/pipeworx-fruityvice) <br>
- [Publisher profile](https://clawhub.ai/user/b-gutman) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON responses and Markdown with shell and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for direct examples; MCP setup runs npx mcp-remote against the Pipeworx Fruityvice gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
