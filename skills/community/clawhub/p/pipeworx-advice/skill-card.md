## Description: <br>
Crowdsourced life advice - search, browse, or grab a random slip of wisdom from the Advice Slip API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to retrieve random, searched, or ID-specific advice slips for conversational motivation, tip widgets, or placeholder content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Advice searches and tool calls are sent to the Pipeworx gateway. <br>
Mitigation: Avoid submitting sensitive personal information in advice queries and review external service use before deployment. <br>
Risk: The optional MCP client configuration runs npx with mcp-remote@latest. <br>
Mitigation: Prefer direct curl usage for minimal local execution, or pin and review npm package execution before using the MCP configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-advice) <br>
- [Pipeworx Advice Pack](https://pipeworx.io/packs/advice) <br>
- [Pipeworx Advice MCP Gateway](https://gateway.pipeworx.io/advice/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advice-fetching guidance and examples; runtime responses may include advice text, search result counts, slip IDs, and MCP client configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
