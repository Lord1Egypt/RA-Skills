## Description: <br>
OpenAlex MCP wraps the OpenAlex API for scholarly works search without requiring authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure access to OpenAlex scholarly search tools for works, authors, institutions, and concepts through the Pipeworx MCP gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scholarly search queries are sent through the Pipeworx MCP gateway. <br>
Mitigation: Avoid sensitive private research queries unless the gateway and runtime package source are trusted. <br>
Risk: The connection uses an npm-based MCP bridge. <br>
Mitigation: Review the runtime package source and pin or control package execution according to local deployment policy. <br>


## Reference(s): <br>
- [Pipeworx OpenAlex pack](https://pipeworx.io/packs/openalex) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON configuration and inline command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes scholarly search queries through the disclosed Pipeworx MCP gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
