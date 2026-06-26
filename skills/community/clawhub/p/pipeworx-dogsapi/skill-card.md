## Description: <br>
Detailed dog breed encyclopedia covering weight ranges, life spans, temperament, and breed groups from dogapi.dog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to query dog breed details and random dog facts for breed comparison tools, pet adoption experiences, chatbots, and newsletters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests are sent to a remote Pipeworx endpoint. <br>
Mitigation: Use the skill for public dog-breed information and review endpoint use against local network and data-handling policies before deployment. <br>
Risk: The sample MCP configuration uses mcp-remote@latest, which can reduce reproducibility. <br>
Mitigation: Pin or review the mcp-remote package version when reproducible setup matters. <br>


## Reference(s): <br>
- [Pipeworx dogsapi homepage](https://pipeworx.io/packs/dogsapi) <br>
- [Pipeworx dogsapi ClawHub listing](https://clawhub.ai/brucegutman/pipeworx-dogsapi) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns public dog-breed and dog-fact information through a remote Pipeworx MCP endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
