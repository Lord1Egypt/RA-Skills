## Description: <br>
Access detailed profiles and power stats of 731 superheroes and villains from Marvel, DC, and more for comparison and research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and researchers use this skill to query superhero and villain profiles, compare power statistics, and retrieve biography or appearance details through the Pipeworx MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a clean scan but notes that the target artifact was not available for deeper review. <br>
Mitigation: Review the ClawHub artifact page for a clear purpose, expected permissions, and no surprising credential, persistence, or mutation behavior before installation. <br>
Risk: The skill routes use through a remote MCP endpoint. <br>
Mitigation: Avoid sending sensitive data unless required by the use case, and verify that the endpoint and requested permissions match the documented superhero profile and power-stat lookup behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-superhero) <br>
- [Pipeworx Superhero MCP endpoint](https://gateway.pipeworx.io/superhero/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP tool names, superhero IDs, endpoint configuration, and comparison guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
