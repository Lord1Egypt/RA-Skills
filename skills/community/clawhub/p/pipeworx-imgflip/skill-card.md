## Description: <br>
Top 100 meme templates from Imgflip - names, dimensions, and image URLs ready for captioning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to retrieve popular Imgflip meme-template metadata for meme generators, social content tools, random template selection, or meme-format reference data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs npx mcp-remote@latest and sends requests to the Pipeworx Imgflip MCP gateway, so the remote package or service behavior can change over time. <br>
Mitigation: Before installing or deploying, confirm that remote MCP package execution and requests to the Pipeworx gateway are acceptable for the target environment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/brucegutman/pipeworx-imgflip) <br>
- [Pipeworx Imgflip pack](https://pipeworx.io/packs/imgflip) <br>
- [Pipeworx Imgflip MCP gateway](https://gateway.pipeworx.io/imgflip/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown instructions with JSON MCP configuration; tool responses are JSON meme-template records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns template id, name, image URL, width, height, and box count.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
