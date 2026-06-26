## Description: <br>
Find the right MCP server for a task using an indexed MCP server search service ranked by relevance and community trust. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c5huracan](https://clawhub.ai/user/c5huracan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search for MCP servers that match a plain-language task, then review candidate servers before installation or connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the third-party API at api.rhdxm.com. <br>
Mitigation: Do not include secrets, credentials, private URLs, internal project names, or proprietary details in search phrases. <br>
Risk: Recommended MCP servers may be unsuitable or unsafe for a user's environment. <br>
Mitigation: Review each recommended MCP server before installing, configuring, or connecting it. <br>


## Reference(s): <br>
- [Mcp Finder ClawHub page](https://clawhub.ai/c5huracan/mcp-finder) <br>
- [MCP Finder API documentation](https://api.rhdxm.com/docs) <br>
- [Declared source link in artifact](https://github.com/c5huracan/meyhem) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text search results printed to the terminal] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include candidate server name, URL, stars, language, category, and description when returned by the service.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release metadata; artifact frontmatter says 0.2.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
