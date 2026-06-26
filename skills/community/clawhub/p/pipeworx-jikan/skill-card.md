## Description: <br>
Jikan MCP wraps the Jikan v4 API for free, unauthenticated anime and manga data lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an MCP-capable agent to Jikan-backed anime, manga, and character lookup tools without managing an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Anime, manga, and character lookup queries are routed through Pipeworx and its remote Jikan MCP service. <br>
Mitigation: Avoid putting private or sensitive information in lookup terms. <br>
Risk: The connection example runs mcp-remote@latest through npx, so connector behavior may change as new package versions are published. <br>
Mitigation: Pin the mcp-remote package version when reproducible installs are required. <br>


## Reference(s): <br>
- [Pipeworx Jikan pack homepage](https://pipeworx.io/packs/jikan) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-jikan) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration, Shell commands, Text, JSON] <br>
**Output Format:** [Markdown with JSON configuration snippets and MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required; lookups route through the Pipeworx-hosted Jikan MCP gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
