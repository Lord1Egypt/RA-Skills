## Description: <br>
npm MCP wraps the npm Registry API for free, unauthenticated package lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search npm packages, retrieve package metadata, and check download counts through the Pipeworx npm MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package names and search queries are visible to the Pipeworx MCP provider. <br>
Mitigation: Avoid sending sensitive private package names or internal search terms unless that disclosure is acceptable under the user's data policy. <br>
Risk: The connection example installs mcp-remote using the @latest tag. <br>
Mitigation: Pin a reviewed mcp-remote version in controlled or production environments. <br>


## Reference(s): <br>
- [Pipeworx npm Pack](https://pipeworx.io/packs/npm) <br>
- [Pipeworx](https://pipeworx.io) <br>
- [ClawHub release page](https://clawhub.ai/b-gutman/pipeworx-npm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Shell commands] <br>
**Output Format:** [Markdown with JSON configuration and package lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses remote MCP tools for npm package search, package metadata, and download counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
