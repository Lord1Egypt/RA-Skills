## Description: <br>
Search and retrieve detailed recipes, find meals by ingredient, or get a random meal suggestion with step-by-step instructions and video links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to search recipes by name or ingredient, retrieve detailed meal instructions, or request a random meal suggestion through the Pipeworx recipes MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recipe search terms are sent to gateway.pipeworx.io. <br>
Mitigation: Avoid entering sensitive personal, dietary, medical, or proprietary context in recipe lookup terms unless sharing it with the external API provider is acceptable. <br>
Risk: Recipe content is returned from an external recipe data source and may be incomplete or unsuitable for a user's needs. <br>
Mitigation: Review ingredients, allergens, cooking instructions, and source links before relying on a recipe. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-recipes) <br>
- [Pipeworx recipes MCP endpoint](https://gateway.pipeworx.io/recipes/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown or plain text recipe results, with JSON configuration snippets and curl commands for MCP setup examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recipe details may include meal category, cuisine area, ingredients, measurements, instructions, thumbnail image, video link, and source URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
