## Description: <br>
Discover craft breweries across the US — search by name, city, or ID via Open Brewery DB <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to search for US breweries by name, city, or Open Brewery DB UUID and retrieve brewery details such as address, contact information, website, type, and coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-entered brewery search queries are sent to the Pipeworx gateway. <br>
Mitigation: Use the skill only when sending brewery lookup terms to the disclosed remote service is acceptable. <br>
Risk: The optional MCP client configuration uses npx mcp-remote, which downloads and runs an npm package at runtime. <br>
Mitigation: Review and pin or otherwise control the MCP remote package setup before enabling it in managed environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-breweries) <br>
- [Pipeworx breweries pack](https://pipeworx.io/packs/breweries) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns brewery lookup guidance and remote MCP client configuration; brewery result fields may include names, addresses, contact details, websites, types, and coordinates.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
