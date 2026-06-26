## Description: <br>
Random cat facts and breed information from the Cat Facts API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to fetch random cat facts, retrieve multiple cat facts, or browse cat breed details for chatbots, notifications, educational apps, and harmless test data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests go to Pipeworx's external gateway. <br>
Mitigation: Review whether external API calls are acceptable for the deployment environment before installing or enabling the MCP configuration. <br>
Risk: The optional MCP configuration runs mcp-remote@latest through npx. <br>
Mitigation: In stricter environments, review or pin the helper package version before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-catfacts) <br>
- [Pipeworx Catfacts homepage](https://pipeworx.io/packs/catfacts) <br>
- [Pipeworx Catfacts MCP endpoint](https://gateway.pipeworx.io/catfacts/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill documents calls to an external Pipeworx cat facts MCP/API endpoint and example MCP client configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
