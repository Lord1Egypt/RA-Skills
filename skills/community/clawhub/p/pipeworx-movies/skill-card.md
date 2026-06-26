## Description: <br>
Pipeworx Movies connects agents to Pipeworx's Movies MCP for movie search and TV show lookup through iTunes Search API and TVmaze sources without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure movie and TV lookup tools that search movies, TV shows, individual show details, and TV schedules through Pipeworx's remote MCP gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Movie and TV search queries are sent to Pipeworx's remote MCP gateway. <br>
Mitigation: Avoid entering sensitive personal information or confidential queries when using the lookup tools. <br>
Risk: The connection configuration runs the current mcp-remote npm package through npx. <br>
Mitigation: Review the package and command before installation, and use the skill only if that runtime dependency is acceptable. <br>


## Reference(s): <br>
- [Pipeworx Movies Pack](https://pipeworx.io/packs/movies) <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-movies) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON configuration and inline command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces MCP connection guidance for remote movie and TV lookup tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
