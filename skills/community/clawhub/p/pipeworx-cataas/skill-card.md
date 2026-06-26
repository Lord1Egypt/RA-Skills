## Description: <br>
Retrieve random cat image URLs, fetch cat images by tag, and list available cat tags through the Pipeworx CATAAS MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users can use this skill to retrieve cat image URLs, find cat images by descriptive tags, and inspect available tags from a no-auth Pipeworx CATAAS MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts a third-party MCP endpoint to retrieve cat image URLs and tags. <br>
Mitigation: Confirm that use of the Pipeworx CATAAS endpoint is acceptable for the agent environment before installation. <br>
Risk: Returned image URLs and tags come from an external service. <br>
Mitigation: Review returned links before using them in sensitive workflows or sharing them externally. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/brucegutman/pipeworx-cataas) <br>
- [Pipeworx CATAAS MCP endpoint](https://gateway.pipeworx.io/cataas/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration] <br>
**Output Format:** [Markdown or plain text containing cat image URLs, cat IDs, tags, and MCP configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill contacts a third-party MCP endpoint and does not require credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
