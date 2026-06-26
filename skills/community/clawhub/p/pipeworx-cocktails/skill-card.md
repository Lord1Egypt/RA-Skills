## Description: <br>
Cocktail recipes from TheCocktailDB — search by name, browse by ingredient, or discover a random drink. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up cocktail recipes, search by name or ingredient, retrieve full ingredient measurements and instructions, or request a random drink suggestion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recipe queries are sent through the Pipeworx gateway. <br>
Mitigation: Avoid sending sensitive or personal information in cocktail lookup prompts and review organizational data-sharing policy before use. <br>
Risk: The sample MCP client setup runs mcp-remote via npx. <br>
Mitigation: Pin or inspect the mcp-remote package before enabling the MCP configuration in environments that require tighter supply-chain control. <br>


## Reference(s): <br>
- [Pipeworx Cocktails homepage](https://pipeworx.io/packs/cocktails) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-cocktails) <br>
- [Pipeworx Cocktails MCP endpoint](https://gateway.pipeworx.io/cocktails/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown or plain text recipe results with inline shell commands and JSON MCP configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns cocktail names, IDs, thumbnails, ingredient measurements, preparation instructions, and setup guidance for MCP clients.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
