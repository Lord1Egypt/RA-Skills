## Description: <br>
The finest dad jokes on the internet - random, searchable, and groan-worthy from icanhazdadjoke.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch random dad jokes, search jokes by keyword, or retrieve a specific joke for chatbots and messaging workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Joke searches and requests are sent to the Pipeworx gateway. <br>
Mitigation: Treat joke terms and requests as data shared with the remote service and avoid sending sensitive content. <br>
Risk: The setup uses npx mcp-remote, which can download code from npm during installation. <br>
Mitigation: Review the MCP remote setup and package source before running it in a production environment. <br>


## Reference(s): <br>
- [Pipeworx dadjokes homepage](https://pipeworx.io/packs/dadjokes) <br>
- [Pipeworx dadjokes ClawHub page](https://clawhub.ai/brucegutman/pipeworx-dadjokes) <br>
- [Pipeworx dadjokes MCP endpoint](https://gateway.pipeworx.io/dadjokes/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns joke text or search results through a remote MCP endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
